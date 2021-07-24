import math

import pygame

from client.camera import get_camera
from client.const import SCREEN_H, SCREEN_W, scheme, SHIP_HEALTH_ARC_DIAM, SHIP_SHIELD_ARC_DIAM, RETICULE_SIZE
from client.game import pick_ship
from client.mouse import get_mouse
from client.ui.power_window import power_window


def render_static_ui(game, screen):
    power_window(game, screen)

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

    camera_x_transform, camera_y_transform = get_camera()

    for ship_id, ship in game.ships.items():
        reticule = pygame.Rect(ship.x - RETICULE_SIZE/2 - camera_x_transform, ship.y - RETICULE_SIZE/2 - camera_y_transform, RETICULE_SIZE, RETICULE_SIZE)
        if ship_id == game.targeting_ship_id:
            pygame.draw.rect(screen, scheme["targeted_reticule"], reticule, width=2)
        if ship_id != game.ship_id and pick_ship(ship, get_mouse(), camera_x_transform, camera_y_transform):
            pygame.draw.rect(screen, scheme["hover_reticule"], reticule, width=2)
        pygame.draw.circle(screen, scheme["entity"], (ship.x - camera_x_transform, ship.y - camera_y_transform), 5)

        healthRect = pygame.Rect(
            ship.x - SHIP_HEALTH_ARC_DIAM/2 - camera_x_transform,
            ship.y - SHIP_HEALTH_ARC_DIAM/2 - camera_y_transform,
            SHIP_HEALTH_ARC_DIAM,
            SHIP_HEALTH_ARC_DIAM,
        )
        pygame.draw.arc(screen, scheme["health"], healthRect, 0, math.pi * 2 * (ship.health/100.0), width=2)
        shieldRect = pygame.Rect(
            ship.x - SHIP_SHIELD_ARC_DIAM/2 - camera_x_transform,
            ship.y - SHIP_SHIELD_ARC_DIAM/2 - camera_y_transform,
            SHIP_SHIELD_ARC_DIAM,
            SHIP_SHIELD_ARC_DIAM,
        )
        pygame.draw.arc(screen, scheme["shield"], shieldRect, 0, math.pi * 2 * (ship.shield/100.0), width=2)

    for _, laser_shot in game.active_laser_shots.items():
        shooter_ship = game.ships[laser_shot.shooter_ship_id]
        being_shot_ship = game.ships[laser_shot.being_shot_ship_id]
        pygame.draw.line(
            screen,
            scheme["laser"],
            (
                shooter_ship.x - camera_x_transform,
                shooter_ship.y - camera_y_transform
            ),
            (
                being_shot_ship.x - camera_x_transform,
                being_shot_ship.y - camera_y_transform
            ),
            width=1
        )

    if game.ship_id and game.ships[game.ship_id].dead:
        pygame.draw.rect(screen, scheme["death_overlay"], screenRect)
