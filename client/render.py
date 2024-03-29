import math

import pygame

from client.camera import get_camera_zoom, world_to_screen
from client.const import scheme, SHIP_HEALTH_ARC_DIAM, SHIP_SHIELD_ARC_DIAM, CRATE_WIDTH, CRATE_HEIGHT, \
    TOWER_WIDTH, TOWER_HEIGHT, LOOT_ICON_WIDTH, LOOT_ICON_HEIGHT
from client.game import pick_ship
from client.mouse import get_mouse
from client.reticules import draw_hover_reticule, draw_targetted_reticule
from client.ui.action_bar.action_bar import action_bar
from client.ui.components.icon import icon
from client.ui.crate_window.crate_window import crate_window
from client.ui.power_window.power_window import power_window
from client.ui.slot_window.slot_window import slot_window
from client.ui.tower_ui.tower_ui import tower_ui
from common.const import get_laser_range, CRATE_LOOT_RANGE, BASE_SENSOR_RANGE, SPEED_BOOST_CLOUD_RANGE
from common.utils import dist


def render_static_ui(game, screen, old_state, font):
    client_ship = game.ships[game.ship_id]

    state = power_window(game, screen, old_state)

    for crate_id, crate in game.crates.items():
        dist_to_crate = dist(client_ship.x, client_ship.y, crate.x, crate.y)
        if dist_to_crate <= CRATE_LOOT_RANGE:
            crate_window(game, screen, font, crate_id)

    for tower_id, _tower in game.sensor_towers.items():
        tower_ui(game, screen, tower_id)

    slot_window(screen, game, 50, 50)
    action_bar(screen, game, font)

    if game.dragged_item:
        mouse = get_mouse()

        icon(
            screen,
            game.dragged_item.type_id,
            pygame.Rect(
                mouse.x,
                mouse.y,
                LOOT_ICON_WIDTH,
                LOOT_ICON_HEIGHT
            )
        )

    return state

def render_game(game, screen, screenRect):
    background_color = scheme["background"]

    if game.sensor_tower_boost:
        background_color = scheme["sensor_tower_boost_background"]

    pygame.draw.rect(screen, background_color, screenRect)

    if get_camera_zoom() < 8:
        render_game_view(game, screen, screenRect)
    else:
        render_map_view(game, screen, screenRect)

def render_map_view(game, screen, _screenRect):
    this_ship = game.ships[game.ship_id]

    if not game.sensor_tower_boost:
        pygame.draw.circle(screen, scheme["sensor_range_marker"], world_to_screen(game, this_ship.x, this_ship.y),
                           BASE_SENSOR_RANGE / float(get_camera_zoom()), width=1)

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

    for _id, crate in game.crates.items():
        crate_screen_space_coords = world_to_screen(game, crate.x, crate.y)
        pygame.draw.circle(screen, scheme["crate"], crate_screen_space_coords, 2)

    for _id, tower in game.sensor_towers.items():
        tower_screen_space_coords = world_to_screen(game, tower.x, tower.y)
        pygame.draw.circle(screen, scheme["sensor_tower"], tower_screen_space_coords, 2)
        pygame.draw.circle(screen, scheme["sensor_tower_range"], tower_screen_space_coords, tower.connection_range / float(get_camera_zoom()), width=1)

    for _, warp_point in game.warp_points.items():
        warp_point_space_coords = world_to_screen(game, warp_point.x, warp_point.y)
        pygame.draw.circle(screen, scheme["warp_point"], warp_point_space_coords, 2)
        pygame.draw.circle(screen, scheme["warp_point_range"], warp_point_space_coords, warp_point.range / get_camera_zoom(), width=1)

def render_game_view(game, screen, screenRect):
    ship = game.ships[game.ship_id]

    session_ship_screen_space_coords = world_to_screen(
        game,
        ship.x,
        ship.y,
    )

    laser_range = get_laser_range() / float(get_camera_zoom())
    laserRangeRect = pygame.Rect(
        session_ship_screen_space_coords[0] - laser_range,
        session_ship_screen_space_coords[1] - laser_range,
        laser_range * 2,
        laser_range * 2,
    )
    pygame.draw.arc(screen, scheme["range_marker"], laserRangeRect, 0, math.pi * 2, width=1)

    if not game.sensor_tower_boost:
        pygame.draw.circle(screen, scheme["sensor_range_marker"], world_to_screen(game, ship.x, ship.y), BASE_SENSOR_RANGE / float(get_camera_zoom()), width=1)

    for ship_id, ship in game.ships.items():

        ship_screen_space_coords = world_to_screen(
            game,
            ship.x,
            ship.y,
        )

        for slot in game.weapon_slots:
            if ship_id in slot.target_ids:
                draw_targetted_reticule(screen, game, slot.type_id, ship_id)

        if pick_ship(game, ship, get_mouse()):
            draw_hover_reticule(screen, game, ship_id)

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
        pygame.draw.line(
            screen,
            scheme["laser"],
            world_to_screen(game, shooter_ship.x, shooter_ship.y),
            world_to_screen(game, being_shot_ship.x, being_shot_ship.y),
            width=1
        )

    for _, missile in game.in_flight_missiles.items():
        pygame.draw.circle(screen, scheme["entity"], world_to_screen(game, missile.x, missile.y), 1)

    for shot in game.mini_gun_shots_effects:
        if not shot.done:
            pygame.draw.circle(screen, scheme["entity"], world_to_screen(game, shot.x, shot.y), 1)

    for explosion in game.explosions:
        pygame.draw.circle(screen, scheme["explosion_radius"], world_to_screen(game, explosion.x, explosion.y), explosion.radius/get_camera_zoom(), width=1)
        pygame.draw.circle(screen, scheme["explosion_frontier"], world_to_screen(game, explosion.x, explosion.y),
                           explosion.drawRadius / get_camera_zoom(), width=1)

    for warp_effect in game.warp_effects:
        pygame.draw.circle(screen, scheme["explosion_radius"], world_to_screen(game, warp_effect.x, warp_effect.y),
                           warp_effect.radius / get_camera_zoom(), width=1)
        pygame.draw.circle(screen, scheme["explosion_frontier"], world_to_screen(game, warp_effect.x, warp_effect.y),
                           warp_effect.drawRadius / get_camera_zoom(), width=1)


    for _, warp_point in game.warp_points.items():
        warp_point_space_coords = world_to_screen(game, warp_point.x, warp_point.y)

        pygame.draw.circle(screen, scheme["warp_point"], warp_point_space_coords, 20)
        pygame.draw.circle(screen, scheme["warp_point_range"], warp_point_space_coords, warp_point.range / get_camera_zoom(), width=2)

    for _, tower in game.sensor_towers.items():
        tower_screen_space_coords = world_to_screen(game, tower.x, tower.y)
        tower_rect = pygame.Rect(
            tower_screen_space_coords[0] - TOWER_WIDTH/2,
            tower_screen_space_coords[1] - TOWER_HEIGHT/2,
            TOWER_WIDTH,
            TOWER_HEIGHT,
        )
        pygame.draw.rect(screen, scheme["sensor_tower"], tower_rect)
        pygame.draw.circle(screen, scheme["sensor_tower_range"], tower_screen_space_coords,
                           tower.connection_range / float(get_camera_zoom()), width=1)


    for _, cloud in game.speed_boost_clouds.items():
        cloud_screen_coords = world_to_screen(game, cloud.x, cloud.y)
        pygame.draw.circle(screen, scheme["speed_boost_cloud_range"], cloud_screen_coords, SPEED_BOOST_CLOUD_RANGE / float(get_camera_zoom()), width=1)


    for _, crate in game.crates.items():
        crate_screen_space_cords = world_to_screen(game, crate.x, crate.y)
        crate_rect = pygame.Rect(
            crate_screen_space_cords[0] - CRATE_WIDTH/2,
            crate_screen_space_cords[1] - CRATE_HEIGHT/2,
            CRATE_WIDTH,
            CRATE_HEIGHT,
        )
        if crate.open:
            pygame.draw.rect(screen, scheme["crate"], crate_rect, width=1)
        else:
            pygame.draw.rect(screen, scheme["crate"], crate_rect)

        screen_loot_range_diam = CRATE_LOOT_RANGE/get_camera_zoom() * 2
        loot_range_rect = pygame.Rect(
            crate_screen_space_cords[0] - screen_loot_range_diam/2,
            crate_screen_space_cords[1] - screen_loot_range_diam/2,
            screen_loot_range_diam,
            screen_loot_range_diam,
        )
        pygame.draw.arc(screen, scheme["crate"], loot_range_rect, 0, math.pi*2)

    if game.ship_id and game.ships[game.ship_id].dead:
        pygame.draw.rect(screen, scheme["death_overlay"], screenRect)
