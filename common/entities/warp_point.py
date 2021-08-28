from common.const import WARP_POINT_RANGE
from common.entities.entity import Entity
from common.serializable.serializable import FIELD_TYPE_VALUE


class WarpPoint(Entity):
    def __init__(
            self,
             x=0,
             y=0,
             id_fun=None,
             id=None,
             range=WARP_POINT_RANGE,
    ):
        super().__init__(id, id_fun)
        self.x = x
        self.y = y
        self.range = range

    @classmethod
    def fields(cls):
        return {
            "id": (FIELD_TYPE_VALUE, int),
            "x": (FIELD_TYPE_VALUE, float),
            "y": (FIELD_TYPE_VALUE, float),
            "range": (FIELD_TYPE_VALUE, int),
        }
