import pygame
import yaml

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

SHIP_WIDTH = 20
SHIP_HEIGHT = 20

RETICULE_SIZE = 50

SHIP_HEALTH_ARC_DIAM = 20
SHIP_SHIELD_ARC_DIAM = 30

CRATE_WIDTH = 10
CRATE_HEIGHT = 10

TOWER_WIDTH = 10
TOWER_HEIGHT = 30

LOOT_ICON_WIDTH = 50
LOOT_ICON_HEIGHT = 50

scheme = {
    "background": BLACK,
    "sensor_tower_boost_background": GRAY,
    "entity": WHITE,
    "map_me": GREEN,
    "map_other": RED,
    "foreground": GRAY,
    "hover_reticule": YELLOW,
    "targeted_reticule": PINK,
    "targeted_by_reticule": RED,
    "laser": YELLOW,
    "death_overlay": RED_TRANSPARENT,
    "health": WHITE,
    "shield": CYAN,
    "ui_background": GRAY,
    "ui_boarder": LIGHT_GRAY,
    "ui_boarder_highlight": WHITE,
    "ui_boarder_selected": YELLOW,
    "ui_background_highlight": LIGHT_GRAY,
    "engines_power": RED,
    "shields_power": CYAN,
    "guns_power": YELLOW,
    "power": WHITE,
    "button_idle": DARK_GRAY,
    "button_hover": LIGHT_GRAY,
    "button_down": BLACK,
    "range_marker": YELLOW,
    "sensor_range_marker": LIGHT_GRAY,
    "crate": WHITE,
    "banner_background": DARK_GRAY,
    "banner_foreground": WHITE,
    "explosion_radius": RED,
    "explosion_frontier": CYAN,
    "sensor_tower": CYAN,
    "sensor_tower_range": LIGHT_GRAY,
    "online_tower_gauge": CYAN,
    "offline_tower_gauge": WHITE,
}

loot_type_icons = {}

def load_types():
    global loot_type_icons

    types = []
    with open('data/types.yaml') as file:
        types = yaml.safe_load(file)

    for type in types:
        loot_type_icons[type["type_id"]] = type["icon_path"]
