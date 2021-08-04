from common.const import MISSILE_LAUNCHER
from common.entities.crate import Crate
from common.entities.entity import Entity
from common.entities.loot.lootitem import LootItem
from server.id import new_id


class SolarSystem(Entity):

    def __init__(self, ships={}, projectiles={}, active_laser_shots={}, in_flight_missiles={}, id=None, id_fun=None):
        super().__init__(id=id, id_fun=id_fun)
        self.ships = ships
        self.projectiles = projectiles
        self.active_laser_shots = active_laser_shots
        self.in_flight_missiles = in_flight_missiles
        item = LootItem(id_fun=new_id, type_id=MISSILE_LAUNCHER)
        crate = Crate(x=250, y=250, id_fun=new_id,  contents={item.id: item})
        self.crates = {
            crate.id: crate,
        }

    def tick(self, delta=1.0):
        for _id, ship in self.ships.items():
            ship.tick(delta=delta)

        for _id, missile in self.in_flight_missiles.items():
            missile.tick(self.ships, delta=delta)
