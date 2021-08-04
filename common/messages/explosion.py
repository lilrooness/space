from common.messages.message import Message
from common.serializable.serializable import FIELD_TYPE_VALUE


class ExplosionMessage(Message):
    MESSAGE_NAME = "explosion_message"

    def __init__(self, x, y, radius):
        self.x = x
        self.y = y
        self.radius = radius

    @classmethod
    def fields(cls):
        return {
            "x": (FIELD_TYPE_VALUE, float),
            "y": (FIELD_TYPE_VALUE, float),
            "radius": (FIELD_TYPE_VALUE, float),
        }

    def marshal(self):
        message = [
            ExplosionMessage.MESSAGE_NAME,
            "%d" % self.x,
            "%d" % self.y,
            "%d" % self.radius,
        ]

        return ":".join(message)

    @classmethod
    def unmarshal(cls, encoded):
        fields_map, _remaining = ExplosionMessage.message_unmarshal_fields_map(encoded)

        return ExplosionMessage(
            fields_map["x"],
            fields_map["y"],
            fields_map["radius"],
        )
