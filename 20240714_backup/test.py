import json
import os


def extract_and_combine_data(input_files, output_file):
    combined_data = {}

    for input_file in input_files:
        if not os.path.isfile(input_file):
            print(f"File not found: {input_file}")
            continue

        with open(input_file, 'r') as infile:
            data = json.load(infile)

        for color, details in data.items():
            if color not in combined_data:
                combined_data[color] = {}

            for number_key, number_info in details.items():
                if isinstance(number_info, dict):
                    if 'average' in number_info:
                        # Save average values
                        combined_data[color][number_key] = {
                            'average': number_info['average']
                        }

            # Add x, y, and part if available
            if 'x' in details:
                combined_data[color]['x'] = details['x']
            if 'y' in details:
                combined_data[color]['y'] = details['y']
            if 'part' in details:
                combined_data[color]['part'] = details['part']

    with open(output_file, 'w') as outfile:
        json.dump(combined_data, outfile, indent=4)

# List of JSON files to combine
input_files = ['main_data\\reference_coordinates_data_to_filter(1).json', 
               'main_data\\reference_coordinates_data_to_filter(2).json',
               'main_data\\reference_coordinates_data_to_filter(3).json',
               'main_data\\reference_coordinates_data_to_filter(4).json',
               'main_data\\reference_coordinates_data_to_filter(5).json',
               'main_data\\reference_coordinates_data_to_filter(6).json',
               'main_data\\reference_coordinates_data_to_filter(7).json',
               'main_data\\reference_coordinates_data_to_filter(8).json',
               'main_data\\reference_coordinates_data_to_filter(9).json',
               'main_data\\reference_coordinates_data_to_filter(10).json',
               'main_data\\reference_coordinates_data_to_filter(11).json',
               'main_data\\reference_coordinates_data_to_filter(12).json'
               ]  # Add your file names here

output_file = 'combined_data.json'  # Replace with your desired output file name

extract_and_combine_data(input_files, output_file)
