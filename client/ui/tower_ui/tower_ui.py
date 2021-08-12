import pygame

from client.camera import world_to_screen
from client.const import TOWER_HEIGHT, scheme
from client.ui.components.gauge import gauge


def tower_ui(game, screen, tower_id):
    tower = game.sensor_towers[tower_id]
    tower_screen_space_coords = world_to_screen(game, tower.x, tower.y)
    gauge_width = 50
    gauge_height = 10
    gauge_cont_rect = pygame.Rect(
        tower_screen_space_coords[0] - gauge_width/2,
        tower_screen_space_coords[1] - TOWER_HEIGHT/2 - gauge_height*2,
        gauge_width,
        gauge_height,
    )

    if tower.online:
        foregound_color = scheme["online_tower_gauge"]
    else:
        foregound_color = scheme["offline_tower_gauge"]

    gauge(
        screen,
        scheme["ui_background"],
        foregound_color,
        gauge_cont_rect,
        tower.percent_activated,
        verticle=False
    )


