class Message():

    MESSAGE_NAME = None

    def marshal(self):
        pass

    def unmarshal(self):
        pass

class ServerTickMessage(Message):

    MESSAGE_NAME = "server_tick"

    def __init__(self, ship_id, solar_system_id, ships, resources={}):
        self.ship_id = ship_id
        self.solar_system_id = solar_system_id
        self.ships = ships
        self.resources = resources

    def marshal(self):
        marshalled_ships = [ServerTickMessage.marshal_ship(ship) for ship in self.ships]
        return ":".join([
            self.MESSAGE_NAME,
            "%d" % len(self.ships),
            ":".join(marshalled_ships),
            "%d" % self.ship_id,
            "%d" % self.solar_system_id,
        ])
    
    def unmarshal(self):
        pass

    @classmethod
    def marshal_ship(cls, ship):
        return "{}:{}:{}:{}:{}".format(ship.id, ship.x, ship.y, ship.health, ship.ammo)

messages = {
    ServerTickMessage.MESSAGE_NAME: ServerTickMessage
}