from client import camera
from common.messages.messages import ServerTickMessage
from client.const import SHIP_HEIGHT, SHIP_WIDTH
from common.messages.ship_damage import ShipDamageMessage


class Game():

    def __init__(self, ships={}, ship_id=None, solar_system_id=None, resources=None):
        self.ships = {}
        self.ship_id = ship_id
        self.solar_system_id = solar_system_id
        self.resources = resources
        self.targeting_ship_id = None
        self.targeted_by_ship_id = None
        self.active_laser_shots = {}
        self.power_allocation_guns = 1.0
        self.power_allocation_shields = 0.0
        self.power_allocation_engines = 0.0

def handle_server_tick_message(game, message):
    game.ship_id = message.ship_id
    game.solar_system_id = message.solar_system_id
    ships = {}
    for ship in message.ships:
        ships[ship.id] = ship

    active_laser_shots = {}
    for laser in message.active_laser_shots:
        active_laser_shots[laser.id] = laser

    game.active_laser_shots = active_laser_shots
    game.ships = ships
    game.resources = message.resources
    game.power_allocation_shields = message.power_allocation_shields
    game.power_allocation_guns = message.power_allocation_guns
    game.power_allocation_engines = message.power_allocation_engines

    if message.targeting_ship_id > -1:
        game.targeting_ship_id = message.targeting_ship_id
    else:
        game.targeting_ship_id = None
    if message.targeted_by_ship_id > -1:
        game.targeted_by_ship_id = message.targeted_by_ship_id
    else:
        game.targeted_by_ship_id = None

def handle_ship_damage_message(game, message):
    print("some damage init")

def pick_ship(game, ship, mouse):
    shipX, shipY = camera.world_to_screen(game, ship.x, ship.y)
    if mouse.x >= shipX - SHIP_WIDTH/2 and mouse.x <= shipX + SHIP_WIDTH/2:
        if mouse.y >= shipY - SHIP_HEIGHT/2 and mouse.y <= shipY + SHIP_HEIGHT/2:
            return True
    return False

message_handlers = {
    ServerTickMessage: handle_server_tick_message,
    ShipDamageMessage: handle_ship_damage_message,
}