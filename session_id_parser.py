import json

def extract_value_from_json_file():
    file_path = 'cookies.json'
    with open(file_path, 'r') as file:
        data = json.load(file)
        for key, value in data.items():
            if "prod" in value and "api" in value:
                return value
