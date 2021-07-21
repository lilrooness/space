import pygame

BLACK = pygame.Color(0, 0, 0, 255)
WHITE = pygame.Color(255, 255, 255, 255)
GRAY = pygame.Color(100, 100, 100, 50)
GREEN = pygame.Color(0, 255, 0, 255)
YELLOW = pygame.Color(255, 255, 0, 255)
RED = pygame.Color(255, 0, 0, 255)

SCREEN_W = 640
SCREEN_H = 480

SHIP_WIDTH = 20
SHIP_HEIGHT = 20

scheme = {
    "background": BLACK,
    "entity": WHITE,
    "foreground": GRAY,
    "hover_reticule": YELLOW,
    "targeted_reticule": RED,
}
