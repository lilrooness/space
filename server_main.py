import socket
from datetime import datetime
from select import select

from common.net_const import SERVER_TICK_TIME
from server.commands import process_command
from server.const import load_types
from server.game import server_game
from server.game.server_game import spawn_new_ship
from server.logger import get_session_logger
from server.map_reader import read_map_data
from server.sessions.session import Session
from server.sessions.sessions import get_sessions, get_message_queue


def accept_new_connections(server_socket, sessions, systems):
    readable, _, _  = select([server_socket], [], [], 0)
    if len(readable) == 1:
        connection, address = server_socket.accept()

        new_ship = spawn_new_ship(systems[1])
        new_session = Session(connection, address, 1, new_ship.id)
        sessions[new_session.id] = new_session

def process_out_message_queue(message_queue, sessions):
    for session_id, messages in message_queue.items():
        if session_id in sessions:
            session = sessions[session_id]
            remaining_messages = session.send_messages(messages)
            message_queue[session_id] = remaining_messages

def run_game():
    loaded_system = read_map_data("data/map.yaml")
    load_types()
    server_game.seed_loot(loaded_system)
    systems = {
        1: loaded_system
    }


    serverSocket = socket.socket()
    serverSocket.bind(("0.0.0.0", 12345))
    serverSocket.listen()

    message_queue = {}

    ticks = 0

    lastTick = datetime.now()

    while(serverSocket.fileno() != -1):

        accept_new_connections(serverSocket, get_sessions(), systems)
        
        delta = datetime.now() - lastTick

        sessions_to_delete = []
        for session_id, session in get_sessions().items():
            if not session.alive:
                del systems[session.solar_system_id].ships[session.ship_id]
                sessions_to_delete.append(session_id)

        for session_id in sessions_to_delete:
            get_session_logger().flush_session_logs(session_id)
            del get_sessions()[session_id]

        # receive from clients
        for _, session in get_sessions().items():
            if session.alive:
                try:
                    request = session.receive_request()
                except Exception:
                    session.alive = False
                if request:
                    process_command(systems, session, request, ticks)

        if delta.microseconds >= SERVER_TICK_TIME:
            ticks += 1

            server_game.tick(systems, ticks)

            # push state to all clients
            lastTick = datetime.now()
            for _, session in get_sessions().items():
                session.send_server_tick(systems, ticks)

            process_out_message_queue(get_message_queue(), get_sessions())

            # do some cleanup here of objects that no longer need to be around
            # because we've informed the clients about them
            for sys_id, system in systems.items():
                minigunshot_ids_to_delete = []
                for id, shot in system.mini_gun_shots.items():
                    if shot.resolved:
                        minigunshot_ids_to_delete.append(id)

                for id in minigunshot_ids_to_delete:
                    del system.mini_gun_shots[id]

if __name__ == "__main__":
    try:
        run_game()
    finally:
        print("Flushing session logs after error...")
        get_session_logger().flush_all_session_logs()

