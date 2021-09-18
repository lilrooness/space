from common.entities.entity import Entity
from common.serializable.serializable import FIELD_TYPE_VALUE


class SpeedBoostCloud(Entity):

    def __init__(
            self,
            x=0,
            y=0,
            id_fun=None,
            id=None,

    ):
        super().__init__(id, id_fun)
        self.x = x
        self.y = y

    @classmethod
    def fields(self):
        return {
            "id": (FIELD_TYPE_VALUE, int),
            "x": (FIELD_TYPE_VALUE, float),
            "y": (FIELD_TYPE_VALUE, float),
        }
