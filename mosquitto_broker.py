import paho.mqtt.client as mqtt
import numpy as np
import subprocess
import psutil
import datetime
import threading
import time
import json
from dataFilter import kalman_filter as kf

time_form = datetime.datetime.now().strftime('%y%m%d_%H%M%S')
file_path = time_form + '_rssi.json'

client = mqtt.Client()

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
        client.subscribe("/gw/ac233fc18bf0/status")  # sub topic
        
    def message(self, client, userdata, msg):
        data = json.loads(msg.payload.decode('utf-8'))
        for item in data:
            if "timestamp" in item and "mac" in item and "rssi" in item and 'ibeaconTxPower' in item:
                if item["mac"] not in self.mac_data:
                    self.mac_data[item["mac"]] = []
                self.mac_data[item["mac"]].append({
                    "timestamp": item["timestamp"],
                    "mac": item["mac"],
                    "rssi": item["rssi"],
                    "ibeaconTxPower": item["ibeaconTxPower"]
                })
        
        #kf.apply_kalman_filter(self.mac_data)

        # 필터링된 결과를 저장하거나 추가적인 처리를 수행할 수 있음
        with open(self.file_path, 'w') as json_file:
            json.dump(self.mac_data, json_file, indent=4)

        print("Filtered data saving")
        
    # def broker_start(self):
    #     self.start()
    #     result = self.is_process_running()

    #     check_thread = threading.Thread(target=self.check_process_thread)
    #     check_thread.start()

    #     try:
    #         while True:
    #             time.sleep(1)
    #     except KeyboardInterrupt:
    #         print("\nKeyboardInterrupt!. exit...")
    #     finally:
    #         self.terminate()
    #         check_thread.join()
    #         print("broker threade is break down.")


################# test main code #################
# if __name__ == "__main__":
#     broker = mosquitto_broker()
#     broker.broker_start()
