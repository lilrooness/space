from common.entities.entity import Entity


class SolarSystem(Entity):

    def __init__(self, ships={}, projectiles={}, active_laser_shots={}, id=None, id_fun=None):
        super().__init__(id=id, id_fun=id_fun)
        self.ships = ships
        self.projectiles = projectiles
        self.active_laser_shots = active_laser_shots

    def tick(self, delta=1.0):
        for _id, ship in self.ships.items():
            ship.tick(delta=delta)
