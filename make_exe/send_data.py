import asyncio
import websockets
import datetime
import json
import os
from datetime import datetime as dt
from searching_most_closed_location import SensorDataAnalyzer

class HandlingJsonFile:
    def __init__(self):
        self.directory = 'D:/project_mmp/make_exe/main_data/reference_coordinates_data.json'
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
                file_name = f'D:/project_mmp/make_exe/measurement_data/{timestamp_str}_beacondata.json'
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