from common.messages.message import Message, FIELD_TYPE_VALUE


class ShipDamageMessage(Message):
    MESSAGE_NAME = "ship_damage_message"

    def __init__(self, ship_id, damage, death=False):
        self.ship_id = ship_id
        self.damage = damage
        self.death = death

    @classmethod
    def fields(cls):
        return {
            "ship_id": (FIELD_TYPE_VALUE, int),
            "damage": (FIELD_TYPE_VALUE, int),
            "death": (FIELD_TYPE_VALUE, bool),
        }

    def marshal(self):
        message = [
            ShipDamageMessage.MESSAGE_NAME,
            "%d" % self.ship_id,
            "%d" % self.damage,
            "{}".format(self.death)
        ]

        return ":".join(message)

    @classmethod
    def unmarshal(cls, encoded):
        fields_map = ShipDamageMessage._unmarshal_fields_map(encoded)

        return ShipDamageMessage(
            fields_map["ship_id"],
            fields_map["damage"],
            fields_map["death"],
        )