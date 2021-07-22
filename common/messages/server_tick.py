from common.messages.message import FIELD_TYPE_VALUE, Message, \
    FIELD_TYPE_MULTIPLE_ENTITIES
from common.net_const import NONE_MARKER
from common.space import Ship, LaserShot


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
            targeted_by_ship_id=None,
            active_laser_shots={},
    ):
        self.ship_id = ship_id
        self.solar_system_id = solar_system_id
        self.ships = ships
        self.projectiles = projectiles
        self.resources = resources
        self.targeting_ship_id = targeting_ship_id
        self.targeted_by_ship_id = targeted_by_ship_id
        self.active_laser_shots = active_laser_shots

    @classmethod
    def fields(cls):
        return {
            "ships": (FIELD_TYPE_MULTIPLE_ENTITIES, Ship),
            "ship_id": (FIELD_TYPE_VALUE, int),
            "solar_system_id": (FIELD_TYPE_VALUE, int),
            "targeting_ship_id": (FIELD_TYPE_VALUE, int),
            "targeted_by_ship_id": (FIELD_TYPE_VALUE, int),
            "active_laser_shots": (FIELD_TYPE_MULTIPLE_ENTITIES, LaserShot)
        }

    def marshal(self):
        marshalled_ships = [ship.marshal() for ship in self.ships]
        active_laser_shots = [laser.marshal() for laser in self.active_laser_shots]
        message = [
            self.MESSAGE_NAME,
            "%d" % len(self.ships),
            ":".join(marshalled_ships),
            "%d" % self.ship_id,
            "%d" % self.solar_system_id,
            "%d" % (self.targeting_ship_id or NONE_MARKER),
            "%d" % (self.targeted_by_ship_id or NONE_MARKER),
            "%d" % len(self.active_laser_shots),
            ":".join(active_laser_shots or [str(NONE_MARKER)]),
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
            targeting_ship_id=fields_map["targeting_ship_id"],
            active_laser_shots=fields_map["active_laser_shots"],
        )