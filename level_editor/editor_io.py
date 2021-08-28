import yaml

def read_map_file(filename):
    with open(filename) as map_file:
        map_data = yaml.safe_load(map_file)
        return map_data

def write_map_file(map_data, filename):
    with open(filename, 'w') as map_file:
        yaml.safe_dump(map_data, map_file)