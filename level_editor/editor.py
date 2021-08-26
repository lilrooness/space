import pygame

BLACK = pygame.Color(0, 0, 0, 255)
WHITE = pygame.Color(255, 255, 255, 255)
LIGHT_GRAY = pygame.Color(150, 150, 150, 100)
GRAY = pygame.Color(100, 100, 100, 100)
DARK_GRAY = pygame.Color(50, 50, 50, 100)
GREEN = pygame.Color(0, 255, 0, 255)
YELLOW = pygame.Color(255, 255, 0, 255)
RED = pygame.Color(255, 0, 0, 255)
RED_TRANSPARENT = pygame.Color(255, 0, 0, 1)
CYAN = pygame.Color(0, 255, 255, 255)
PINK = pygame.Color(255, 20, 147, 255)

SCREEN_W = 640*2
SCREEN_H = 480*2

class EditorState():

    def __init__(self, sensor_towers={}, crates={}):
        self.sensor_towers = sensor_towers
        self.crates = crates
        self.selected = None

    def select_placeable(self, type_id):
        self.selected = type_id