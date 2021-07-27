import math

import pygame

from client.camera import get_camera_zoom, world_to_screen
from client.const import scheme, SHIP_HEALTH_ARC_DIAM, SHIP_SHIELD_ARC_DIAM, RETICULE_SIZE
from client.game import pick_ship
from client.mouse import get_mouse
from client.ui.power_window.power_window import power_window
from common.const import get_laser_range


def render_static_ui(game, screen, old_state):
    state = power_window(game, screen, old_state)
    return state

def render_game(game, screen, screenRect):
    pygame.draw.rect(screen, scheme["background"], screenRect)

    if get_camera_zoom() < 8:
        render_game_view(game, screen, screenRect)
    else:
        render_map_view(game, screen, screenRect)

def render_map_view(game, screen, _screenRect):
    for ship_id, ship in game.ships.items():
        ship_screen_space_coords = world_to_screen(
            game,
            ship.x,
            ship.y,
        )

        color = scheme["map_other"]

        if ship_id == game.ship_id:
            color = scheme["map_me"]

        pygame.draw.circle(screen, color, ship_screen_space_coords, 2)

def render_game_view(game, screen, screenRect):
    ship = game.ships[game.ship_id]

    grid_width = 500
    grid_height = 500

    x_step = 100 / get_camera_zoom()
    y_step = 100 / get_camera_zoom()

    for x in range(grid_width):
        if x == 0:
            continue
        xpos = x_step * x - ship.x
        pygame.draw.line(
            screen,
            scheme["foreground"],
            world_to_screen(game, xpos, 0),
            world_to_screen(game, xpos, grid_height*y_step),
            width=1,
        )

    for y in range(grid_height):
        if y == 0:
            continue
        ypos = y_step * y - ship.y
        pygame.draw.line(
            screen,
            scheme["foreground"],
            world_to_screen(game, 0, ypos),
            world_to_screen(game, grid_width*x_step, ypos),
            width=1
        )

    session_ship_screen_space_coords = world_to_screen(
        game,
        ship.x,
        ship.y,
    )

    laser_range = get_laser_range(game.power_allocation_guns) / float(get_camera_zoom())
    laserRangeRect = pygame.Rect(
        session_ship_screen_space_coords[0] - laser_range,
        session_ship_screen_space_coords[1] - laser_range,
        laser_range * 2,
        laser_range * 2,
    )
    pygame.draw.arc(screen, scheme["range_marker"], laserRangeRect, 0, math.pi * 2, width=1)

    for ship_id, ship in game.ships.items():

        ship_screen_space_coords = world_to_screen(
            game,
            ship.x,
            ship.y,
        )

        reticule = pygame.Rect(ship_screen_space_coords[0] - RETICULE_SIZE/2, ship_screen_space_coords[1] - RETICULE_SIZE/2, RETICULE_SIZE, RETICULE_SIZE)
        if ship_id == game.targeting_ship_id:
            pygame.draw.rect(screen, scheme["targeted_reticule"], reticule, width=2)
        if ship_id != game.ship_id and pick_ship(game, ship, get_mouse()):
            pygame.draw.rect(screen, scheme["hover_reticule"], reticule, width=2)

        pygame.draw.circle(screen, scheme["entity"], world_to_screen(game, ship.x, ship.y), 5)

        healthRect = pygame.Rect(
            ship_screen_space_coords[0] - SHIP_HEALTH_ARC_DIAM / 2,
            ship_screen_space_coords[1] - SHIP_HEALTH_ARC_DIAM / 2,
            SHIP_HEALTH_ARC_DIAM,
            SHIP_HEALTH_ARC_DIAM,
        )
        pygame.draw.arc(screen, scheme["health"], healthRect, 0, math.pi * 2 * (ship.health/100.0), width=2)

        shieldRect = pygame.Rect(
            ship_screen_space_coords[0] - SHIP_SHIELD_ARC_DIAM / 2,
            ship_screen_space_coords[1] - SHIP_SHIELD_ARC_DIAM / 2,
            SHIP_SHIELD_ARC_DIAM,
            SHIP_SHIELD_ARC_DIAM,
        )
        pygame.draw.arc(screen, scheme["shield"], shieldRect, 0, math.pi * 2 * (ship.shield/100.0), width=2)

    for _, laser_shot in game.active_laser_shots.items():
        shooter_ship = game.ships[laser_shot.shooter_ship_id]
        being_shot_ship = game.ships[laser_shot.being_shot_ship_id]
        world_to_screen(game, being_shot_ship.x, being_shot_ship.y)
        pygame.draw.line(
            screen,
            scheme["laser"],
            world_to_screen(game, shooter_ship.x, shooter_ship.y),
            world_to_screen(game, being_shot_ship.x, being_shot_ship.y),
            width=1
        )

    if game.ship_id and game.ships[game.ship_id].dead:
        pygame.draw.rect(screen, scheme["death_overlay"], screenRect)
