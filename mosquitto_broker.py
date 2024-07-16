import paho.mqtt.client as mqtt
import subprocess
import psutil
import datetime
import time
import json

from dataFilter import kalman_filter as kf

time_form = datetime.datetime.now().strftime('%y%m%d_%H%M%S')
file_path = f'D:\\project_mmp\\measurement_data\\{time_form}_rssi(far_gateway).json'

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
        self.file_path = file_path

    def sub_connect(self, client, userdata, flags, rc):
        print("Connected with result code " + str(rc))
        client.subscribe("/gw/scanpub/40d63cd6fd92")  
        
    def on_message(self, client, userdata, msg):
        data = json.loads(msg.payload.decode('utf-8'))
            
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
        
        with open(self.file_path, 'w') as json_file:
            json.dump(self.mac_data, json_file, indent=4)
            
        # put this line dataFilter class
        
        print(f'{time_form} Filtered data saving')
        
        
################# test main code #################
# if __name__ == "__main__":
#     broker = mosquitto_broker()
#     broker.broker_start()