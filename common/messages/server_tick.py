from common.entities.crate import Crate
from common.entities.inflight_missile import InFlightMissile
from common.entities.laser_shot import LaserShot
from common.entities.mini_gun_shot import MinigunShot
from common.entities.ship import Ship
from common.entities.slot import Slot
from common.messages.message import Message
from common.serializable.serializable import FIELD_TYPE_VALUE, Serializable, \
    FIELD_TYPE_MULTIPLE_ENTITIES
from common.net_const import NONE_MARKER


class ServerTickMessage(Message):
    MESSAGE_NAME = "server_tick"

    def __init__(
            self,
            ship_id,
            solar_system_id,
            ships,
            projectiles={},
            resources={},
            targeted_by_ship_id=None,
            active_laser_shots=[],
            in_flight_missiles=[],
            power_allocation_guns = None,
            power_allocation_shields = None,
            power_allocation_engines = None,
            crates = [],
            shield_slots = [],
            engine_slots = [],
            weapon_slots = [],
            hull_slots = [],
            mini_gun_shots = [],
    ):
        self.ship_id = ship_id
        self.solar_system_id = solar_system_id
        self.ships = ships
        self.projectiles = projectiles
        self.resources = resources
        self.targeted_by_ship_id = targeted_by_ship_id
        self.active_laser_shots = active_laser_shots
        self.power_allocation_guns = power_allocation_guns
        self.power_allocation_shields = power_allocation_shields
        self.power_allocation_engines = power_allocation_engines
        self.crates = crates
        self.shield_slots = shield_slots
        self.engine_slots = engine_slots
        self.weapon_slots = weapon_slots
        self.hull_slots   = hull_slots
        self.in_flight_missiles = in_flight_missiles
        self.mini_gun_shots = mini_gun_shots

    @classmethod
    def fields(cls):
        return {
            "ships": (FIELD_TYPE_MULTIPLE_ENTITIES, Ship),
            "ship_id": (FIELD_TYPE_VALUE, int),
            "solar_system_id": (FIELD_TYPE_VALUE, int),
            "targeted_by_ship_id": (FIELD_TYPE_VALUE, int),
            "active_laser_shots": (FIELD_TYPE_MULTIPLE_ENTITIES, LaserShot),
            "in_flight_missiles": (FIELD_TYPE_MULTIPLE_ENTITIES, InFlightMissile),
            "mini_gun_shots": (FIELD_TYPE_MULTIPLE_ENTITIES, MinigunShot),
            "power_allocation_guns": (FIELD_TYPE_VALUE, float),
            "power_allocation_shields": (FIELD_TYPE_VALUE, float),
            "power_allocation_engines": (FIELD_TYPE_VALUE, float),
            "crates": (FIELD_TYPE_MULTIPLE_ENTITIES, Crate),
            "shield_slots": (FIELD_TYPE_MULTIPLE_ENTITIES, Slot),
            "engine_slots": (FIELD_TYPE_MULTIPLE_ENTITIES, Slot),
            "weapon_slots": (FIELD_TYPE_MULTIPLE_ENTITIES, Slot),
            "hull_slots": (FIELD_TYPE_MULTIPLE_ENTITIES, Slot),
        }

    def marshal(self):

        marshalled_ships = [ship.marshal() for ship in self.ships]
        active_laser_shots = [laser.marshal() for laser in self.active_laser_shots]
        marshalled_in_flight_missiles = [missile.marshal() for missile in self.in_flight_missiles]
        marshalled_mini_gun_shots = [shot.marshal() for shot in self.mini_gun_shots]
        marshalled_crates = [crate.marshal() for crate in self.crates]
        marshalled_shield_slots = [slot.marshal() for slot in self.shield_slots]
        marshalled_engine_slots = [slot.marshal() for slot in self.engine_slots]
        marshalled_weapon_slots = [slot.marshal() for slot in self.weapon_slots]
        marshalled_hull_slots = [slot.marshal() for slot in self.hull_slots]

        message = [
            self.MESSAGE_NAME,
            "%d" % len(self.ships),
            ":".join(marshalled_ships),
            "%d" % self.ship_id,
            "%d" % self.solar_system_id,
            "%d" % (self.targeted_by_ship_id or NONE_MARKER),
            "%d" % len(self.active_laser_shots),
            ":".join(active_laser_shots or [str(NONE_MARKER)]),
            "%d" % len(marshalled_in_flight_missiles),
            ":".join(marshalled_in_flight_missiles or [str(NONE_MARKER)]),
            "%d" % len(marshalled_mini_gun_shots),
            ":".join(marshalled_mini_gun_shots or [str(NONE_MARKER)]),
            "%f" % self.power_allocation_guns,
            "%f" % self.power_allocation_shields,
            "%f" % self.power_allocation_engines,
            "%d" % len(self.crates),
            ":".join(marshalled_crates or [str(NONE_MARKER)]),
            "%d" % len(self.shield_slots),
            ":".join(marshalled_shield_slots),
            "%d" % len(self.engine_slots),
            ":".join(marshalled_engine_slots),
            "%d" % len(self.weapon_slots),
            ":".join(marshalled_weapon_slots),
            "%d" % len(self.hull_slots),
            ":".join(marshalled_hull_slots),
        ]

        return ":".join(message)

    @classmethod
    def unmarshal(cls, encoded):
        fields_map, _remaining = ServerTickMessage.message_unmarshal_fields_map(encoded)

        return ServerTickMessage(
            fields_map["ship_id"],
            fields_map["solar_system_id"],
            fields_map["ships"],
            targeted_by_ship_id=fields_map["targeted_by_ship_id"],
            active_laser_shots=fields_map["active_laser_shots"],
            power_allocation_guns=fields_map["power_allocation_guns"],
            power_allocation_shields=fields_map["power_allocation_shields"],
            power_allocation_engines=fields_map["power_allocation_engines"],
            crates=fields_map["crates"],
            hull_slots=fields_map["hull_slots"],
            weapon_slots=fields_map["weapon_slots"],
            engine_slots=fields_map["engine_slots"],
            shield_slots=fields_map["shield_slots"],
            in_flight_missiles=fields_map["in_flight_missiles"],
            mini_gun_shots=fields_map["mini_gun_shots"],
        )