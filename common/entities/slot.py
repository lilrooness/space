from common.const import SLOT_AMMO_INFINITY
from common.entities.entity import Entity
from common.serializable.serializable import FIELD_TYPE_VALUE, FIELD_TYPE_MULTIPLE_VALUES

SHIELD_CONSTRAINT = 1
ENGINE_CONSTRAINT = 2
WEAPON_CONSTRAINT = 3
HULL_CONSTRAINT = 4

class Slot(Entity):

    def __init__(self, type_id=0, type_constraint=0, target_ids=None, ammo=SLOT_AMMO_INFINITY ,max_ammo=SLOT_AMMO_INFINITY,  id_fun=None, id=None):
        super().__init__(id=id, id_fun=id_fun)
        self.type_id = type_id
        self.type_constraint = type_constraint
        self.max_ammo = max_ammo
        self.ammo = ammo

        if target_ids is None:
            self.target_ids = []
        else:
            self.target_ids = target_ids

        self.userdata = {}

    @classmethod
    def fields(cls):
        return {
            "id": (FIELD_TYPE_VALUE, int),
            "type_id": (FIELD_TYPE_VALUE, int),
            "type_constraint": (FIELD_TYPE_VALUE, int),
            "target_ids": (FIELD_TYPE_MULTIPLE_VALUES, int),
            "max_ammo": (FIELD_TYPE_VALUE, int),
            "ammo": (FIELD_TYPE_VALUE, int),
        }
