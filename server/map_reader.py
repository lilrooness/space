from common.entities.crate import Crate
from common.entities.sensor_tower import SensorTower
from server.id import new_id

CRATE_MARKER = "CRATE"
SENSOR_TOWER_MARKER = "SENSOR_TOWER"

entity_markers = {
    "CRATE": Crate,
    "TOWER": SensorTower,
}

def read_map_data(filename):
    map = {
        SENSOR_TOWER_MARKER: [],
        CRATE_MARKER: [],
    }

    with open(filename) as map_file:
        lines = map_file.readlines()

        for line in lines:
            if line.startswith(CRATE_MARKER):
                npop = len(CRATE_MARKER)
                encoded_crate = line[npop:]
                crate = Crate.unmarshal(encoded_crate)
                crate.id = new_id()
                map[CRATE_MARKER].append(crate)
            elif line.startswith(SENSOR_TOWER_MARKER):
                npop = len(SENSOR_TOWER_MARKER)
                encoded_sensor_tower = line[npop:]
                sensor_tower = SensorTower.unmarshal(encoded_sensor_tower)
                sensor_tower.id = new_id()
                map[SENSOR_TOWER_MARKER].append(sensor_tower)

    return map
