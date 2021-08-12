from common.const import MINI_GUN, MISSILE_LAUNCHER
from common.entities.crate import Crate
from common.entities.entity import Entity
from common.entities.loot.lootitem import LootItem
from common.entities.sensor_tower import SensorTower
from server.id import new_id


class SolarSystem(Entity):

    def __init__(self, ships={}, projectiles={}, active_laser_shots={}, in_flight_missiles={}, mini_gun_shots={}, sensor_towers={}, id=None, id_fun=None):
        super().__init__(id=id, id_fun=id_fun)
        self.ships = ships
        self.projectiles = projectiles
        self.active_laser_shots = active_laser_shots
        self.in_flight_missiles = in_flight_missiles
        self.mini_gun_shots = mini_gun_shots
        self.sensor_towers = sensor_towers

        item_1 = LootItem(id_fun=new_id, type_id=MINI_GUN)
        crate_1 = Crate(x=250, y=250, id_fun=new_id,  contents={item_1.id: item_1})

        item_2 = LootItem(id_fun=new_id, type_id=MISSILE_LAUNCHER)
        crate_2 = Crate(x=250, y=50, id_fun=new_id,  contents={item_2.id: item_2})

        self.crates = {
            crate_1.id: crate_1,
            crate_2.id: crate_2,
        }

        tower_1 = SensorTower(
            x=50,
            y=100,
            id_fun=new_id,
        )
        self.sensor_towers = {
            tower_1.id: tower_1
        }

    def tick(self, delta=1.0, tick=None):
        for _id, ship in self.ships.items():
            ship.tick(delta=delta, currentTick=tick)

        for _id, missile in self.in_flight_missiles.items():
            missile.tick(self.ships, delta=delta)
