import json
import os

from searching_most_closed_location import SensorDataAnalyzer
from data_web_socket import send_beacon_data
from datetime import datetime

class handling_json_file:
    
    def __init__(self):
        self.base_filename = datetime.now().strftime("%y%m%d_%H%M00")
        self.count = 5
        self.directory = 'D:\\project_mmp\\measurement_data'
        self.all_device_ids = {'40d63cd705ba', '40d63cd70316', '40d63cd702e8', '40D63cd6fd92', '40d63cd70406'}
        self.last_file_path = ''
        
    def combine_json_files(self):
        checking = False
        predict_xy = SensorDataAnalyzer()
        checking = False
        
        self.base_filename = datetime.now().strftime("%y%m%d_%H%M00")
        if datetime.now().second == 5:
            file_paths = [
                os.path.join(self.directory, f"{self.base_filename}_{device_id}.json")
                for device_id in self.all_device_ids
            ]
            
            combine_file_path = os.path.join(self.directory, f"{self.base_filename}combined.json")
            combined_data = {}

            # Check if all files exist
            all_files_exist = all(os.path.exists(file_path) for file_path in file_paths)
            
            if not all_files_exist:
                return

            # If the combined file already exists, read its content
            if os.path.exists(combine_file_path):
                with open(combine_file_path, 'r') as f:
                    combined_data = json.load(f)
            
            # Read and combine data from existing files
            for file_path in file_paths:
                with open(file_path, 'r') as f:
                    data = json.load(f)
                    combined_data.update(data)  # Merge data into combined_data

            # Write the combined data to the combined file
            try:
                with open(combine_file_path, 'w') as new_file:
                    json.dump(combined_data, new_file, indent=4)
                print(f"Combined data saved to {combine_file_path}")

                checking = True

                # After successfully saving the combined data, delete the original files
                for file_path in file_paths:
                    if os.path.exists(file_path):
                        os.remove(file_path)
                        print(f"Deleted {file_path}")

            except IOError as e:
                print(f"An error occurred while saving the combined file: {e}")
                
            if checking:
                predict_xy.set_tree()
                predict_xy.process_data(combine_file_path)
                send_beacon_data(combine_file_path)
                checking = False