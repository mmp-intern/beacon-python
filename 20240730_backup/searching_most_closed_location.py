import json
import math
from collections import defaultdict
from typing import Dict, Any, List, Tuple, Optional

class SensorDataAnalyzer:
    def __init__(self):
        # Initialize the class with a set of all device IDs
        self.all_device_ids = {'40D63CD705BA', '40D63CD70316', '40D63CD702E8', '40D63CD6FD92', '40D63CD70406'}
    
    def euclidean_distance(self, data1: Dict[str, Dict[str, float]], data2: Dict[str, Dict[str, float]]) -> float:
        dist = 0.0
        
        for device_id in self.all_device_ids:
            avg1 = data1.get(device_id, {}).get("average", -85.0)
            avg2 = data2.get(device_id, {}).get("average", -85.0)
            
            dist += (avg1 - avg2) ** 2
        
        return math.sqrt(dist)

    def find_most_similar_node(self, tree: Dict[str, Any], target_node: Dict[str, Any]) -> Tuple[Optional[Dict[str, Any]], Optional[str]]:
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

    # def transform_data(self, data: List[Dict[str, Any]]) -> Dict[str, Dict[str, float]]:
    #     transformed = {}
        
    #     for device in data:
    #         for device_id, sensors in device.items():
    #             for sensor_id, stats in sensors.items():
    #                 if sensor_id not in transformed:
    #                     transformed[sensor_id] = {"data": {}}
                    
    #                 transformed[sensor_id]["data"][device_id] = {"average": stats.get("average", -85.0)}

    #     # Ensure all device IDs are present for each sensor ID
    #     for sensor_id, sensor_data in transformed.items():
    #         for device_id in self.all_device_ids:
    #             if device_id not in sensor_data["data"]:
    #                 sensor_data["data"][device_id] = {"average": -85.0}
        
    #     return transformed
    
    def transform_data(self, data: List[Dict[str, Any]]) -> Dict[str, Dict[str, float]]:
        transformed = {}
        
        for device in data:
            if not isinstance(device, dict):
                raise ValueError("Each item in the data list should be a dictionary.")
            
            for device_id, sensors in device.items():
                if not isinstance(sensors, dict):
                    raise ValueError(f"Expected sensors to be a dictionary for device_id: {device_id}")
                
                for sensor_id, stats in sensors.items():
                    if not isinstance(stats, dict):
                        raise ValueError(f"Expected stats to be a dictionary for sensor_id: {sensor_id}")
                    
                    if sensor_id not in transformed:
                        transformed[sensor_id] = {"data": {}}
                    
                    transformed[sensor_id]["data"][device_id] = {"average": stats.get("average", -85.0)}

        # Ensure all device IDs are present for each sensor ID
        for sensor_id, sensor_data in transformed.items():
            for device_id in self.all_device_ids:
                if device_id not in sensor_data["data"]:
                    sensor_data["data"][device_id] = {"average": -85.0}
        
        return transformed
    
def dictify(d):
    if isinstance(d, defaultdict):
        d = {k: dictify(v) for k, v in d.items()}
    return d


# Example usage:
if __name__ == "__main__":

    # Initialize the class with the device IDs
    analyzer = SensorDataAnalyzer()
    
    # Load the reference coordinates data
    with open('main_data/reference_coordinates_data.json', 'r') as file:
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
    
    final_tree = dictify(tree)
    
    # Load measurement data
    with open('D:/project_mmp/measurement_data/240730_153900combined.json', 'r') as f:
        measurement_data = json.load(f)
    
    # Transform the measurement data
    transformed_data = analyzer.transform_data(measurement_data)
    
    # Find the most similar node for each sensor
    for sensor_id, sensor_data in transformed_data.items():
        target_sensor_data = sensor_data["data"]
        
        most_similar_node, most_similar_location = analyzer.find_most_similar_node(final_tree, sensor_data)
        
        if most_similar_node:
            print(f"Most similar node for sensor '{sensor_id}':")
            print(f"Location: {most_similar_location}")
            print(f"Node: {most_similar_node['name']}")
            print(f"Distance: {analyzer.euclidean_distance(most_similar_node['data'], sensor_data['data']):.2f}\n")
        else:
            print(f"No similar node found for sensor '{sensor_id}'.\n")