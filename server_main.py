import socket
from datetime import datetime
from select import select

from common.const import SHIELD_REPAIRER
from common.entities.ship import Ship
from common.entities.slot import Slot, SHIELD_CONSTRAINT, ENGINE_CONSTRAINT, WEAPON_CONSTRAINT, HULL_CONSTRAINT
from common.net_const import SERVER_TICK_TIME
from server.commands import process_command
from server.const import load_types
from server.game import server_game
from server.id import new_id
from server.map_reader import read_map_data
from server.sessions.session import Session
from server.sessions.sessions import get_sessions, get_message_queue


def accept_new_connections(server_socket, sessions, systems):
    readable, _, _  = select([server_socket], [], [], 0)
    if len(readable) == 1:
        connection, address = server_socket.accept()

        weapon_slot_1 = Slot(type_constraint=WEAPON_CONSTRAINT, type_id=SHIELD_REPAIRER, max_ammo=3, ammo=3, id_fun=new_id)
        engine_slot = Slot(type_constraint=ENGINE_CONSTRAINT, id_fun=new_id)
        shield_slot = Slot(type_constraint=SHIELD_CONSTRAINT, id_fun=new_id)
        hull_slot = Slot(type_constraint=HULL_CONSTRAINT, id_fun=new_id)

        new_ship = Ship(
            10,
            10,
            vx=0,
            vy=0,
            id_fun=new_id,
            shield_slots= {shield_slot.id: shield_slot},
            engine_slots = {engine_slot.id: engine_slot},
            weapon_slots = {weapon_slot_1.id: weapon_slot_1},
            hull_slots = {hull_slot.id: hull_slot},
        )

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
            del get_sessions()[session_id]

        # receive from clients
        for _, session in get_sessions().items():
            if session.check_alive():
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
