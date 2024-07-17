import json
import numpy as np

# Load the JSON data from the file
 
class kalman_filter:
    def __init__(self):
        self.filtered_data = {}

    # Function to apply a simple Kalman Filter on RSSI values
    def kalman_filter(rssi_values):
        if not rssi_values:
            raise ValueError("RSSI values are empty or None.")
        
        # Kalman filter parameters
        initial_state = rssi_values[0]
        estimate_uncertainty = 5.0
        process_noise = 0.5
        measurement_noise = 5.0
        kalman_gain = estimate_uncertainty / (estimate_uncertainty + measurement_noise)
        
        # Initial estimate
        estimates = [initial_state]
        current_estimate = initial_state
        
        try:
            for rssi in rssi_values[1:]:
                # Prediction update
                prediction_estimate = current_estimate
                prediction_uncertainty = estimate_uncertainty + process_noise
                
                # Measurement update
                kalman_gain = prediction_uncertainty / (prediction_uncertainty + measurement_noise)
                current_estimate = prediction_estimate + kalman_gain * (rssi - prediction_estimate)
                estimate_uncertainty = (1 - kalman_gain) * prediction_uncertainty
                
                estimates.append(current_estimate)
        except IndexError as e:
            print(f"IndexError occurred: {e}. Check your input data.")
        
        return estimates

    # Apply Kalman filter to RSSI data of each MAC address
    def apply_kalman_filter_to_data(self, data):
        
        for gateway_mac, beacon_macs in data.items():
            for beacon_mac, readings in beacon_macs.items():
                rssi_values = [reading['RSSI'] for reading in readings]
                filtered_rssi = kalman_filter.kalman_filter(rssi_values)
                if gateway_mac not in self.filtered_data:
                    self.filtered_data[gateway_mac] = {}
                self.filtered_data[gateway_mac][beacon_mac] = filtered_rssi

        result_data = self.stats_rssi_per_mac(self.filtered_data)
        
        return result_data
    
    # Calculate the average and standard deviation of the filtered RSSI values for each MAC address   
    def stats_rssi_per_mac(self, data):  
              
        stats_rssi_per_mac = {}
        
        for gateway_mac, beacon_data in data.items():
            stats_rssi_per_mac[gateway_mac] = {}
            for beacon_mac, rssi in beacon_data.items():
                average = np.mean(rssi)
                std_dev = np.std(rssi)
                max_rssi = average + std_dev
                min_rssi = average - std_dev
                stats_rssi_per_mac[gateway_mac][beacon_mac] = {
                    "average": average,
                    "std_dev": std_dev,
                    "max_rssi": max_rssi,
                    "min_rssi": min_rssi
                }

        return stats_rssi_per_mac


################# test main code #################

# file_path = 'measurement_data\\240717_091757_rssi(far_gateway).json'        ### write your test measuring file path
# with open(file_path, 'r') as json_file:
#     json_data = json.load(json_file)
   

# if __name__ == "__main__":
#     filter_instance = kalman_filter()
#     filtered_data = filter_instance.apply_kalman_filter_to_data(json_data)
#     print(filtered_data)