from common.entities.entity import Entity
from common.serializable.serializable import FIELD_TYPE_VALUE

SHIELD_CONSTRAINT = 1
ENGINE_CONSTRAINT = 2
WEAPON_CONSTRAINT = 3
HULL_CONSTRAINT = 4

class Slot(Entity):

    def __init__(self, type_id=0, type_constraint=0, id_fun=None):
        super().__init__(id=None, id_fun=id_fun)
        self.type_id = type_id
        self.type_constraint = type_constraint

    @classmethod
    def fields(cls):
        return {
            "type_id": (FIELD_TYPE_VALUE, int),
            "type_constraint": (FIELD_TYPE_VALUE, int),
        }
