import json
import numpy as np

# Load the JSON data from the file
file_path = 'reft_main_centerYdata.json'
with open(file_path, 'r', encoding='utf-8') as file:
    data = json.load(file)

# Function to apply a simple Kalman Filter on RSSI values
def apply_kalman_filter(rssi_values):
    # Kalman filter parameters
    initial_state = rssi_values[0]
    estimate_uncertainty = 5.0
    process_noise = 0.5
    measurement_noise = 5.0
    kalman_gain = estimate_uncertainty / (estimate_uncertainty + measurement_noise)
    
    # Initial estimate
    estimates = [initial_state]
    current_estimate = initial_state
    
    for rssi in rssi_values[1:]:
        # Prediction update
        prediction_estimate = current_estimate
        prediction_uncertainty = estimate_uncertainty + process_noise
        
        # Measurement update
        kalman_gain = prediction_uncertainty / (prediction_uncertainty + measurement_noise)
        current_estimate = prediction_estimate + kalman_gain * (rssi - prediction_estimate)
        estimate_uncertainty = (1 - kalman_gain) * prediction_uncertainty
        
        estimates.append(current_estimate)
    
    return estimates

# Apply Kalman filter to RSSI data of each MAC address
filtered_data = {}
for mac, readings in data.items():
    rssi_values = [reading['rssi'] for reading in readings]
    filtered_rssi = apply_kalman_filter(rssi_values)
    filtered_data[mac] = filtered_rssi

# Calculate the average and standard deviation of the filtered RSSI values for each MAC address
stats_rssi_per_mac = {}
for mac, rssi in filtered_data.items():
    average = np.mean(rssi)
    std_dev = np.std(rssi)
    max_rssi = average + std_dev
    min_rssi = average - std_dev
    stats_rssi_per_mac[mac] = {
        "average": average,
        "std_dev": std_dev,
        "max_rssi": max_rssi,
        "min_rssi": min_rssi
    }

print(stats_rssi_per_mac)
