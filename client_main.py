import socket
from select import select
import pygame
from common.messages import messages as message_types

SCREEN_W = 640
SCREEN_H = 480

if __name__ == "__main__":
    client_socket = socket.socket()
    client_socket.connect(("localhost", 12345))

    pygame.init()
    screenRect = pygame.Rect(0,0, SCREEN_W, SCREEN_H)
    run = True
    screen = pygame.display.set_mode((SCREEN_W, SCREEN_H))
    
    while run:
        readable, _, _ =  select([client_socket], [], [], 0)
        if len(readable) > 0:
            header = client_socket.recv(4)
            message_size = int.from_bytes(header, 'big')
            message = client_socket.recv(message_size)
            message_name = message.decode().split(":")[0]
            print(message.decode())
            print(message_types[message_name])
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                continue
