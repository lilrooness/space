from common.entities.entity import Entity
from common.serializable.serializable import FIELD_TYPE_VALUE, FIELD_TYPE_MULTIPLE_VALUES

SHIELD_CONSTRAINT = 1
ENGINE_CONSTRAINT = 2
WEAPON_CONSTRAINT = 3
HULL_CONSTRAINT = 4

class Slot(Entity):

    def __init__(self, type_id=0, type_constraint=0, target_ids=[], id_fun=None, id=None):
        super().__init__(id=id, id_fun=id_fun)
        self.type_id = type_id
        self.type_constraint = type_constraint
        self.target_ids = target_ids
        self.userdata = {}

    @classmethod
    def fields(cls):
        return {
            "id": (FIELD_TYPE_VALUE, int),
            "type_id": (FIELD_TYPE_VALUE, int),
            "type_constraint": (FIELD_TYPE_VALUE, int),
            "target_ids": (FIELD_TYPE_MULTIPLE_VALUES, int),
        }
