import yaml

global_types = {}

def load_types():
    global loot_type_icons

    types = []
    with open('data/types.yaml') as file:
        types = yaml.safe_load(file)

    for type in types:
        global_types[type["type_id"]] = type["icon_path"]
