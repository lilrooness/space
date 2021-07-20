from common.messages.message import FIELD_TYPE_MULTIPLE_SHIPS, FIELD_TYPE_VALUE, Message
from common.net_const import NONE_MARKER
from common.space import Ship


class ServerTickMessage(Message):
    MESSAGE_NAME = "server_tick"

    def __init__(
            self,
            ship_id,
            solar_system_id,
            ships,
            projectiles={},
            resources={},
            targeting_ship_id=None,
            targeted_by_ship_id=None
    ):
        self.ship_id = ship_id
        self.solar_system_id = solar_system_id
        self.ships = ships
        self.projectiles = projectiles
        self.resources = resources
        self.targeting_ship_id = targeting_ship_id
        self.targeted_by_ship_id = targeted_by_ship_id

    @classmethod
    def fields(cls):
        return {
            "ships": (FIELD_TYPE_MULTIPLE_SHIPS, Ship),
            "ship_id": (FIELD_TYPE_VALUE, int),
            "solar_system_id": (FIELD_TYPE_VALUE, int),
            "targeting_ship_id": (FIELD_TYPE_VALUE, int),
            "targeted_by_ship_id": (FIELD_TYPE_VALUE, int),
        }

    def marshal(self):
        marshalled_ships = [ship.marshal() for ship in self.ships]
        message = [
            self.MESSAGE_NAME,
            "%d" % len(self.ships),
            ":".join(marshalled_ships),
            "%d" % self.ship_id,
            "%d" % self.solar_system_id,
            "%d" % (self.targeting_ship_id or NONE_MARKER),
            "%d" % (self.targeted_by_ship_id or NONE_MARKER),
        ]

        return ":".join(message)

    @classmethod
    def unmarshal(cls, encoded):
        fields_map = ServerTickMessage._unmarshal_fields_map(encoded)
        return ServerTickMessage(
            fields_map["ship_id"],
            fields_map["solar_system_id"],
            fields_map["ships"],
            targeted_by_ship_id=fields_map["targeted_by_ship_id"],
            targeting_ship_id=fields_map["targeting_ship_id"]
        )