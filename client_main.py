import socket
from select import select

import pygame

from client.const import SCREEN_H, SCREEN_W
from client.game import Game, message_handlers, pick_ship
from client.mouse import get_mouse
from common.commands.request_moveto import RequestMoveToCommand
from common.commands.request_shoot import RequestShootCommand
from common.messages.messages import message_types
from common.net_const import HEADER_SIZE
from client.render import render_game


def receive(client_socket):
    def can_rcv():
        readable, _, _ = select([client_socket], [], [], 0)
        return len(readable) > 0

    while can_rcv():
        header = client_socket.recv(HEADER_SIZE)
        message_size = int.from_bytes(header, 'big')
        message = client_socket.recv(message_size)
        parts = message.decode().split(":")
        message_name = parts[0]
        message = message_types[message_name].unmarshal(message.decode())
        return message

    return None

def send_request(client_socket, request):
    bytes = request.marshal().encode()
    message_size = len(bytes)
    header = message_size.to_bytes(HEADER_SIZE, "big")
    print("sending message {}".format(header + bytes))
    client_socket.send(header + bytes)

def queue_to_send(out_message_queue, request):

    out_message_queue.append(request)

def process_out_message_queue(out_message_queue, client_socket):

    def can_snd():
        _, writable, _ = select([], [client_socket], [], 0)
        return len(writable) > 0

    while out_message_queue and can_snd():
        send_request(client_socket, out_message_queue[0])
        out_message_queue = out_message_queue[1:]

    return out_message_queue

def process_input(game):
    if get_mouse().down_this_frame:
        for ship_id, ship in game.ships.items():
            if ship_id != game.ship_id:
                if pick_ship(ship, get_mouse()):
                    queue_to_send(out_message_queue, RequestShootCommand(ship_id))
                    return

        queue_to_send(out_message_queue, RequestMoveToCommand(mouseX, mouseY))


if __name__ == "__main__":
    client_socket = socket.socket()
    client_socket.connect(("localhost", 12345))

    pygame.init()
    screenRect = pygame.Rect(0,0, SCREEN_H, SCREEN_H)
    run = True
    screen = pygame.display.set_mode((SCREEN_W, SCREEN_H))
    
    game = Game()
    mouseX = 0
    mouseY = 0

    out_message_queue = []

    while run:
        get_mouse().new_input_frame()
        message = receive(client_socket)

        if message:
            message_handlers[message.__class__](game, message)

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

        process_input(game)

        render_game(game, screen, screenRect)

        pygame.display.flip()
        out_message_queue = process_out_message_queue(out_message_queue, client_socket)
