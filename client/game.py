from common.messages.messages import ServerTickMessage


class Game():

    def __init__(self, ships={}, ship_id=None, solar_system_id=None, resources=None):
        self.ships = {}
        self.ship_id = ship_id
        self.solar_system_id = solar_system_id
        self.resources = resources

def handle_server_tick_message(game, message):
    game.ship_id = message.ship_id
    game.solar_system_id = message.solar_system_id
    ships = {}
    for ship in message.ships:
        ships[ship.id] = ship

    game.ships = ships
    game.resources = message.resources

message_handlers = {
    ServerTickMessage: handle_server_tick_message
}