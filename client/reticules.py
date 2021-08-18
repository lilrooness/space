import pygame

from client.camera import world_to_screen
from client.const import RETICULE_SIZE, scheme
from common.ballistics import get_mini_gun_miss_chance, get_laser_turret_miss_chance
from common.const import MISSILE_LAUNCHER, MINI_GUN, get_speed, LASER_TURRET
from common.utils import get_transversal_from_perspective_of_a


def draw_targetted_reticule(screen, game, slot_type_id, target_ship_id):

    target_ship = game.ships[target_ship_id]
    targetting_ship = game.ships[game.ship_id]

    owner_vx = targetting_ship.vx * get_speed(targetting_ship.power_allocation_engines)
    owner_vy = targetting_ship.vy * get_speed(targetting_ship.power_allocation_engines)

    target_vx = target_ship.vx * get_speed(target_ship.power_allocation_engines)
    target_vy = target_ship.vy * get_speed(target_ship.power_allocation_engines)

    transversal_velocity = get_transversal_from_perspective_of_a(
        targetting_ship.x,
        targetting_ship.y,
        owner_vx,
        owner_vy,
        target_ship.x,
        target_ship.y,
        target_vx,
        target_vy
    )

    target_ship_screen_space_coords = world_to_screen(
        game,
        game.ships[target_ship_id].x,
        game.ships[target_ship_id].y,
    )

    if slot_type_id == MISSILE_LAUNCHER:
        reticule = pygame.Rect(target_ship_screen_space_coords[0] - RETICULE_SIZE / 2,
                               target_ship_screen_space_coords[1] - RETICULE_SIZE / 2, RETICULE_SIZE, RETICULE_SIZE)
        pygame.draw.rect(screen, scheme["targeted_reticule"], reticule, width=2)
    if slot_type_id == MINI_GUN:

        miss_chance = get_mini_gun_miss_chance(transversal_velocity)
        max_size = RETICULE_SIZE * 1.5
        size = max(20, miss_chance * max_size)
        reticule = pygame.Rect(target_ship_screen_space_coords[0] - size / 2,
                               target_ship_screen_space_coords[1] - size / 2, size, size)
        pygame.draw.rect(screen, scheme["targeted_reticule"], reticule, width=2)
    if slot_type_id == LASER_TURRET:
        miss_chance = get_laser_turret_miss_chance(transversal_velocity)
        max_size = RETICULE_SIZE * 1.5
        size = max(20, miss_chance * max_size)

        pygame.draw.circle(screen, scheme["targeted_reticule"], target_ship_screen_space_coords, size, width=2)


def draw_hover_reticule(screen, game, target_ship_id):
    target_ship_screen_space_coords = world_to_screen(
        game,
        game.ships[target_ship_id].x,
        game.ships[target_ship_id].y,
    )

    reticule = pygame.Rect(target_ship_screen_space_coords[0] - RETICULE_SIZE / 2,
                           target_ship_screen_space_coords[1] - RETICULE_SIZE / 2, RETICULE_SIZE, RETICULE_SIZE)
    pygame.draw.rect(screen, scheme["hover_reticule"], reticule, width=2)