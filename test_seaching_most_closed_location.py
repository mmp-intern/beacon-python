import json
import math
from collections import defaultdict
from typing import Dict, Any, List, Optional

# Path to your JSON file
file_path = 'main_data\\reference_coordinates_data.json'

# Convert JSON file to dictionary
with open(file_path, 'r') as file:
    data_dict = json.load(file)

# Initialize the tree structure using defaultdict
tree = defaultdict(lambda: {"children": []})

# Build the tree structure
for key, value in data_dict.items():
    location = value["location"]
    node = {
        "name": key,
        "data": {
            "number1": value["number1"],
            "number2": value["number2"],
            "number3": value["number3"],
            "number4": value["number4"],
            "number5": value["number5"],
            "x": value["x"],
            "y": value["y"]
        }
    }
    # Add node to the corresponding location in the tree
    tree[location]["children"].append(node)

# Convert defaultdict to a regular dict for nicer output
def dictify(d):
    """Convert defaultdict to dict."""
    if isinstance(d, defaultdict):
        d = {k: dictify(v) for k, v in d.items()}
    return d

# Final tree structure
final_tree = dictify(tree)

def euclidean_distance(data1: Dict[str, Any], data2: Dict[str, Any]) -> float:
    """Calculate the Euclidean distance between two nodes based on their numerical attributes and coordinates."""
    dist = 0.0
    for number in ["number1", "number2", "number3", "number4", "number5"]:
        dist += (data1[number]["average"] - data2[number]["average"]) ** 2
    if "x" in data1 and "x" in data2 and "y" in data1 and "y" in data2:
        dist += (data1["x"] - data2["x"]) ** 2
        dist += (data1["y"] - data2["y"]) ** 2
    return math.sqrt(dist)

def find_most_similar_node(tree: Dict[str, Any], target_node: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    """Find the most similar node to the target_node based on Euclidean distance."""
    closest_node = None
    min_distance = float('inf')
    closest_location = None
    
    # Iterate through all locations in the tree
    for location, loc_data in tree.items():
        # Iterate through all nodes in the location
        for node in loc_data["children"]:
            distance = euclidean_distance(node["data"], target_node["data"])
            if distance < min_distance:
                min_distance = distance
                closest_node = node
                closest_location = location
    
    return closest_node, closest_location

def print_sorted_nodes_by_similarity(tree: Dict[str, Any], location: str, target_node: Dict[str, Any]):
    """Print nodes in the given location sorted by their similarity to the target_node."""
    if location in tree:
        nodes = tree[location]["children"]
        # Calculate similarity for each node and sort by similarity
        nodes_with_distance = []
        for node in nodes:
            distance = euclidean_distance(node["data"], target_node["data"])
            nodes_with_distance.append((node, distance))
        
        # Sort nodes by distance
        nodes_with_distance.sort(key=lambda x: x[1])
        
        print(f"\nNodes with the same parent ('{location}') sorted by similarity to target node:")
        for node, distance in nodes_with_distance:
            print(f"- {node['name']}: {node['data']}, Distance: {distance:.2f}")
    else:
        print(f"No nodes found with the location '{location}'.")

# Example usage

if __name__ == "__main__":
    # Define the target node to compare against
    target_node = {
        "name": "target_node_name",
        "data": {
            "number1": {"average": -85.0},
            "number2": {"average": -86.0},
            "number3": {"average": -70.0},
            "number4": {"average": -65.0},
            "number5": {"average": -60.0},
            # Note: No 'x' and 'y' values in the target node
        }
    }
    
    # Find the most similar node
    most_similar_node, most_similar_location = find_most_similar_node(final_tree, target_node)
    
    # Print the result
    import pprint
    print(f"Most similar node to '{target_node['name']}':")
    pprint.pprint(most_similar_node)
    
    # Print nodes with the same parent sorted by similarity
    if most_similar_location:
        print_sorted_nodes_by_similarity(final_tree, most_similar_location, target_node)
