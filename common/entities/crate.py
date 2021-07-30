from common.entities.entity import Entity
from common.serializable.serializable import FIELD_TYPE_VALUE


class Crate(Entity):

    def __init__(
            self,
            x=0,
            y=0,
            contents=[],
            id=None,
            id_fun=None,
            open=False
    ):
        super().__init__(id, id_fun)
        self.x = x
        self.y = y
        self.contents = contents
        self.open = open

    @classmethod
    def fields(cls):
        return {
            "id": (FIELD_TYPE_VALUE, int),
            "x": (FIELD_TYPE_VALUE, float),
            "y": (FIELD_TYPE_VALUE, float),
            "open": (FIELD_TYPE_VALUE, bool),
        }
