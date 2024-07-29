import json

def fix_json(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        data = file.read()

    data = data.strip()
    data = data.replace('{}', '')

    json_objects = []
    balance = 0
    current_obj = ''

    for char in data:
        if char == '{':
            balance += 1
        if char == '}':
            balance -= 1
        
        current_obj += char
        
        if balance == 0 and current_obj:
            json_objects.append(current_obj)
            current_obj = ''
    
    parsed_objects = []
    for obj in json_objects:
        try:
            parsed_objects.append(json.loads(obj))
        except json.JSONDecodeError:
            continue

    output_path = file_path.replace('.json', '_fixed.json')
    with open(output_path, 'w', encoding='utf-8') as file:
        json.dump(parsed_objects, file, ensure_ascii=False, indent=4)

    print(f'Fixed JSON data has been saved to: {output_path}')

# Example usage
fix_json('measurement_data/240729_115100number.json')