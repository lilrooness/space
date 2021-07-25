import socket
from select import select

import pygame

from client import camera
from client.camera import set_camera
from client.const import SCREEN_H, SCREEN_W
from client.game import Game, message_handlers, pick_ship
from client.mouse import get_mouse
from common.commands.request_moveto import RequestMoveToCommand
from common.commands.request_shoot import RequestShootCommand
from common.messages.messages import message_types
from common.net_const import HEADER_SIZE
from client.render import render_game, render_static_ui
from client.session import process_out_message_queue, queue_to_send


def receive(client_socket):
    def can_rcv():
        readable, _, _ = select([client_socket], [], [], 0)
        return len(readable) > 0

    messages = []

    while can_rcv():
        header = client_socket.recv(HEADER_SIZE)
        message_size = int.from_bytes(header, 'big')
        message = client_socket.recv(message_size)
        parts = message.decode().split(":")
        message_name = parts[0]
        message = message_types[message_name].unmarshal(message.decode())
        messages.append(message)

    return messages

def process_input(game):
    camera_x_transform, camera_y_transform = camera.get_camera()
    if get_mouse().down_this_frame:
        for ship_id, ship in game.ships.items():
            if ship_id != game.ship_id:
                if pick_ship(ship, get_mouse(), camera_x_transform, camera_y_transform):
                    queue_to_send(RequestShootCommand(ship_id))
                    return

        queue_to_send(RequestMoveToCommand(mouseX + camera_x_transform, mouseY + camera_y_transform))


if __name__ == "__main__":
    client_socket = socket.socket()
    client_socket.connect(("localhost", 12345))

    pygame.init()
    screenRect = pygame.Rect(0,0, SCREEN_W, SCREEN_H)
    run = True
    screen = pygame.display.set_mode((SCREEN_W, SCREEN_H))
    
    game = Game()
    mouseX = 0
    mouseY = 0

    while run:
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
                get_mouse().set_mouse_up()

            if event.type == pygame.MOUSEBUTTONDOWN:
                get_mouse().set_mouse_down()

        render_game(game, screen, screenRect)
        render_static_ui(game, screen)

        process_input(game)

        pygame.display.flip()
        out_message_queue = process_out_message_queue(client_socket)
