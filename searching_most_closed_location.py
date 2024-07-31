import json
import math
from collections import defaultdict
from typing import Dict, Any, List, Tuple, Optional

class SensorDataAnalyzer:
    def __init__(self):
        # Initialize the class with a set of all device IDs
        self.all_device_ids = {'40D6CD705BA', '40D63CD70316', '40D63CD702E8', '40D63CD6FD92', '40D63CD70406'}
        self.reference_coordinates_file_path = 'main_data/reference_coordinates_data.json'
        self.last_data = {}
        
    
    def euclidean_distance(self, data1: Dict[str, Dict[str, float]], data2: Dict[str, Dict[str, float]]) -> float:
        dist = 0.0
        
        for device_id in self.all_device_ids:
            avg1 = data1.get(device_id, {}).get("average", -90.0)
            avg2 = data2.get(device_id, {}).get("average", -90.0)
            
            dist += (avg1 - avg2) ** 2
        
        return math.sqrt(dist)

    def find_most_similar_node_distance(self, tree: Dict[str, Any], target_node: Dict[str, Any]) -> Tuple[Optional[Dict[str, Any]], Optional[str]]:
        closest_node = None
        min_distance = float('inf')
        closest_location = None

        for location, loc_data in tree.items():
            for node in loc_data["children"]:
                distance = self.euclidean_distance(node["data"], target_node["data"])
                if distance < min_distance:
                    min_distance = distance
                    closest_node = node
                    closest_location = location

        return closest_node, closest_location

    def transform_data(self, data: Dict[str, Dict[str, Dict[str, float]]]):
        transformed = {}
        
        for device_id, sensors in data.items():
            # Iterate over each sensor within the device
            for sensor_id, stats in sensors.items():
                # Initialize the sensor_id in the transformed dictionary if not already present
                if sensor_id not in transformed:
                    transformed[sensor_id] = {"data": {}}
                
                # Assign the average value for the sensor_id under the corresponding device_id
                transformed[sensor_id]["data"][device_id] = {"average": stats.get("average", -85.0)}

        # Ensure all device IDs are present for each sensor ID
        for sensor_id, sensor_data in transformed.items():
            for device_id in self.all_device_ids:
                if device_id not in sensor_data["data"]:
                    sensor_data["data"][device_id] = {"average": -85.0}
        
        self.last_data = transformed
        
        return transformed
    
    def process_data(self, measurement_file_path: str):
        # Load the reference coordinates data
        with open(self.reference_coordinates_file_path, 'r') as file:
            tree_data = json.load(file)

        # Initialize the tree structure using defaultdict
        tree = defaultdict(lambda: {"children": []})

        # Build the tree structure
        for key, value in tree_data.items():
            location = value["location"]
            node = {
                "name": key,
                "data": {
                    "40D63CD6FD92": value.get("40D63CD6FD92"),
                    "40D63CD705BA": value.get("40D63CD705BA"),
                    "40D63CD70406": value.get("40D63CD70406"),
                    "40D63CD702E8": value.get("40D63CD702E8"),
                    "40D63CD70316": value.get("40D63CD70316"),
                    "x": value.get("x"),
                    "y": value.get("y")
                }
            }
            tree[location]["children"].append(node)

        final_tree = self.dictify(tree)

        # Load measurement data
        with open(measurement_file_path, 'r') as f:
            measurement_data = json.load(f)

        # Transform the measurement data
        transformed_data_distance = self.transform_data(measurement_data)

        # Find the most similar node for each sensor using distance
        print('Distance result')
        for sensor_id, sensor_data in transformed_data_distance.items():
            most_similar_node, most_similar_location = self.find_most_similar_node_distance(final_tree, sensor_data)
            if most_similar_node:
                print(f"Most similar node for sensor '{sensor_id}':")
                print(f"Location: {most_similar_location}")
                print(f"Node: {most_similar_node['name']}")
            else:
                print(f"No similar node found for sensor '{sensor_id}'.\n")

    def dictify(self, d: defaultdict) -> Dict:
        if isinstance(d, defaultdict):
            d = {k: self.dictify(v) for k, v in d.items()}
        return d
    


################## test main code #################
    
if __name__ == "__main__":
    analyzer = SensorDataAnalyzer()
    analyzer.process_data('measurement_data/240731_095600combined.json')