import yaml

types = {}

def load_types():
    global types
    _types = []
    with open('data/types.yaml') as file:
        _types = yaml.safe_load(file)

    for type in _types:
        type_id = type["type_id"]
        del type["type_id"]
        types[type_id] = type
