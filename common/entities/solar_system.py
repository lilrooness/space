from common.entities.crate import Crate
from common.entities.entity import Entity
from common.entities.loot.lootitem import LootItem
from server.id import new_id


class SolarSystem(Entity):

    def __init__(self, ships={}, projectiles={}, active_laser_shots={}, id=None, id_fun=None):
        super().__init__(id=id, id_fun=id_fun)
        self.ships = ships
        self.projectiles = projectiles
        self.active_laser_shots = active_laser_shots
        crate = Crate(x=500, y=500, id_fun=new_id,  contents=[LootItem(id_fun=new_id)])
        self.crates = {
            crate.id: crate,
        }

    def tick(self, delta=1.0):
        for _id, ship in self.ships.items():
            ship.tick(delta=delta)
