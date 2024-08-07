import numpy as np
import pytz

from datetime import datetime, timezone

# Load the JSON data from the file
 
kst = pytz.timezone('Asia/Seoul') 

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
                timestamp_values = [datetime.fromisoformat(reading['TimeStamp'][:-1]) for reading in readings]
                
                filtered_rssi = kalman_filter.kalman_filter(rssi_values)
                
                if gateway_mac not in self.filtered_data:
                    self.filtered_data[gateway_mac] = {}
                    
                self.filtered_data[gateway_mac][beacon_mac] = {
                    'FilteredRSSI': filtered_rssi,
                    'Timestamps': timestamp_values
                }

        result_data = self.stats_rssi_per_mac(self.filtered_data)
        
        return result_data     
    
    # Calculate the average and standard deviation of the filtered RSSI values for each MAC address   
    def stats_rssi_per_mac(self, data):  
        
        stats_rssi_per_mac = {}

        for gateway_mac, beacon_data in data.items():
            stats_rssi_per_mac[gateway_mac] = {}

            # Initialize variables to hold min/max timestamps and battvoltage
            min_timestamp = None
            max_timestamp = None

            for beacon_mac, rssi_data in beacon_data.items():
                # Extract timestamps and battvoltages from the filtered data
                timestamps = rssi_data["Timestamps"]

                # Calculate average and standard deviation of RSSI
                rssi_values = rssi_data['FilteredRSSI']
                average = np.mean(rssi_values)
                std_dev = np.std(rssi_values)
                
                     
                max_rssi = None
                min_rssi = None
                
                for rssi in rssi_values:
                    if average - std_dev <= rssi <= average + std_dev:
                        if max_rssi is None or rssi > max_rssi:
                            max_rssi = rssi
                        if min_rssi is None or rssi < min_rssi:
                            min_rssi = rssi
                # Determine min and max timestamp
                if min_timestamp is None or min(timestamps) < min_timestamp:
                    min_timestamp = min(timestamps)
                if max_timestamp is None or max(timestamps) > max_timestamp:
                    max_timestamp = max(timestamps)

                min_timestamp_utc = min_timestamp.replace(tzinfo=timezone.utc)
                max_timestamp_utc = max_timestamp.replace(tzinfo=timezone.utc)

                min_timestamp_kst = min_timestamp_utc.astimezone(kst)
                max_timestamp_kst = max_timestamp_utc.astimezone(kst)

                early_timestamp = min_timestamp_kst.isoformat()
                late_timestamp = max_timestamp_kst.isoformat()
                
                # Store statistics for current beacon_mac
                stats_rssi_per_mac[gateway_mac][beacon_mac] = {
                    "average": average,
                    "std_dev": std_dev,
                    "max_rssi": max_rssi,
                    "min_rssi": min_rssi,
                    "early_timestamp": early_timestamp,
                    "late_timestamp": late_timestamp
                }

        return stats_rssi_per_mac


################ test main code #################

# file_path = 'main_criterion_coordinate(-21,123)(21,123).json'        ### write your test measuring file path

# if __name__ == "__main__":
#     with open(file_path, 'r') as json_file:
#         json_data = json.load(json_file)
#     filter_instance = kalman_filter()
#     filtered_data = filter_instance.apply_kalman_filter_to_data(json_data)
#     print(filtered_data)