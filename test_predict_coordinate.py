import json
import math
import numpy as np

def load_data_from_file(filename):
    with open(filename, 'r') as file:
        return json.load(file)

def calculate_differences(data):
    coord_diffs = {}
    num_keys = ["40D63CD6FD92", "40D63CD705BA", "40D63CD70406", "40D63CD702E8", "40D63CD70316"]
    
    # Group by location
    locations = {}
    for key, obj in data.items():
        location = obj["location"]
        if location not in locations:
            locations[location] = []
        locations[location].append(obj)
    
    for location, objects in locations.items():
        coord_diffs[location] = {"x": {}, "y": {}}

        # Gather all unique x and y values for the current location
        x_values = sorted(set(obj["x"] for obj in objects))
        y_values = sorted(set(obj["y"] for obj in objects))

        # Compute differences for x coordinates
        for i in range(len(x_values) - 1):
            x1 = x_values[i]
            x2 = x_values[i + 1]
            if x1 != x2:
                coord_diffs[location]["x"][(x1, x2)] = {}
                for key in num_keys:
                    avg1 = next((obj[key]["average"] for obj in objects if obj["x"] == x1), None)
                    avg2 = next((obj[key]["average"] for obj in objects if obj["x"] == x2), None)
                    if avg1 is not None and avg2 is not None:
                        coord_diffs[location]["x"][(x1, x2)][key] = avg2 - avg1
        
        # Compute differences for y coordinates
        for i in range(len(y_values) - 1):
            y1 = y_values[i]
            y2 = y_values[i + 1]
            if y1 != y2:
                coord_diffs[location]["y"][(y1, y2)] = {}
                for key in num_keys:
                    avg1 = next((obj[key]["average"] for obj in objects if obj["y"] == y1), None)
                    avg2 = next((obj[key]["average"] for obj in objects if obj["y"] == y2), None)
                    if avg1 is not None and avg2 is not None:
                        coord_diffs[location]["y"][(y1, y2)][key] = avg2 - avg1
    
    return coord_diffs

def find_closest_point(data, input_averages):
    closest_point = None
    min_distance = float('inf')

    for point, values in data.items():
        point_averages = [
            values["40D63CD6FD92"]["average"],
            values["40D63CD705BA"]["average"],
            values["40D63CD70406"]["average"],
            values["40D63CD702E8"]["average"],
            values["40D63CD70316"]["average"]
        ]
        distance = calculate_distance(input_averages, point_averages)
        
        if distance < min_distance:
            min_distance = distance
            closest_point = point

    print(closest_point)
    
    if closest_point:
        location = data[closest_point]["location"]
        x = data[closest_point]["x"]
        y = data[closest_point]["y"]
        return location, x, y
    else:
        return None, None, None

def calculate_distance(avg1, avg2):
    return math.sqrt(sum((a - b) ** 2 for a, b in zip(avg1, avg2)))

def predict_coordinates(data, input_averages):
    location, x_closest, y_closest = find_closest_point(data, input_averages)
    
    if not location:
        return None, None

    coord_diffs = calculate_differences(data)
    if location not in coord_diffs:
        return None, None

    diffs = coord_diffs[location]

    # Calculate average differences in x and y
    avg_x_diff = np.mean([val for diff in diffs["x"].values() for val in diff.values() if val is not None])
    avg_y_diff = np.mean([val for diff in diffs["y"].values() for val in diff.values() if val is not None])

    # Assuming the input_averages is for point (x', y')
    # We will use the closest point (x_closest, y_closest) and differences to estimate (x', y')
    predicted_x = x_closest + avg_x_diff
    predicted_y = y_closest + avg_y_diff

    return predicted_x, predicted_y

def main():
    # File path to the JSON data
    filename = 'main_data/reference_coordinates_data.json'

    # Load data
    data = load_data_from_file(filename)
    
    # Example input averages
    input_averages = [-82.06, -83.75, -68.86, -59.13, -67.96]
    
    # Predict coordinates
    predicted_x, predicted_y = predict_coordinates(data, input_averages)
    
    if predicted_x is not None and predicted_y is not None:
        print(f"Predicted coordinates: x={predicted_x:.2f}, y={predicted_y:.2f}")
    else:
        print("Could not make a prediction.")

if __name__ == "__main__":
    main()
