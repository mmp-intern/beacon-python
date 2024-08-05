import numpy as np
import json
import math
from typing import Dict, Any, List, Tuple, Optional
from collections import defaultdict

class SensorDataAnalyzer:
    
    def __init__(self):
        self.all_device_ids = {'40D63CD705BA', '40D63CD70316', '40D63CD702E8', '40D63CD6FD92', '40D63CD70406'}
        self.reference_coordinates_file_path = 'main_data/reference_coordinates_data.json'
        self.data_tree = {}
        self.last_data = {}

    def euclidean_distance(self, data1: Dict[str, Dict[str, float]], data2: Dict[str, float]) -> float:
        dist = 0.0
        for device_id in self.all_device_ids:
            avg1 = data1.get(device_id, {}).get("average", -90.0)
            avg2 = data2.get(device_id, -90.0)
            dist += (avg1 - avg2) ** 2
        return math.sqrt(dist)

    def find_most_similar_node(self, target_node: Dict[str, float]) -> Tuple[Optional[Dict[str, Any]], Optional[str], Optional[float], Optional[float]]:
        closest_node = None
        min_distance = float('inf')
        closest_location = None
        closest_x = None
        closest_y = None

        for location, loc_data in self.data_tree.items():
            for node in loc_data["children"]:
                distance = self.euclidean_distance(node["data"], target_node)
                if distance < min_distance:
                    min_distance = distance
                    closest_node = node
                    closest_location = location
                    
                    # Get x and y with default values if they are missing
                    closest_x = node["data"].get("x", 0.0)
                    closest_y = node["data"].get("y", 0.0)

        return closest_node, closest_location, closest_x, closest_y

    def transform_data(self, data: Dict[str, Dict[str, Dict[str, float]]]) -> Dict[str, Dict[str, float]]:
        transformed = {}
        
        for device_id, sensors_data in data.items():
            for sensor_id, rssi in sensors_data.items():
                if sensor_id not in transformed:
                    transformed[sensor_id] = {}
                transformed[sensor_id][device_id] = rssi.get("average", -90.0)
        
        for sensor_id, sensor_data in transformed.items():
            for device_id in self.all_device_ids:
                if device_id not in sensor_data:
                    sensor_data[device_id] = -85.0
        
        self.last_data = transformed
        
        return transformed

    def calculate_differences(self, data: Dict[str, Any]) -> Dict[str, Dict[str, Dict[str, Dict[str, float]]]]:
        coord_diffs = {}
        num_keys = list(self.all_device_ids)

        for location, loc_data in data.items():
            coord_diffs[location] = {"x": {}, "y": {}}
            objects = loc_data.get("children", [])

            # Extract unique x and y values
            x_values = sorted(set(obj["data"].get("x") for obj in objects if "x" in obj["data"]))
            y_values = sorted(set(obj["data"].get("y") for obj in objects if "y" in obj["data"]))

            # Calculate differences based on x coordinates
            for i in range(len(x_values) - 1):
                x1 = x_values[i]
                x2 = x_values[i + 1]
                if x1 != x2:
                    coord_diffs[location]["x"][(x1, x2)] = {}
                    for key in num_keys:
                        avg1 = next((obj["data"].get(key, {}).get("average", -90.0) for obj in objects if obj["data"].get("x") == x1), None)
                        avg2 = next((obj["data"].get(key, {}).get("average", -90.0) for obj in objects if obj["data"].get("x") == x2), None)
                        if avg1 is not None and avg2 is not None:
                            coord_diffs[location]["x"][(x1, x2)][key] = avg2 - avg1

            # Calculate differences based on y coordinates
            for i in range(len(y_values) - 1):
                y1 = y_values[i]
                y2 = y_values[i + 1]
                if y1 != y2:
                    coord_diffs[location]["y"][(y1, y2)] = {}
                    for key in num_keys:
                        avg1 = next((obj["data"].get(key, {}).get("average", -90.0) for obj in objects if obj["data"].get("y") == y1), None)
                        avg2 = next((obj["data"].get(key, {}).get("average", -90.0) for obj in objects if obj["data"].get("y") == y2), None)
                        if avg1 is not None and avg2 is not None:
                            coord_diffs[location]["y"][(y1, y2)][key] = avg2 - avg1

        return coord_diffs
    
    def set_tree(self):
        with open(self.reference_coordinates_file_path, 'r') as file:
            tree_data = json.load(file)
        
        tree = defaultdict(lambda: {"children": []})
        for key, value in tree_data.items():
            location = value.get("location")
            if location is None:
                print(f"Warning: No location found for key: {key}")
                continue
            
            node = {
                "name": key,
                "data": {
                    "40D63CD6FD92": value.get("40D63CD6FD92", {"average": -90.0}),
                    "40D63CD705BA": value.get("40D63CD705BA", {"average": -90.0}),
                    "40D63CD70406": value.get("40D63CD70406", {"average": -90.0}),
                    "40D63CD702E8": value.get("40D63CD702E8", {"average": -90.0}),
                    "40D63CD70316": value.get("40D63CD70316", {"average": -90.0}),
                    "x": value.get("x", 0),
                    "y": value.get("y", 0)
                }
            }
            tree[location]["children"].append(node)

        self.data_tree = self.dictify(tree)
        
        # Debugging: Print the final tree structure
        print("Final tree structure:")
        for location, loc_data in self.data_tree.items():
            print(f"Location: {location}, Number of children: {len(loc_data.get('children', []))}")

    def process_data(self, measurement_file_path: str):
        with open(measurement_file_path, 'r') as f:
            measurement_data = json.load(f)

        # Transform the measurement data
        transformed_data_distance = self.transform_data(measurement_data)

        # Define the bounds for x and y coordinates
        x_bounds = (0, 735)
        y_bounds = (0, 2070)

        # Find the most similar node for each sensor using distance
        print('Distance result')
        for sensor_id, sensor_data in transformed_data_distance.items():
            predicted_x, predicted_y = self.predict_coordinates(sensor_data, x_bounds, y_bounds)
            if predicted_x is None or predicted_y is None:
                print(f"No similar node found for sensor '{sensor_id}'.\n")
            else:
                print(f"Predicted coordinates for sensor '{sensor_id}': (x: {predicted_x}, y: {predicted_y})")

    def predict_coordinates(self, input_averages: Dict[str, float], x_bounds: Tuple[float, float], y_bounds: Tuple[float, float]) -> Tuple[Optional[float], Optional[float]]:
        # Find the most similar node
        closest_node, closest_location, closest_x, closest_y = self.find_most_similar_node(input_averages)
        
        if not closest_node:
            return None, None

        # Calculate differences
        coord_diffs = self.calculate_differences(self.data_tree)
        if closest_location not in coord_diffs:
            return None, None

        diffs = coord_diffs[closest_location]

        # Calculate average differences in x and y
        avg_x_diff = np.mean([val for diff in diffs["x"].values() for val in diff.values() if val is not None])
        avg_y_diff = np.mean([val for diff in diffs["y"].values() for val in diff.values() if val is not None])

        # Predict coordinates
        predicted_x = closest_x + avg_x_diff
        predicted_y = closest_y + avg_y_diff

        # Ensure predicted coordinates are within bounds
        predicted_x = f'{max(x_bounds[0], min(predicted_x, x_bounds[1])):.2f}'
        predicted_y = f'{max(y_bounds[0], min(predicted_y, y_bounds[1])):.2f}'

        return predicted_x, predicted_y

    def dictify(self, d: defaultdict) -> Dict:
        if isinstance(d, defaultdict):
            d = {k: self.dictify(v) for k, v in d.items()}
        return d

# if __name__ == "__main__":
#     analyzer = SensorDataAnalyzer()
#     analyzer.set_tree()
#     measurement_file_path = 'D:/project_mmp/measurement_data/240805_155000combined.json'
#     analyzer.process_data(measurement_file_path)
