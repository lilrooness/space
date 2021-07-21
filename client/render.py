from common.space import Entity
import pygame

from client.const import SCREEN_H, SCREEN_W, scheme
from client.game import pick_ship
from client.mouse import get_mouse

def render_game(game, screen, screenRect):
    pygame.draw.rect(screen, scheme["background"], screenRect)
    for x in range(10):
        if x == 0:
            continue
        xpos = SCREEN_W / 10 * x
        pygame.draw.line(
            screen,
            scheme["foreground"],
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
            scheme["foreground"],
            (0, ypos),
            (SCREEN_W, ypos),
            width=1
        )

    for ship_id, ship in game.ships.items():
        reticule = pygame.Rect(ship.x - 10, ship.y - 10, 20, 20)
        if ship_id == game.targeting_ship_id:
            pygame.draw.rect(screen, scheme["targeted_reticule"], reticule, width=2)
        if pick_ship(ship, get_mouse()):
            pygame.draw.rect(screen, scheme["hover_reticule"], reticule, width=2)
        pygame.draw.circle(screen, scheme["entity"], (ship.x, ship.y), 5)