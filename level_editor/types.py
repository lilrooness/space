import yaml

types = {}

TOWER_TYPE_ID = -1
CRATE_TYPE_ID = -2
WARP_POINT_TYPE_ID = -3
SPAWN_POINT_TYPE_ID = -4
SPEED_BOOST_CLOUD_TYPE_ID = -5

def load_types():
    global types
    _types = []
    with open('data/types.yaml') as file:
        _types = yaml.safe_load(file)

    for type in _types:
        type_id = type["type_id"]
        del type["type_id"]
        types[type_id] = type
