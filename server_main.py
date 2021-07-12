from common.net_const import HEADER_SIZE
from common.messages import ServerTickMessage
from math import e
import socket
from select import select
from datetime import datetime

from common.space import Ship, SolarSystem, Warp

LAST_ID = 0

def new_id():
    global LAST_ID
    print(LAST_ID) 
    LAST_ID += 1
    return LAST_ID

class Session():
    def __init__(self, connection, address, solar_system_id, ship_id, alive=True):
        self.connection = connection
        self.address = address
        self.solar_system_id = solar_system_id
        self.ship_id = ship_id
        self.alive = alive
    
    # should only be used before sending data to the client
    # between syncronisation ticks, just check alive flag
    def check_alive(self):
        if not self.alive:
            return False
         
        if self.connection.fileno() == -1:
            self.alive = False
            return False
        
        return True

    
    def request_warp_to(self, x, y):
        current_system = systems[self.solar_system_id]
        ship = current_system.ships[session.ship_id]

        if ship.warp:
            # already in warp
            return

        ship.warp = Warp((ship.x, ship.y), (x, y))


def accept_new_connections(server_socket, sessions, systems):
    readable, _, _  = select([server_socket], [], [], 0)
    if len(readable) == 1:
        connection, address = server_socket.accept()
        new_ship = Ship(10, 10, id_fun=new_id)
        systems[1].ships[new_ship.id] = new_ship
        new_session = Session(connection, address, 1, new_ship.id)
        sessions.append(new_session)

if __name__ == "__main__":

    systems = {
        1: SolarSystem(id_fun=new_id),
        2: SolarSystem(id_fun=new_id)
    }


    serverSocket = socket.socket()
    serverSocket.bind(("0.0.0.0", 12345))
    serverSocket.listen()

    sessions = []

    lastTick = datetime.now()
    tickFrequency = 500000 #in microseconds

    while(serverSocket.fileno() != -1):

        accept_new_connections(serverSocket, sessions, systems)
        
        delta = datetime.now() - lastTick
        if delta.microseconds >= tickFrequency:

            for _, system in systems.items():
                system.tick()

            # push state to all clients
            lastTick = datetime.now()
            for session in sessions:
                if session.check_alive():
                    session_ship_object = systems[session.solar_system_id].ships[session.ship_id]
                    
                    message = ServerTickMessage(
                        session.ship_id,
                        session.solar_system_id,
                        [session_ship_object]
                    ).marshal()

                    bytes = message.encode()
                    message_size = len(bytes)
                    header = message_size.to_bytes(HEADER_SIZE, "big")
                    session.connection.send(header + bytes)
