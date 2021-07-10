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
        marshalled_ships = [ship.marshal() for ship in self.ships]
        return ":".join([
            self.MESSAGE_NAME,
            "%d" % len(self.ships),
            ":".join(marshalled_ships),
            "%d" % self.ship_id,
            "%d" % self.solar_system_id,
        ])
    
    @classmethod
    def unmarshal(cls, encoded):
        parts = encoded.split(":")
        message_name = parts[0]
        nships = parts[1]
        ship_id = parts[1 + nships]
        solar_system_id = parts[2 + nships]

        print("message_name: {}, nships: {}, ship_id: {}, solar_system_id: {}")
        return

messages = {
    ServerTickMessage.MESSAGE_NAME: ServerTickMessage
}