from common.entities.entity import Entity
from common.serializable.serializable import FIELD_TYPE_VALUE


class Crate(Entity):

    def __init__(
            self,
            x=0,
            y=0,
            contents=None,
            id=None,
            id_fun=None,
            open=False
    ):
        super().__init__(id, id_fun)
        self.x = x
        self.y = y
        if contents is None:
            self.contents = {}
        else:
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

    def get(self, type_id):
        for _id, item in self.contents.items():
            if item.type_id == type_id:
                return item

        return None

    def remove(self, type_id):
        item = self.get(type_id)
        if item:
            del self.contents[item.id]