import socket
from datetime import datetime
from select import select

from common.space import Ship, SolarSystem
from server.commands import process_command
from server.game import server_game
from server.id import new_id
from server.sessions.session import Session
from server.sessions.sessions import get_sessions, get_message_queue


def accept_new_connections(server_socket, sessions, systems):
    readable, _, _  = select([server_socket], [], [], 0)
    if len(readable) == 1:
        connection, address = server_socket.accept()
        new_ship = Ship(10, 10, id_fun=new_id)
        systems[1].ships[new_ship.id] = new_ship
        new_session = Session(connection, address, 1, new_ship.id)
        sessions[new_session.id] = new_session

def process_out_message_queue(message_queue, sessions):
    for session_id, messages in message_queue.items():
        if session_id in sessions:
            session = sessions[session_id]
            remaining_messages = session.send_messages(messages)
            message_queue[session_id] = remaining_messages

if __name__ == "__main__":

    systems = {
        1: SolarSystem(id_fun=new_id),
        2: SolarSystem(id_fun=new_id)
    }


    serverSocket = socket.socket()
    serverSocket.bind(("0.0.0.0", 12345))
    serverSocket.listen()

    message_queue = {}

    ticks = 0

    lastTick = datetime.now()
    tickFrequency = 500000 #in microseconds

    while(serverSocket.fileno() != -1):

        accept_new_connections(serverSocket, get_sessions(), systems)
        
        delta = datetime.now() - lastTick

        sessions_to_delete = []
        for session_id, session in get_sessions().items():
            if not session.alive:
                del systems[session.solar_system_id].ships[session.ship_id]
                sessions_to_delete.append(session_id)

        for session_id in sessions_to_delete:
            del get_sessions()[session_id]

        # receive from clients
        for _, session in get_sessions().items():
            if session.check_alive():
                try:
                    request = session.receive_request()
                except Exception:
                    session.alive = False
                if request:
                    process_command(systems, session, request)

        if delta.microseconds >= tickFrequency:
            ticks += 1

            server_game.tick(systems, ticks)

            # push state to all clients
            lastTick = datetime.now()
            for _, session in get_sessions().items():
                session.send_server_tick(systems)

            process_out_message_queue(get_message_queue(), get_sessions())
