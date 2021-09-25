from select import select

from common.commands.commands import commands
from common.entities.ship import Warp
from common.messages.server_tick import ServerTickMessage
from common.net_const import HEADER_SIZE
from server.game.server_game import get_ship_ids_in_sensor_range_of_ship, does_ship_have_sensor_tower_buff
from server.id import new_id
from server.logger import get_session_logger


class Session():
    def __init__(self, connection, address, solar_system_id, ship_id, alive=True, admin=False):
        self.connection = connection
        self.address = address
        self.solar_system_id = solar_system_id
        self.ship_id = ship_id
        self.alive = alive
        self.admin=admin
        self.id = new_id()

    # should only be used before sending data to the client
    # between syncronisation ticks, just check alive flag
    def check_alive(self):
        if not self.alive:
            return False

        if self.connection.fileno() == -1:
            self.alive = False
            return False

        return True

    # TODO: move this to command handler
    def request_warp_to(self, systems, x, y):
        current_system = systems[self.solar_system_id]
        ship = current_system.ships[self.ship_id]

        if ship.warp:
            # already in warp
            return

        ship.warp = Warp((ship.x, ship.y), (x, y))

    def receive_request(self):
        readable, _, _ = select([self.connection], [], [], 0)
        if len(readable) > 0:
            header = self.connection.recv(HEADER_SIZE)
            message_size = int.from_bytes(header, "big")
            message = self.connection.recv(message_size)
            parts = message.decode().split(":")
            request_name = parts[0]
            request = commands[request_name].unmarshal(message.decode())
            get_session_logger().to_server_log(self.id, request)
            return request

        return None

    def send_messages(self, messages):
        def can_snd():
            _, writable, _ = select([], [self.connection], [], 0)
            return len(writable) > 0
        while can_snd() and messages:
            message = messages[0]
            bytes = message.marshal().encode()
            length = len(bytes)
            header = length.to_bytes(HEADER_SIZE, "big")
            get_session_logger().to_client_log(self.id, message)
            try:
                self.connection.send(header + bytes)
                messages = messages[1:]
            except Exception:
                self.alive = False

        return messages

    def send_server_tick(self, systems, ticks):
        if self.check_alive():
            session_system_object = systems[self.solar_system_id]
            session_ship_object = session_system_object.ships[self.ship_id]

            visible_ships = self._get_visible_ships_list(session_system_object)
            active_laser_shots = [shot for _id, shot in session_system_object.active_laser_shots.items()]
            visible_crates = [crate for _id, crate, in session_system_object.crates.items()]
            in_flight_missiles = [missile for _id, missile in session_system_object.in_flight_missiles.items()]
            serverTickMessage = ServerTickMessage(
                self.ship_id,
                self.solar_system_id,
                visible_ships,
                active_laser_shots=active_laser_shots,
                in_flight_missiles=in_flight_missiles,
                power_allocation_guns=session_ship_object.power_allocation_guns,
                power_allocation_shields=session_ship_object.power_allocation_shields,
                power_allocation_engines=session_ship_object.power_allocation_engines,
                crates=visible_crates,
                weapon_slots=list(session_ship_object.weapon_slots.values()),
                shield_slots=list(session_ship_object.shield_slots.values()),
                engine_slots=list(session_ship_object.engine_slots.values()),
                hull_slots=list(session_ship_object.hull_slots.values()),
                mini_gun_shots=list(session_system_object.mini_gun_shots.values()),
                sensor_towers=list(session_system_object.sensor_towers.values()),
                sensor_tower_boost=does_ship_have_sensor_tower_buff(session_system_object, self.ship_id),
                warp_points=list(session_system_object.warp_points.values()),
                speed_boost_clouds=list(session_system_object.speed_boost_clouds.values()),
                server_tick_number=ticks,
            )

            get_session_logger().to_client_log(self.id, serverTickMessage)
            message = serverTickMessage.marshal()

            bytes = message.encode()
            message_size = len(bytes)

            if message_size == 0:
                # this was happening ... but I guess not anymore -
                # keeping this here just in case
                print("WARNING!! WE'RE SENDING A ZERO HEADER!")
                print("message: {}".format(message))

            header = message_size.to_bytes(HEADER_SIZE, "big")
            try:
                self.connection.send(header + bytes)
            except Exception:
                self.alive = False

    def _get_visible_ships_list(self, system):

        visible_ships = []

        if does_ship_have_sensor_tower_buff(system, self.ship_id):
            visible_ships = list(system.ships.values())
        else:
            visible_ships = [system.ships[self.ship_id]]

            in_range_ships = [system.ships[ship_id] for ship_id in get_ship_ids_in_sensor_range_of_ship(system, self.ship_id)]
            visible_ships = visible_ships + in_range_ships

        return visible_ships
