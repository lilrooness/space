import pygame

BLACK = pygame.Color(0, 0, 0, 255)
WHITE = pygame.Color(255, 255, 255, 255)
GREEN = pygame.Color(0, 255, 0, 255)
YELLOW = pygame.Color(255, 255, 0, 255)

SCREEN_W = 640
SCREEN_H = 480

SHIP_WIDTH = 20
SHIP_HEIGHT = 20

scheme = {
    "background": BLACK,
    "entity": WHITE,
    "foreground": WHITE,
    "hover_reticule": YELLOW,
}