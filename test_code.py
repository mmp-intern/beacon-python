# import os
# import json
# from datetime import datetime
# class handling_json_file:
#     def __init__(self):
#         self.base_filename = datetime.now().strftime("%y%m%d_%H%M00")
#         self.count = 5
#         self.directory = 'D:/project_mmp/measurement_data'

#     def combine_json_files(self):
#         self.base_filename = datetime.now().strftime("%y%m%d_%H%M00")
#         if datetime.now().second == 10:
#             combine_file_path = os.path.join(self.directory, f"{self.base_filename}combined.json")
#             combined_data = {}

#             # Check if all files exist
#             all_files_exist = True
#             file_paths = [os.path.join(self.directory, f"{self.base_filename}number{i}.json") for i in range(1, self.count + 1)]
            
#             for file_path in file_paths:
#                 if not os.path.exists(file_path):
#                     all_files_exist = False

#             if not all_files_exist:
#                 return

#             # If the combined file already exists, read its content
#             if os.path.exists(combine_file_path):
#                 with open(combine_file_path, 'r') as f:
#                     combined_data = json.load(f)
#                 print(f"Existing combined data loaded from {combine_file_path}")
            
#             # Read and combine data from existing files
#             for file_path in file_paths:
#                 with open(file_path, 'r') as f:
#                     data = json.load(f)
#                     combined_data.update(data)  # Merge data into combined_data

#             # Write the combined data to the combined file
#             try:
#                 with open(combine_file_path, 'w') as new_file:
#                     json.dump(combined_data, new_file, indent=4)
#                 print(f"Combined data saved to {combine_file_path}")

#                 # After successfully saving the combined data, delete the original files
#                 for file_path in file_paths:
#                     if os.path.exists(file_path):
#                         os.remove(file_path)
#                         print(f"Deleted {file_path}")

#             except IOError as e:
#                 print(f"An error occurred while saving the combined file: {e}")

import os
import json
from datetime import datetime
class handling_json_file:
    def __init__(self):
        self.base_filename = datetime.now().strftime("%y%m%d_%H%M00")
        self.count = 5
        self.directory = 'D:/project_mmp/measurement_data'

    def combine_json_files(self):
        self.base_filename = datetime.now().strftime("%y%m%d_%H%M00")
        if datetime.now().second == 10:
            combine_file_path = os.path.join(self.directory, f"{self.base_filename}combined.json")
            combined_data = {}

            # Check if all files exist
            all_files_exist = True
            file_paths = [os.path.join(self.directory, f"{self.base_filename}number{i}.json") for i in range(1, self.count + 1)]
            
            for file_path in file_paths:
                if not os.path.exists(file_path):
                    all_files_exist = False

            if not all_files_exist:
                return

            # If the combined file already exists, read its content
            if os.path.exists(combine_file_path):
                with open(combine_file_path, 'r') as f:
                    combined_data = json.load(f)
                print(f"Existing combined data loaded from {combine_file_path}")
            
            # Read and combine data from existing files
            for file_path in file_paths:
                with open(file_path, 'r') as f:
                    data = json.load(f)
                    combined_data.update(data)  # Merge data into combined_data

            # Write the combined data to the combined file
            try:
                with open(combine_file_path, 'w') as new_file:
                    json.dump(combined_data, new_file, indent=4)
                print(f"Combined data saved to {combine_file_path}")

                # After successfully saving the combined data, delete the original files
                for file_path in file_paths:
                    if os.path.exists(file_path):
                        os.remove(file_path)
                        print(f"Deleted {file_path}")

            except IOError as e:
                print(f"An error occurred while saving the combined file: {e}")