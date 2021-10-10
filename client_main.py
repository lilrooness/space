import socket
from select import select

import pygame

from client.camera import set_camera, get_camera_zoom, set_camera_zoom, screen_to_world
from client.const import SCREEN_H, SCREEN_W, load_types
from client.game import Game, message_handlers, pick_ship
from client.mouse import get_mouse
from client.render import render_game, render_static_ui
from client.session import process_out_message_queue, queue_to_send
from client.texture import load_loot_icon_textures
from common.commands.request_moveto import RequestMoveToCommand
from common.commands.request_target import RequestTargetCommand
from common.commands.request_warp import RequestWarpCommand
from common.messages.messages import message_types
from common.net_const import HEADER_SIZE

remaining_size_to_read = 0
remaining_message_buffer = None

def receive(client_socket):
    global remaining_size_to_read
    global remaining_message_buffer
    def can_rcv():
        readable, _, _ = select([client_socket], [], [], 0)
        return len(readable) > 0

    messages = []

    while can_rcv():
        if remaining_size_to_read:
            remaining_message = client_socket.recv(remaining_size_to_read)
            remaining_message_buffer = remaining_message_buffer + remaining_message
            if len(remaining_message) == remaining_size_to_read:
                print("completing old message")
                remaining_size_to_read = 0
                message = decode_bytes_to_message(remaining_message_buffer)
                messages.append(message)
                remaining_message_buffer = None
        else:
            header = client_socket.recv(HEADER_SIZE)
            message_size = int.from_bytes(header, 'big')
            message = client_socket.recv(message_size)
            actual_size = len(message)
            remaining_size_to_read = message_size - actual_size
            if remaining_size_to_read == 0:
                message = decode_bytes_to_message(message)
                messages.append(message)
            else:
                print("saving message for later")
                remaining_message_buffer = message


    return messages

def decode_bytes_to_message(bytes):
    parts = bytes.decode().split(":")
    message_name = parts[0]
    message = message_types[message_name].unmarshal(bytes.decode())
    return message

def process_input(game):
    if get_mouse().down_this_frame:
        for ship_id, ship in game.ships.items():
            if game.selected_slot_id:
                if pick_ship(game, ship, get_mouse()):
                    queue_to_send(RequestTargetCommand(ship_id, game.selected_slot_id))
                    return


        world_coords = screen_to_world(game, mouseX, mouseY)
        if get_camera_zoom() < 8:
            queue_to_send(RequestMoveToCommand(*world_coords), optimistic_state=game)
        else:
            queue_to_send(RequestWarpCommand(*world_coords))

    if get_mouse().wheel_scrolled:
        set_camera_zoom(get_camera_zoom() + get_mouse().wheel_scroll_amount)
        get_mouse().use_button_event("wheel_scrolled")

def get_host_settings(filename):
    with open(filename, "r") as settings_file:
        settings = {}
        lines = settings_file.readlines()
        for line in lines:
            parts = line.split(":", 1)
            if not line.startswith("#") and len(parts) == 2:
                settings[parts[0].strip()] = parts[1].strip()

        return settings

if __name__ == "__main__":
    client_socket = socket.socket()
    host_settings = get_host_settings("client_settings.txt")

    if host_settings:
        client_socket.connect((host_settings["hostname"], int(host_settings["port"])))
    else:
        raise Exception("ERROR: Could not read settings file")

    pygame.init()
    pygame.font.init()
    pygame.image.get_extended()

    load_types()
    load_loot_icon_textures()

    font = pygame.font.SysFont("sourcecodeproblack", 27)
    screenRect = pygame.Rect(0,0, SCREEN_W, SCREEN_H)
    run = True
    screen = pygame.display.set_mode((SCREEN_W, SCREEN_H))
    
    game = Game()
    mouseX = 0
    mouseY = 0

    static_ui_state = None

    while run:

        game.tick()

        get_mouse().new_input_frame()
        messages = receive(client_socket)

        if messages:
            for message in messages:
                message_handlers[message.__class__](game, message)

        if game.ship_id:
            set_camera(
                game.ships[game.ship_id].x - SCREEN_W / 2,
                game.ships[game.ship_id].y - SCREEN_H / 2,
            )

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                continue
            if event.type == pygame.MOUSEMOTION:
                mouseX, mouseY = event.pos
                get_mouse().set_pos(mouseX, mouseY)

            if event.type == pygame.MOUSEBUTTONUP:
                get_mouse().set_mouse_up(pygame.mouse.get_pressed(num_buttons=3))

            if event.type == pygame.MOUSEBUTTONDOWN:
                get_mouse().set_mouse_down(pygame.mouse.get_pressed(num_buttons=3))

            if event.type == pygame.MOUSEWHEEL:
                get_mouse().set_wheel_scrolled(event.y)

        if game.ship_id:
            render_game(game, screen, screenRect)
            static_ui_state = render_static_ui(game, screen, static_ui_state, font)
            process_input(game)

        pygame.display.flip()
        out_message_queue = process_out_message_queue(client_socket)
