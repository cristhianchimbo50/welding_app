import json

def load_materials():
    with open('data/materials.json', 'r') as file:
        return json.load(file)
