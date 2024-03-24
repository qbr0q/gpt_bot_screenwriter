import json

def get_json_data(file_name: str) -> dict:
    with open(file_name, encoding='utf-8') as data:
        return json.loads(data.read())

def save_json_data(data: dict,
                   file_name: str) -> None:
    with open(file_name, 'w', encoding='utf-8') as dt:
        json.dump(data, dt)