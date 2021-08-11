from common.messages.message import Message
from common.serializable.serializable import FIELD_TYPE_VALUE


class WarpStartedMessage(Message):

    MESSAGE_NAME = "warp_started_message"

    def __init__(self, ship_id, ticks_to_complete, destination_x=None, destination_y=None):
        self.ship_id = ship_id
        self.ticks_to_complete = ticks_to_complete
        self.destination_x = destination_x
        self.destination_y = destination_y

    @classmethod
    def fields(cls):
        return {
            "ship_id": (FIELD_TYPE_VALUE, int),
            "ticks_to_complete": (FIELD_TYPE_VALUE, int),
            "destination_x": (FIELD_TYPE_VALUE, float),
            "destination_y": (FIELD_TYPE_VALUE, float),
        }

    def marshal(self):
        message = [
            WarpStartedMessage.MESSAGE_NAME,
            "%d" % self.ship_id,
            "%d" % self.ticks_to_complete,
            "%d" % self.destination_x,
            "%d" % self.destination_y,
        ]

        return ":".join(message)

    @classmethod
    def unmarshal(cls, encoded):
        fields_map, _remaining = WarpStartedMessage.message_unmarshal_fields_map(encoded)

        return WarpStartedMessage(
            fields_map["ship_id"],
            fields_map["ticks_to_complete"],
            fields_map["destination_x"],
            fields_map["destination_y"],
        )
