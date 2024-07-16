import json 

test_message = [
    {
        "TimeStamp": "2024-07-16T05:55:50.006Z",
        "Format": "Gateway",
        "GatewayMAC": "40D63CD6FD92"
    },
    {
        "TimeStamp": "2024-07-16T05:55:49.557Z",
        "Format": "BeaconX Pro-Device info",
        "BLEMAC": "F4741C781187",
        "RSSI": -68,
        "AdvType": "Legacy",
        "BLEName": "BeaconX Pro",
        "TxPower": 0,
        "RSSI@0m": 0,
        "AdvInterval": 1000,
        "BattVoltage": 3115,
        "FirmwareVer": "V3.0.11"
    },
    {
        "TimeStamp": "2024-07-16T05:55:49.195Z",
        "Format": "BeaconX Pro-Device info",
        "BLEMAC": "DE42759B6E12",
        "RSSI": -64,
        "AdvType": "Legacy",
        "BLEName": "BeaconX Pro",
        "TxPower": 0,
        "RSSI@0m": 0,
        "AdvInterval": 1000,
        "BattVoltage": 3022,
        "FirmwareVer": "V3.0.11"
    }
]

class mqtt_sub:
    def __init__(self):
        self.mac_data = {}
        self.file_path = 'test.json'
        
    def message_filter(self, data):
        for item in data:
            if isinstance(item, dict):
                if item.get("Format") == "Gateway" and "GatewayMAC" in item:
                    gateway_mac = item["GatewayMAC"]
                    if gateway_mac not in self.mac_data:
                        self.mac_data[gateway_mac] = {}
                
                elif item.get("Format") == "BeaconX Pro-Device info" and "BLEMAC" in item:
                    gateway_mac = item.get("GatewayMAC", "")  # Beacon 정보에 GatewayMAC이 없을 수 있음
                    beacon_mac = item["BLEMAC"]
                    
                    if gateway_mac not in self.mac_data:
                        self.mac_data[gateway_mac] = {}
                    
                    if beacon_mac not in self.mac_data[gateway_mac]:
                        self.mac_data[gateway_mac][beacon_mac] = []
                    
                    self.mac_data[gateway_mac][beacon_mac].append({
                        "TimeStamp": item.get("TimeStamp", ""),
                        "RSSI": item.get("RSSI", ""),
                        "BattVoltage": item.get("BattVoltage", "")
                    })
       
        with open(self.file_path, 'w') as json_file:
            json.dump(self.mac_data, json_file, indent=4)
        
test = mqtt_sub()
test.message_filter(test_message)
        
with open(test.file_path, 'r') as f:
    print(f.read())