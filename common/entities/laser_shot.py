from common.entities.entity import Entity


class LaserShot(Entity):

    def __init__(self, shooter_ship_id, being_shot_ship_id, power, id=None, id_fun=None):
        super().__init__(id, id_fun)
        self.shooter_ship_id = shooter_ship_id
        self.being_shot_ship_id = being_shot_ship_id
        self.power = power

    @classmethod
    def marshalled_field_types(cls):
        return {
            "id": lambda id: int(id),
            "shooter_ship_id": lambda id: int(id),
            "being_shot_ship_id": lambda id: int(id),
            "power": lambda id: int(id),
        }

