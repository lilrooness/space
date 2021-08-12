from common.entities.entity import Entity
from common.serializable.serializable import FIELD_TYPE_VALUE

ACTIVATION_TICK_AMOUNT = 0.002

class SensorTower(Entity):

    def __init__(
            self,
            x=0,
            y=0,
            id_fun=None,
            id=None,
            last_charged_by=-1,
            connected_ship_id=-1,
            percent_activated=0.0,
            connection_range=400,
            online=False,
    ):
        super().__init__(id, id_fun)
        self.x = x
        self.y = y
        self.last_charged_by = last_charged_by
        self.percent_activated = percent_activated
        self.connected_ship_id = connected_ship_id
        self.connection_range = connection_range
        self.online = online

    @classmethod
    def fields(cls):
        return {
            "id": (FIELD_TYPE_VALUE, int),
            "x": (FIELD_TYPE_VALUE, float),
            "y": (FIELD_TYPE_VALUE, float),
            "percent_activated": (FIELD_TYPE_VALUE, float),
            "connection_range": (FIELD_TYPE_VALUE, float),
            "online": (FIELD_TYPE_VALUE, bool),
        }


