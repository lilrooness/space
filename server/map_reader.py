import yaml

from common.const import TOWER_TYPE_ID, CRATE_TYPE_ID, WARP_POINT_TYPE_ID
from common.entities.crate import Crate
from common.entities.sensor_tower import SensorTower
from common.entities.solar_system import SolarSystem
from common.entities.warp_point import WarpPoint
from server.id import new_id

CRATE_MARKER = "CRATE"
SENSOR_TOWER_MARKER = "SENSOR_TOWER"

entity_markers = {
    "CRATE": Crate,
    "TOWER": SensorTower,
}

def read_map_data(filename):
    sensor_towers = {}
    crates = {}
    warp_points = {}
    with open(filename) as map_file:
        map_data = yaml.safe_load(map_file)

    for type_id, coords in map_data.items():
        for coord in coords:
            if type_id == TOWER_TYPE_ID:
                tower = SensorTower(x=coord[0], y=coord[1], id_fun=new_id)
                sensor_towers[tower.id] = tower
            elif type_id == CRATE_TYPE_ID:
                crate = Crate(x=coord[0], y=coord[1], id_fun=new_id)
                crates[crate.id] = crate
            elif type_id == WARP_POINT_TYPE_ID:
                warp_point = WarpPoint(x=coord[0], y=coord[1], id_fun=new_id)
                warp_points[warp_point.id] = warp_point

    return SolarSystem(
        sensor_towers=sensor_towers,
        warp_points=warp_points,
        crates=crates,
    )

