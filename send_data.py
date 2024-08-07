import asyncio
import websockets
import datetime
import json
import os
from datetime import datetime as dt
from searching_most_closed_location import SensorDataAnalyzer

class HandlingJsonFile:
    def __init__(self):
        self.directory = 'D:\\project_mmp\\measurement_data'
        self.all_device_ids = {'40d63cd705ba', '40d63cd70316', '40d63cd702e8', '40D63cd6fd92', '40d63cd70406'}
        self.interval = 10
        self.last_save_second = None
        self.file_path = ''

    async def send_beacon_data(self):
        uri = "ws://localhost:8080/ws/beacon"
        predict_xy = SensorDataAnalyzer()
        predict_xy.set_tree()

        while True:
            current_time = dt.now()
            if current_time.second % 10 == 0 and (self.last_save_second is None or self.last_save_second != current_time.second):
                timestamp_str = current_time.strftime("%y%m%d_%H%M%S")
                file_name = f"D:\project_mmp\measurement_data\{timestamp_str}_beacondata.json"
                file_path = os.path.join(self.directory, file_name)
                
                # Wait for the next 10 seconds to avoid checking every second
                await asyncio.sleep(1)

                if os.path.exists(file_path):
                    try:
                        async with websockets.connect(uri) as websocket:
                            # Check if the file exists
                            if not os.path.isfile(file_path):
                                print("Error: File not found.")
                                continue

                            try:
                                # Read and process the file
                                with open(file_path, 'r') as file:
                                    data = json.load(file)

                                # Transform the data
                                beacon_data = {"gateways": []}
                                for gatewayMac, beacons in data.items():
                                    gateway_entry = {"gatewayMac": gatewayMac, "beacons": []}
                                    for mac, info in beacons.items():
                                        beacon_entry = {
                                            "mac": mac,
                                            "earlyTimestamp": info.get("early_timestamp", "N/A"),
                                            "lateTimestamp": info.get("late_timestamp", "N/A")
                                        }
                                        gateway_entry["beacons"].append(beacon_entry)
                                    beacon_data["gateways"].append(gateway_entry)

                                beacon_data_str = json.dumps(beacon_data, indent=2)
                                await websocket.send(beacon_data_str)
                                print(f"Sent data: {beacon_data_str}")

                                predict_xy.process_data(file_path)
                                
                            except json.JSONDecodeError as e:
                                print(f"JSON Error: {e}")
                            except Exception as e:
                                print(f"File Read/Error: {e}")

                    except (websockets.exceptions.ConnectionClosedError, websockets.exceptions.InvalidURI) as e:
                        print(f"WebSocket Error: {e}")
                        await asyncio.sleep(10)  # Wait before trying to reconnect
                else:
                    print(f"File {file_name} does not exist.")
            else:
                await asyncio.sleep(1)  # Short sleep to avoid high CPU usage

            self.last_save_second = current_time.second

    # async def combine_json_files(self):
    #     predict_xy = SensorDataAnalyzer()
    #     while True:
    #         now = datetime.now()
    #         if now.second % 10 != 0:
    #             await asyncio.sleep(1)  # Wait a second and check again
    #             print('it''s not time to go!')
    #             continue
            
    #         base_filename = now.strftime(f"%y%m%d_%H%M{now.second:02}")
    #         file_paths = [
    #             os.path.join(self.directory, f"{base_filename}_{device_id}.json")
    #             for device_id in self.all_device_ids
    #         ]
    #         combine_file_path = os.path.join(self.directory, f"{base_filename}combined.json")
    #         combined_data = {}

    #         # Check if all files exist
    #         all_files_exist = all(os.path.exists(file_path) for file_path in file_paths)
    #         if not all_files_exist:
    #             print("All files do not exist.")
    #             await asyncio.sleep(self.interval)
    #             continue

    #         # If the combined file already exists, read its content
    #         if os.path.exists(combine_file_path):
    #             with open(combine_file_path, 'r') as f:
    #                 combined_data = json.load(f)

    #         # Read and combine data from existing files
    #         for file_path in file_paths:
    #             with open(file_path, 'r') as f:
    #                 data = json.load(f)
    #                 combined_data.update(data)  # Merge data into combined_data

    #         # Write the combined data to the combined file
    #         try:
    #             with open(combine_file_path, 'w') as new_file:
    #                 json.dump(combined_data, new_file, indent=4)
    #             print(f"Combined data saved to {combine_file_path}")

    #             # After successfully saving the combined data, delete the original files
    #             for file_path in file_paths:
    #                 if os.path.exists(file_path):
    #                     os.remove(file_path)
    #                     print(f"Deleted {file_path}")

    #             self.checking = True

    #         except IOError as e:
    #             print(f"An error occurred while saving the combined file: {e}")

    #         if self.checking:
    #             print("Processing and sending beacon data")
    #             predict_xy.set_tree()
    #             predict_xy.process_data(combine_file_path)
    #             self.file_path = combine_file_path  # Update file_path with the combined file
    #             self.send_beacon_data()  # Call the coroutine directly
    #             self.checking = False

    #         await asyncio.sleep(self.interval)  # Check every `interval` seconds
