import paho.mqtt.client as mqtt
import subprocess
import psutil
import datetime
import time
import json
import os

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
    def __init__(self):
        self.mac_data_number1 = {}
        self.mac_data_number2 = {}
        self.mac_data_number3 = {}
        self.mac_data_number4 = {}
        self.mac_data_number5 = {}
        self.last_save_second = None
        self.file_path = r'D:\\project_mmp\\measurement_data'

    def number1_sub_connect(self, client, userdata, flags, rc):
        print("Connected with result code " + str(rc))
        client.subscribe('/gw/scanpub/40d63cd6fd92') 

    def number2_sub_connect(self, client, userdata, flags, rc):
        print("Connected with result code " + str(rc))
        client.subscribe('/gw/scanpub/40d63cd705ba') 
        
    def number3_sub_connect(self, client, userdata, flags, rc):
        print("Connected with result code " + str(rc))
        client.subscribe('/gw/scanpub/40d63cd70406') 
        
    def number4_sub_connect(self, client, userdata, flags, rc):
        print("Connected with result code " + str(rc))
        client.subscribe('/gw/scanpub/40d63cd702e8') 
        
    def number5_sub_connect(self, client, userdata, flags, rc):
        print("Connected with result code " + str(rc))
        client.subscribe('/gw/scanpub/40d63cd70316') 
        
    def on_message_to_number1(self, client, userdata, msg):

        data = json.loads(msg.payload.decode('utf-8'))
        current_time = datetime.datetime.now()
        
        for item in data:
            if isinstance(item, dict):
                if item.get("Format") == "Gateway" and "GatewayMAC" in item:
                    gateway_mac = item["GatewayMAC"]
                    if gateway_mac not in self.mac_data_number1:
                        self.mac_data_number1[gateway_mac] = {}

                elif item.get("Format") == "BeaconX Pro-Device info" and "BLEMAC" in item:
                    beacon_mac = item["BLEMAC"]

                    if "TimeStamp" in item and "RSSI" in item:
                        # Ensure gateway_mac is not None before proceeding
                        if gateway_mac is None:
                            print(f"Error: GatewayMAC not set for beacon data {item}")
                            continue

                        if gateway_mac not in self.mac_data_number1:
                            self.mac_data_number1[gateway_mac] = {}
                        if beacon_mac not in self.mac_data_number1[gateway_mac]:
                            self.mac_data_number1[gateway_mac][beacon_mac] = []

                        try:
                            self.mac_data_number1[gateway_mac][beacon_mac].append({
                                "TimeStamp": item["TimeStamp"],
                                "RSSI": item["RSSI"]
                            })
                        except AttributeError as e:
                            print(f"AttributeError occurred: {e}")
                            # Check and correct data structure if necessary
                            if isinstance(self.mac_data_number1[gateway_mac][beacon_mac], dict):
                                print(f"Resetting entry for {gateway_mac}-{beacon_mac} to an empty list.")
                                self.mac_data_number1[gateway_mac][beacon_mac] = []
                                # Retry appending the data
                                self.mac_data_number1[gateway_mac][beacon_mac].append({
                                    "TimeStamp": item["TimeStamp"],
                                    "RSSI": item["RSSI"]
                                })
                            else:
                                print(f"Unexpected error with data at {gateway_mac}-{beacon_mac}. Skipping entry.")
        
        # second == 00 JSON file saved
        if current_time.second == 00 and (self.last_save_second is None or self.last_save_second != 0):
            timestamp_str = current_time.strftime("%y%m%d_%H%M%S")
            file_name = f"{timestamp_str}number.json"
            kf = kalman_filter()
            self.mac_data_number1 = kf.apply_kalman_filter_to_data(self.mac_data_number1)
            
            self.save_data_to_json(self.mac_data_number1, file_name)
            
            self.last_save_second = 0
        else:
            self.last_save_second = current_time.second
        
    def on_message_to_number2(self, client, userdata, msg):

        data = json.loads(msg.payload.decode('utf-8'))
        current_time = datetime.datetime.now()
        
        for item in data:
            if isinstance(item, dict):
                if item.get("Format") == "Gateway" and "GatewayMAC" in item:
                    gateway_mac = item["GatewayMAC"]
                    if gateway_mac not in self.mac_data_number2:
                        self.mac_data_number2[gateway_mac] = {}

                elif item.get("Format") == "BeaconX Pro-Device info" and "BLEMAC" in item:
                    beacon_mac = item["BLEMAC"]

                    if "TimeStamp" in item and "RSSI" in item:
                        # Ensure gateway_mac is not None before proceeding
                        if gateway_mac is None:
                            print(f"Error: GatewayMAC not set for beacon data {item}")
                            continue

                        if gateway_mac not in self.mac_data_number1:
                            self.mac_data_number2[gateway_mac] = {}
                        if beacon_mac not in self.mac_data_number2[gateway_mac]:
                            self.mac_data_number2[gateway_mac][beacon_mac] = []

                        try:
                            self.mac_data_number2[gateway_mac][beacon_mac].append({
                                "TimeStamp": item["TimeStamp"],
                                "RSSI": item["RSSI"]
                            })
                        except AttributeError as e:
                            print(f"AttributeError occurred: {e}")
                            # Check and correct data structure if necessary
                            if isinstance(self.mac_data_number2[gateway_mac][beacon_mac], dict):
                                print(f"Resetting entry for {gateway_mac}-{beacon_mac} to an empty list.")
                                self.mac_data_number2[gateway_mac][beacon_mac] = []
                                # Retry appending the data
                                self.mac_data_number2[gateway_mac][beacon_mac].append({
                                    "TimeStamp": item["TimeStamp"],
                                    "RSSI": item["RSSI"]
                                })
                            else:
                                print(f"Unexpected error with data at {gateway_mac}-{beacon_mac}. Skipping entry.")
        
        # second == 00 JSON file saved
        if current_time.second == 00 and (self.last_save_second is None or self.last_save_second != 0):
            timestamp_str = current_time.strftime("%y%m%d_%H%M%S")
            file_name = f"{timestamp_str}number.json"
            kf = kalman_filter()
            self.mac_data_number2 = kf.apply_kalman_filter_to_data(self.mac_data_number2)
            
            self.save_data_to_json(self.mac_data_number2, file_name)
            
            self.last_save_second = 0
        else:
            self.last_save_second = current_time.second
            

    def on_message_to_number3(self, client, userdata, msg):

        data = json.loads(msg.payload.decode('utf-8'))
        current_time = datetime.datetime.now()
        
        for item in data:
            if isinstance(item, dict):
                if item.get("Format") == "Gateway" and "GatewayMAC" in item:
                    gateway_mac = item["GatewayMAC"]
                    if gateway_mac not in self.mac_data_number3:
                        self.mac_data_number3[gateway_mac] = {}

                elif item.get("Format") == "BeaconX Pro-Device info" and "BLEMAC" in item:
                    beacon_mac = item["BLEMAC"]

                    if "TimeStamp" in item and "RSSI" in item:
                        # Ensure gateway_mac is not None before proceeding
                        if gateway_mac is None:
                            print(f"Error: GatewayMAC not set for beacon data {item}")
                            continue

                        if gateway_mac not in self.mac_data_number3:
                            self.mac_data_number3[gateway_mac] = {}
                        if beacon_mac not in self.mac_data_number3[gateway_mac]:
                            self.mac_data_number3[gateway_mac][beacon_mac] = []

                        try:
                            self.mac_data_number3[gateway_mac][beacon_mac].append({
                                "TimeStamp": item["TimeStamp"],
                                "RSSI": item["RSSI"]
                            })
                        except AttributeError as e:
                            print(f"AttributeError occurred: {e}")
                            # Check and correct data structure if necessary
                            if isinstance(self.mac_data_number3[gateway_mac][beacon_mac], dict):
                                print(f"Resetting entry for {gateway_mac}-{beacon_mac} to an empty list.")
                                self.mac_data_number3[gateway_mac][beacon_mac] = []
                                # Retry appending the data
                                self.mac_data_number3[gateway_mac][beacon_mac].append({
                                    "TimeStamp": item["TimeStamp"],
                                    "RSSI": item["RSSI"]
                                })
                            else:
                                print(f"Unexpected error with data at {gateway_mac}-{beacon_mac}. Skipping entry.")
        
        # second == 00 JSON file saved
        if current_time.second == 00 and (self.last_save_second is None or self.last_save_second != 0):
            timestamp_str = current_time.strftime("%y%m%d_%H%M%S")
            file_name = f"{timestamp_str}number.json"
            kf = kalman_filter()
            self.mac_data_number3 = kf.apply_kalman_filter_to_data(self.mac_data_number3)
            
            self.save_data_to_json(self.mac_data_number3, file_name)
            
            self.last_save_second = 0
        else:
            self.last_save_second = current_time.second
            
    def on_message_to_number4(self, client, userdata, msg):

        data = json.loads(msg.payload.decode('utf-8'))
        current_time = datetime.datetime.now()
        
        for item in data:
            if isinstance(item, dict):
                if item.get("Format") == "Gateway" and "GatewayMAC" in item:
                    gateway_mac = item["GatewayMAC"]
                    if gateway_mac not in self.mac_data_number4:
                        self.mac_data_number4[gateway_mac] = {}

                elif item.get("Format") == "BeaconX Pro-Device info" and "BLEMAC" in item:
                    beacon_mac = item["BLEMAC"]

                    if "TimeStamp" in item and "RSSI" in item:
                        # Ensure gateway_mac is not None before proceeding
                        if gateway_mac is None:
                            print(f"Error: GatewayMAC not set for beacon data {item}")
                            continue

                        if gateway_mac not in self.mac_data_number4:
                            self.mac_data_number4[gateway_mac] = {}
                        if beacon_mac not in self.mac_data_number4[gateway_mac]:
                            self.mac_data_number4[gateway_mac][beacon_mac] = []

                        try:
                            self.mac_data_number4[gateway_mac][beacon_mac].append({
                                "TimeStamp": item["TimeStamp"],
                                "RSSI": item["RSSI"]
                            })
                        except AttributeError as e:
                            print(f"AttributeError occurred: {e}")
                            # Check and correct data structure if necessary
                            if isinstance(self.mac_data_number4[gateway_mac][beacon_mac], dict):
                                print(f"Resetting entry for {gateway_mac}-{beacon_mac} to an empty list.")
                                self.mac_data_number4[gateway_mac][beacon_mac] = []
                                # Retry appending the data
                                self.mac_data_number4[gateway_mac][beacon_mac].append({
                                    "TimeStamp": item["TimeStamp"],
                                    "RSSI": item["RSSI"]
                                })
                            else:
                                print(f"Unexpected error with data at {gateway_mac}-{beacon_mac}. Skipping entry.")
        
        # second == 00 JSON file saved
        if current_time.second == 00 and (self.last_save_second is None or self.last_save_second != 0):
            timestamp_str = current_time.strftime("%y%m%d_%H%M%S")
            file_name = f"{timestamp_str}number.json"
            kf = kalman_filter()
            self.mac_data_number4 = kf.apply_kalman_filter_to_data(self.mac_data_number4)
            
            self.save_data_to_json(self.mac_data_number4, file_name)
            
            self.last_save_second = 0
        else:
            self.last_save_second = current_time.second
            
    def on_message_to_number5(self, client, userdata, msg):

        data = json.loads(msg.payload.decode('utf-8'))
        current_time = datetime.datetime.now()
        
        for item in data:
            if isinstance(item, dict):
                if item.get("Format") == "Gateway" and "GatewayMAC" in item:
                    gateway_mac = item["GatewayMAC"]
                    if gateway_mac not in self.mac_data_number5:
                        self.mac_data_number5[gateway_mac] = {}

                elif item.get("Format") == "BeaconX Pro-Device info" and "BLEMAC" in item:
                    beacon_mac = item["BLEMAC"]

                    if "TimeStamp" in item and "RSSI" in item:
                        # Ensure gateway_mac is not None before proceeding
                        if gateway_mac is None:
                            print(f"Error: GatewayMAC not set for beacon data {item}")
                            continue

                        if gateway_mac not in self.mac_data_number5:
                            self.mac_data_number5[gateway_mac] = {}
                        if beacon_mac not in self.mac_data_number5[gateway_mac]:
                            self.mac_data_number5[gateway_mac][beacon_mac] = []

                        try:
                            self.mac_data_number5[gateway_mac][beacon_mac].append({
                                "TimeStamp": item["TimeStamp"],
                                "RSSI": item["RSSI"]
                            })
                        except AttributeError as e:
                            print(f"AttributeError occurred: {e}")
                            # Check and correct data structure if necessary
                            if isinstance(self.mac_data_number5[gateway_mac][beacon_mac], dict):
                                print(f"Resetting entry for {gateway_mac}-{beacon_mac} to an empty list.")
                                self.mac_data_number5[gateway_mac][beacon_mac] = []
                                # Retry appending the data
                                self.mac_data_number5[gateway_mac][beacon_mac].append({
                                    "TimeStamp": item["TimeStamp"],
                                    "RSSI": item["RSSI"]
                                })
                            else:
                                print(f"Unexpected error with data at {gateway_mac}-{beacon_mac}. Skipping entry.")
        
       # second == 00 JSON file saved
        if current_time.second == 00 and (self.last_save_second is None or self.last_save_second != 0):
            timestamp_str = current_time.strftime("%y%m%d_%H%M%S")
            file_name = f"{timestamp_str}number.json"
            kf = kalman_filter()
            self.mac_data_number5 = kf.apply_kalman_filter_to_data(self.mac_data_number5)
            
            self.save_data_to_json(self.mac_data_number5, file_name)
            
            self.last_save_second = 0
        else:
            self.last_save_second = current_time.second
            
    def save_data_to_json(self, data, file_name):
        
        file_path = f'{self.file_path}/{file_name}'
        
        if(self.mac_data_number1,self.mac_data_number2, 
           self.mac_data_number3,self.mac_data_number4,
           self.mac_data_number5 != {}):
            if os.path.exists(file_path):
                # If the file exists, append data to it
                with open(file_path, 'a') as f:
                    f.write("\n")  # Write a new line to separate entries
                    json.dump(data, f, indent=4)                 
                    data = {}
            else:
                # If the file does not exist, create it and write data
                with open(file_path, 'w') as f:
                    json.dump(data, f, indent=4)
                    data = {}
    
    
################## test main code #################

# # set MQTT broker
# broker_address = "" 
# broker_port = 1883

# # set client 
# client = mqtt.Client()        

# if __name__ == "__main__":
#     broker = mqtt_broker()
#     broker.broker_start()
    
#     sub = mqtt_sub()
#     client.on_connect = sub.sub_connect
#     client.on_message = sub.on_message
#     client.connect(broker_address, broker_port)
#     client.loop_forever()