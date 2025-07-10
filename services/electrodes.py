import json

def load_electrodes():
    with open('data/electrodes.json', 'r', encoding='utf-8') as file:
        return json.load(file)
