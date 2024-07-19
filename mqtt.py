import paho.mqtt.client as mqtt
import subprocess
import psutil
import datetime
import time
import json

from dataFilter import kalman_filter

filt_path = r'D:\\project_mmp\\measurement_data'

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
        self.mac_data = {}
        self.last_save_minute = None
        self.last_save_second = None
        self.file_path = filt_path

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
        current_second = current_time.second
        
        for item in data:
            if isinstance(item, dict):
                if item.get("Format") == "Gateway" and "GatewayMAC" in item:
                    gateway_mac = item["GatewayMAC"]
                    if gateway_mac not in self.mac_data:
                        self.mac_data[gateway_mac] = {}
                
                elif item.get("Format") == "BeaconX Pro-Device info" and "BLEMAC" in item:
                    beacon_mac = item["BLEMAC"]
                    
                    if "TimeStamp" in item and "RSSI" in item:
                        if gateway_mac not in self.mac_data:
                            self.mac_data[gateway_mac] = {}
                        if beacon_mac not in self.mac_data[gateway_mac]:
                            self.mac_data[gateway_mac][beacon_mac] = []
                        
                        self.mac_data[gateway_mac][beacon_mac].append({
                            "TimeStamp": item["TimeStamp"],
                            "RSSI": item["RSSI"],
                            "BattVoltage": item.get("BattVoltage", "")
                        })
        
        # minute == 00 JSON file saved
        if current_time.minute == 27 and (self.last_save_minute is None or self.last_save_minute != 0) and current_second == 0 and (self.last_save_second is None or self.last_save_second != 0):
            timestamp_str = current_time.strftime("%y%m%d_%H%M%S")
            file_name = f"filtered_data_{timestamp_str}_(12)_number1.json"
            kf = kalman_filter()
            self.mac_data = kf.apply_kalman_filter_to_data(self.mac_data)
            with open(f'{self.file_path}/{file_name}', 'w') as f:
                json.dump(self.mac_data, f, indent=4)
                
            print(f'Filtered data saved to {self.file_path}')
            self.last_save_minute = 0
            self.mac_data = {}
        else:
            self.last_save_minute = current_time.minute
        
    def on_message_to_number2(self, client, userdata, msg):

        data = json.loads(msg.payload.decode('utf-8'))
        current_time = datetime.datetime.now()
        current_second = current_time.second
        
        for item in data:
            if isinstance(item, dict):
                if item.get("Format") == "Gateway" and "GatewayMAC" in item:
                    gateway_mac = item["GatewayMAC"]
                    if gateway_mac not in self.mac_data:
                        self.mac_data[gateway_mac] = {}
                
                elif item.get("Format") == "BeaconX Pro-Device info" and "BLEMAC" in item:
                    beacon_mac = item["BLEMAC"]
                    
                    if "TimeStamp" in item and "RSSI" in item:
                        if gateway_mac not in self.mac_data:
                            self.mac_data[gateway_mac] = {}
                        if beacon_mac not in self.mac_data[gateway_mac]:
                            self.mac_data[gateway_mac][beacon_mac] = []
                        
                        self.mac_data[gateway_mac][beacon_mac].append({
                            "TimeStamp": item["TimeStamp"],
                            "RSSI": item["RSSI"],
                            "BattVoltage": item.get("BattVoltage", "")
                        })
        
        # minute == 00 JSON file saved
        if current_time.minute == 27 and (self.last_save_minute is None or self.last_save_minute != 0) and current_second == 0 and (self.last_save_second is None or self.last_save_second != 0):
            timestamp_str = current_time.strftime("%y%m%d_%H%M%S")
            file_name = f"filtered_data_{timestamp_str}_(12)_number2.json"
            kf = kalman_filter()
            self.mac_data = kf.apply_kalman_filter_to_data(self.mac_data)
            with open(f'{self.file_path}/{file_name}', 'w') as f:
                json.dump(self.mac_data, f, indent=4)
                
            print(f'Filtered data saved to {self.file_path}')
            self.last_save_minute = 0
            self.mac_data = {}
        else:
            self.last_save_minute = current_time.minute
            

    def on_message_to_number3(self, client, userdata, msg):

        data = json.loads(msg.payload.decode('utf-8'))
        current_time = datetime.datetime.now()
        current_second = current_time.second
        
        for item in data:
            if isinstance(item, dict):
                if item.get("Format") == "Gateway" and "GatewayMAC" in item:
                    gateway_mac = item["GatewayMAC"]
                    if gateway_mac not in self.mac_data:
                        self.mac_data[gateway_mac] = {}
                
                elif item.get("Format") == "BeaconX Pro-Device info" and "BLEMAC" in item:
                    beacon_mac = item["BLEMAC"]
                    
                    if "TimeStamp" in item and "RSSI" in item:
                        if gateway_mac not in self.mac_data:
                            self.mac_data[gateway_mac] = {}
                        if beacon_mac not in self.mac_data[gateway_mac]:
                            self.mac_data[gateway_mac][beacon_mac] = []
                        
                        self.mac_data[gateway_mac][beacon_mac].append({
                            "TimeStamp": item["TimeStamp"],
                            "RSSI": item["RSSI"],
                            "BattVoltage": item.get("BattVoltage", "")
                        })
        
        # minute == 00 JSON file saved
        if current_time.minute == 27 and (self.last_save_minute is None or self.last_save_minute != 0) and current_second == 0 and (self.last_save_second is None or self.last_save_second != 0):
            timestamp_str = current_time.strftime("%y%m%d_%H%M%S")
            file_name = f"filtered_data_{timestamp_str}_(12)_number3.json"
            kf = kalman_filter()
            self.mac_data = kf.apply_kalman_filter_to_data(self.mac_data)
            with open(f'{self.file_path}/{file_name}', 'w') as f:
                json.dump(self.mac_data, f, indent=4)
                
            print(f'Filtered data saved to {self.file_path}')
            self.last_save_minute = 0
            self.mac_data = {}
        else:
            self.last_save_minute = current_time.minute
            
    def on_message_to_number4(self, client, userdata, msg):

        data = json.loads(msg.payload.decode('utf-8'))
        current_time = datetime.datetime.now()
        current_second = current_time.second
        
        for item in data:
            if isinstance(item, dict):
                if item.get("Format") == "Gateway" and "GatewayMAC" in item:
                    gateway_mac = item["GatewayMAC"]
                    if gateway_mac not in self.mac_data:
                        self.mac_data[gateway_mac] = {}
                
                elif item.get("Format") == "BeaconX Pro-Device info" and "BLEMAC" in item:
                    beacon_mac = item["BLEMAC"]
                    
                    if "TimeStamp" in item and "RSSI" in item:
                        if gateway_mac not in self.mac_data:
                            self.mac_data[gateway_mac] = {}
                        if beacon_mac not in self.mac_data[gateway_mac]:
                            self.mac_data[gateway_mac][beacon_mac] = []
                        
                        self.mac_data[gateway_mac][beacon_mac].append({
                            "TimeStamp": item["TimeStamp"],
                            "RSSI": item["RSSI"],
                            "BattVoltage": item.get("BattVoltage", "")
                        })
        
        # minute == 00 JSON file saved
        if current_time.minute == 27 and (self.last_save_minute is None or self.last_save_minute != 0) and current_second == 0 and (self.last_save_second is None or self.last_save_second != 0):
            timestamp_str = current_time.strftime("%y%m%d_%H%M%S")
            file_name = f"filtered_data_{timestamp_str}_(12)_number4.json"
            kf = kalman_filter()
            self.mac_data = kf.apply_kalman_filter_to_data(self.mac_data)
            with open(f'{self.file_path}/{file_name}', 'w') as f:
                json.dump(self.mac_data, f, indent=4)
                
            print(f'Filtered data saved to {self.file_path}')
            self.last_save_minute = 0
            self.mac_data = {}
        else:
            self.last_save_minute = current_time.minute
            
    def on_message_to_number5(self, client, userdata, msg):

        data = json.loads(msg.payload.decode('utf-8'))
        current_time = datetime.datetime.now()
        current_second = current_time.second
        
        for item in data:
            if isinstance(item, dict):
                if item.get("Format") == "Gateway" and "GatewayMAC" in item:
                    gateway_mac = item["GatewayMAC"]
                    if gateway_mac not in self.mac_data:
                        self.mac_data[gateway_mac] = {}
                
                elif item.get("Format") == "BeaconX Pro-Device info" and "BLEMAC" in item:
                    beacon_mac = item["BLEMAC"]
                    
                    if "TimeStamp" in item and "RSSI" in item:
                        if gateway_mac not in self.mac_data:
                            self.mac_data[gateway_mac] = {}
                        if beacon_mac not in self.mac_data[gateway_mac]:
                            self.mac_data[gateway_mac][beacon_mac] = []
                        
                        self.mac_data[gateway_mac][beacon_mac].append({
                            "TimeStamp": item["TimeStamp"],
                            "RSSI": item["RSSI"],
                            "BattVoltage": item.get("BattVoltage", "")
                        })
        
       # minute == 00 JSON file saved
        if current_time.minute == 27 and (self.last_save_minute is None or self.last_save_minute != 0) and current_second == 0 and (self.last_save_second is None or self.last_save_second != 0):
            timestamp_str = current_time.strftime("%y%m%d_%H%M%S")
            file_name = f"filtered_data_{timestamp_str}_(12)_number5.json"
            kf = kalman_filter()
            self.mac_data = kf.apply_kalman_filter_to_data(self.mac_data)
            with open(f'{self.file_path}/{file_name}', 'w') as f:
                json.dump(self.mac_data, f, indent=4)
                
            print(f'Filtered data saved to {self.file_path}')
            self.last_save_minute = 0
            self.mac_data = {}
        else:
            self.last_save_minute = current_time.minute
            
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