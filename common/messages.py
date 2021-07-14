from common.space import Entity, Ship


class Message():

    MESSAGE_NAME = None

    def marshal(self):
        pass

    def unmarshal(self):
        pass

class ServerTickMessage(Message):

    MESSAGE_NAME = "server_tick"

    def __init__(self, ship_id, solar_system_id, ships, projectiles={}, resources={}):
        self.ship_id = ship_id
        self.solar_system_id = solar_system_id
        self.ships = ships
        self.projectiles = projectiles
        self.resources = resources

    def marshal(self):
        marshalled_ships = [ship.marshal() for ship in self.ships]
        marshalled_projectiles = [proj.marshall() for proj in self.projectiles]
        return ":".join([
            self.MESSAGE_NAME,
            "%d" % len(self.ships),
            ":".join(marshalled_ships),
            "%d" % self.ship_id,
            "%d" % self.solar_system_id,
            "%d" % len(self.projectiles),
            ":".join(marshalled_projectiles),
        ])
    
    @classmethod
    def unmarshal(cls, encoded):
        parts = encoded.split(":")
        message_name = parts[0]
        nships = int(parts[1])
        encoded_ships = parts[2:2 + nships*len(Ship.marshalled_fields())]
        ships = Entity.unmarshall_multiple_of_type(":".join(encoded_ships), Ship)
        ship_id = parts[1 + nships]
        solar_system_id = int(parts[2 + nships])

        return ServerTickMessage(ship_id, solar_system_id, ships)

messages = {
    ServerTickMessage.MESSAGE_NAME: ServerTickMessage
}