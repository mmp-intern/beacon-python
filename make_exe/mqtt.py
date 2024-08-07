import subprocess
import datetime
import psutil
import time
import json
import os
import paho.mqtt.client as mqtt
from collections import defaultdict
from dataFilter import kalman_filter

class mqtt_broker:
    def __init__(self):
        self.popen = None

    def broker_start(self) -> subprocess.Popen:
        cmd = ["mosquitto", "-v"]
        self.popen = subprocess.Popen(cmd, stdout=subprocess.PIPE)
        return self.popen

    def terminate(self):
        if self.popen:
            self.popen.kill()

    def is_process_running(self) -> bool:
        for process in psutil.process_iter(['pid', 'name']):
            if process.pid == self.popen.pid and process.info['name'] == 'mosquitto':
                return True
        return False

    def check_process_thread(self):
        while True:
            if not self.is_process_running():
                break
            time.sleep(1)

class mqtt_sub:
    def __init__(self, broker_address, broker_port):
        # Use a single dictionary to hold all MAC data
        self.mac_data = defaultdict(lambda: defaultdict(list))
        self.last_save_second = None
        self.file_path = r'D:\\project_mmp\\make_exe\\measurement_data'
        self.broker_address = broker_address
        self.broker_port = broker_port
        self.client = mqtt.Client()

    def start(self):
        # Assign callback functions
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message
        
        # Connect to the broker
        self.client.connect(self.broker_address, self.broker_port)
        
        # Start the loop
        self.client.loop_start()

    def on_connect(self, client, userdata, flags, rc):
        print("Connected with result code " + str(rc))
        # Subscribe to all required topics
        self.client.subscribe('/gw/scanpub/40d63cd6fd92') 
        self.client.subscribe('/gw/scanpub/40d63cd705ba')
        self.client.subscribe('/gw/scanpub/40d63cd70406')
        self.client.subscribe('/gw/scanpub/40d63cd702e8')
        self.client.subscribe('/gw/scanpub/40d63cd70316')

    def on_message(self, client, userdata, msg):
        topic_handlers = {
            '/gw/scanpub/40d63cd6fd92': self.handle_topic,
            '/gw/scanpub/40d63cd705ba': self.handle_topic,
            '/gw/scanpub/40d63cd70406': self.handle_topic,
            '/gw/scanpub/40d63cd702e8': self.handle_topic,
            '/gw/scanpub/40d63cd70316': self.handle_topic,
        }

        handler = topic_handlers.get(msg.topic)
        if handler:
            handler(msg, msg.topic)
        else:
            print(f"Unhandled topic: {msg.topic}")

    def handle_topic(self, msg, topic):
        data = json.loads(msg.payload.decode('utf-8'))
        current_time = datetime.datetime.now()

        for item in data:
            if isinstance(item, dict):
                if item.get("Format") == "Gateway" and "GatewayMAC" in item:
                    gateway_mac = item["GatewayMAC"]
                    if gateway_mac not in self.mac_data:
                        self.mac_data[gateway_mac] = {}

                elif item.get("Format") == "BeaconX Pro-Device info" and "BLEMAC" in item:
                    beacon_mac = item["BLEMAC"]

                    if "TimeStamp" in item and "RSSI" in item:
                        if gateway_mac is None:
                            print(f"Error: GatewayMAC not set for beacon data {item}")
                            continue

                        if beacon_mac not in self.mac_data[gateway_mac]:
                            self.mac_data[gateway_mac][beacon_mac] = []

                        try:
                            self.mac_data[gateway_mac][beacon_mac].append({
                                "TimeStamp": item["TimeStamp"],
                                "RSSI": item["RSSI"]
                            })
                        except AttributeError as e:
                            if isinstance(self.mac_data[gateway_mac][beacon_mac], dict):
                                self.mac_data[gateway_mac][beacon_mac] = []
                                self.mac_data[gateway_mac][beacon_mac].append({
                                    "TimeStamp": item["TimeStamp"],
                                    "RSSI": item["RSSI"]
                                })
                            else:
                                print(f"Unexpected error with data at {gateway_mac}-{beacon_mac}. Skipping entry.")
        
        # Save data every 10 seconds
        if current_time.second % 10 == 0 and (self.last_save_second is None or self.last_save_second != current_time.second):
            timestamp_str = current_time.strftime("%y%m%d_%H%M%S")
            file_name = f"{timestamp_str}_beacondata.json"
            kf = kalman_filter()
            filtered_data = kf.apply_kalman_filter_to_data(self.mac_data)
            self.save_data_to_json(filtered_data, file_name)
            self.last_save_second = current_time.second
        else:
            self.last_save_second = current_time.second

    def save_data_to_json(self, data, file_name,max_retries=3, delay=1):
        file_path = os.path.join(self.file_path, file_name)
        attempt = 0
        
        while attempt < max_retries:
            try:
                with open(file_path, 'w') as f:
                    json.dump(data, f, indent=4)
                print(f"\nData successfully saved\n")
                if os.path.exists(file_path):
                    return True
                else:
                    raise IOError(f"File does not exist after writing.")
            except IOError as e:
                print(f"\nError saving data: {e}")
                attempt += 1
                print(f"Retrying ({attempt}/{max_retries})...")
                time.sleep(delay)
        
        print(f"Failed to save data after {max_retries} attempts.")
        return False

# Example usage:
if __name__ == "__main__":
    broker_address = "192.168.0.71"
    broker_port = 1883

    broker = mqtt_broker()
    broker.broker_start()
    
    sub = mqtt_sub(broker_address, broker_port)
    sub.start()

    # Keep the main thread running
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("Exiting...")
    finally:
        sub.client.loop_stop()
        broker.terminate()
