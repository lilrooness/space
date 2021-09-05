from common.const import SLOT_AMMO_INFINITY
from common.entities.entity import Entity
from common.serializable.serializable import FIELD_TYPE_VALUE


class LootItem(Entity):

    def __init__(
            self,
            id=None,
            id_fun=None,
            type_id=0,
            ammo=SLOT_AMMO_INFINITY,
    ):
        super().__init__(id, id_fun)
        self.type_id = type_id
        self.ammo = ammo

    @classmethod
    def fields(cls):
        return {
            "id": (FIELD_TYPE_VALUE, int),
            "type_id": (FIELD_TYPE_VALUE, int),
            "ammo": (FIELD_TYPE_VALUE, int),
        }
