import socket
from datetime import datetime
from select import select

from common.space import Ship, SolarSystem
from server.commands import process_command
from server.game.server_game import get_new_laser_shots
from server.id import new_id
from server.session import Session

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

    ticks = 0

    lastTick = datetime.now()
    tickFrequency = 500000 #in microseconds

    while(serverSocket.fileno() != -1):

        accept_new_connections(serverSocket, sessions, systems)
        
        delta = datetime.now() - lastTick

        for session in sessions:
            if not session.alive:
                del systems[session.solar_system_id].ships[session.ship_id]
                sessions.remove(session)

        # receive from clients
        for session in sessions:
            if session.check_alive():
                try:
                    request = session.receive_request()
                except Exception:
                    session.alive = False
                if request:
                    process_command(systems, session, request)

        if delta.microseconds >= tickFrequency:
            ticks += 1

            for _, system in systems.items():
                system.tick()
                system.active_laser_shots = get_new_laser_shots(system, ticks)

            # push state to all clients
            lastTick = datetime.now()
            for session in sessions:
                session.send_server_tick(systems)
