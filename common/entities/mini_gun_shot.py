from common.entities.entity import Entity
from common.serializable.serializable import FIELD_TYPE_VALUE


class MinigunShot(Entity):
    def __init__(self, shooter_ship_id, being_shot_ship_id, velocity, miss=False, id=None, id_fun=None):
        super().__init__(id, id_fun)
        self.shooter_ship_id = shooter_ship_id
        self.being_shot_ship_id = being_shot_ship_id
        self.velocity = velocity
        self.miss = miss
        self.resolved = False

    @classmethod
    def fields(cls):
        return {
            "shooter_ship_id": (FIELD_TYPE_VALUE, int),
            "being_shot_ship_id": (FIELD_TYPE_VALUE, int),
            "velocity": (FIELD_TYPE_VALUE, float),
            "miss": (FIELD_TYPE_VALUE, bool),
        }
