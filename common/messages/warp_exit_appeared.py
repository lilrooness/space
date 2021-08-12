from common.messages.message import Message
from common.serializable.serializable import FIELD_TYPE_VALUE


class WarpExitAppearedMessage(Message):

    MESSAGE_NAME = "warp_exit_appeared"

    def __init__(self, ticks_to_complete, x, y):
        self.ticks_to_complete = ticks_to_complete
        self.x = x
        self.y = y

    @classmethod
    def fields(cls):
        return {
            "ticks_to_complete": (FIELD_TYPE_VALUE, int),
            "x": (FIELD_TYPE_VALUE, float),
            "y": (FIELD_TYPE_VALUE, float),
        }

    def marshal(self):
        message = [
            WarpExitAppearedMessage.MESSAGE_NAME,
            "%d" % self.ticks_to_complete,
            "%d" % self.x,
            "%d" % self.y,
        ]

        return ":".join(message)

    @classmethod
    def unmarshal(cls, encoded):
        fields_map, _remaining = WarpExitAppearedMessage.message_unmarshal_fields_map(encoded)

        return WarpExitAppearedMessage(
            fields_map["ticks_to_complete"],
            fields_map["x"],
            fields_map["y"],
        )
