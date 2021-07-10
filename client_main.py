import socket
from select import select
import pygame

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
            bytes = client_socket.recv(4)
            solar_system  = int.from_bytes(bytes, 'big')
            print(solar_system)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                continue
