import os
import json
import numpy as np

class coordinate:
    def __init__(self):
        self.folder_path = r'D:\\project_mmp\\measurement_data'
        
    def find_near_gateway(self, name):
        file_list = os.listdir(self.folder_path)
        all_beacon_rssi = {} 
        
        # read data(correct name) and svae in all_beacon_rssi
        for filename in file_list:
            if filename.endswith('.json') and name in filename:
                file_path = os.path.join(self.folder_path, filename)
                with open(file_path, 'r', encoding='utf-8') as file:
                    data = json.load(file)
                    
                    for gateway_mac, beacon_data in data.items():
                        for beacon_mac, rssi_stats in beacon_data.items():
                            average_rssi = rssi_stats['average']
                            
                            if beacon_mac not in all_beacon_rssi:
                                all_beacon_rssi[beacon_mac] = {}
                            
                            all_beacon_rssi[beacon_mac][gateway_mac] = average_rssi

        # find strongest rssi value gateway for each mac address
        for beacon_mac, gateway_data in all_beacon_rssi.items():
            max_average_rssi = -np.inf
            max_rssi_gateway = None
            
            for gateway_mac, average_rssi in gateway_data.items():
                if average_rssi > max_average_rssi:
                    max_average_rssi = average_rssi
                    max_rssi_gateway = gateway_mac
            
            if max_rssi_gateway is not None:
                print(f"For Beacon Mac: {beacon_mac}, Nearest Gateway: {max_rssi_gateway}, Average RSSI: {max_average_rssi}")
            else:
                print(f"No data found for Beacon Mac: {beacon_mac}")

    def return_coordinate():
        print('test')
        # read criterion coordinate
        # find nearest criterion coordinate
        # conversion of rssi to coordinate
        # return coordinate

################# test main code #################

# folder_path = r'D:\\project_mmp\\measurement_data'
# name_to_find = "133000"

# if __name__ == '__main__':
#     find_near_gateway(folder_path, name_to_find)
