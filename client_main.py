from common.commands.request_moveto import RequestMoveToCommand
from common.net_const import HEADER_SIZE
import socket
from select import select
import pygame
from common.messages import messages as message_types
from client.const import WHITE, BLACK
from client.game import Game, message_handlers

SCREEN_W = 640
SCREEN_H = 480

def receive(client_socket):
    readable, _, _ =  select([client_socket], [], [], 0)
    if len(readable) > 0:
        header = client_socket.recv(HEADER_SIZE)
        message_size = int.from_bytes(header, 'big')
        message = client_socket.recv(message_size)
        parts = message.decode().split(":")
        message_name = parts[0]
        print(parts)
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
    if out_message_queue:
        _, writable, _ = select([], [client_socket], [], 0)
        if len(writable) > 0:
            send_request(client_socket, out_message_queue[0])
            out_message_queue = out_message_queue[1:]

    return out_message_queue

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

    out_message_queue = []

    while run:
        message = receive(client_socket)

        if message:
            message_handlers[message.__class__](game, message)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                continue
            if event.type == pygame.MOUSEMOTION:
                mouseX, mouseY = event.pos

            if event.type == pygame.MOUSEBUTTONUP:
                queue_to_send(out_message_queue, RequestMoveToCommand(mouseX, mouseY))
        
        pygame.draw.rect(screen, WHITE, screenRect)
        for x in range(10):
            if x == 0:
                continue
            xpos = SCREEN_W / 10 * x
            pygame.draw.line(
                screen,
                BLACK,
                (xpos, 0),
                (xpos, SCREEN_H),
                width=1,
            )
        
        for y in range(10):
            if y == 0:
                continue
            ypos = SCREEN_H / 10 * y
            pygame.draw.line(
                screen,
                BLACK,
                (0, ypos),
                (SCREEN_W, ypos),
                width=1
            )

        for _id, ship in game.ships.items():
            pygame.draw.circle(screen, BLACK, (ship.x, ship.y), 5)

        pygame.display.flip()
        out_message_queue = process_out_message_queue(out_message_queue, client_socket)
