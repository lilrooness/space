from datetime import datetime

from client import camera
from client.vfx.explosion_effect import ExplosionEffect
from client.vfx.minigun_shot_effect import MinigunShotEffect
from client.vfx.warp_effect import WarpEffect
from common.const import CRATE_LOOT_RANGE
from common.messages.crate_contents import CrateContentsMessage
from common.messages.explosion import ExplosionMessage
from common.messages.messages import ServerTickMessage
from client.const import SHIP_HEIGHT, SHIP_WIDTH
from common.messages.ship_damage import ShipDamageMessage
from common.messages.warp_exit_appeared import WarpExitAppearedMessage
from common.messages.warp_started import WarpStartedMessage
from common.net_const import SERVER_TICK_TIME
from common.utils import dist


class Game():

    def __init__(self, ships={}, ship_id=None, solar_system_id=None, resources=None):
        self.ships = ships
        self.ship_id = ship_id
        self.solar_system_id = solar_system_id
        self.resources = resources
        self.targeted_by_ship_id = None
        self.active_laser_shots = {}
        self.in_flight_missiles = {}
        self.mini_gun_shots_effects = []
        self.power_allocation_guns = 1.0
        self.power_allocation_shields = 0.0
        self.power_allocation_engines = 0.0
        self.tick_number = 0
        self.last_tick_time = datetime.now()
        self.last_delta = 0
        self.crates = {}
        self.crate_requests = []
        self.open_crates = []
        self.weapon_slots =[]
        self.shield_slots =[]
        self.engine_slots =[]
        self.hull_slots =[]
        self.selected_slot_id = None
        self.explosions = []
        self.warp_effects = []
        self.sensor_towers = {}
        self.sensor_tower_boost = False
        self.warp_points = {}
        self.speed_boost_clouds = {}
        self.server_tick_number = None
        self.dragged_item = None

    def tick(self):
        time_since_last_tick = datetime.now() - self.last_tick_time

        delta = min(1.0, float(time_since_last_tick.microseconds) / float(SERVER_TICK_TIME))

        if self.dragged_item:
            ship = self.ships[self.ship_id]
            crate = self.crates[self.dragged_item.crate_id]
            if dist(ship.x, ship.y, crate.x, crate.y) > CRATE_LOOT_RANGE:
                self.dragged_item = None

        for ship_id, ship in self.ships.items():
            ship.tick(
                delta=(delta - self.last_delta),
            )

        for missile_id, missile in self.in_flight_missiles.items():
            missile.tick(
                self.ships,
                delta=(delta - self.last_delta),
            )

        done_explosions = []
        for explosion in self.explosions:
            explosion.tick()
            if explosion.done:
                done_explosions.append(explosion)

        for explosion in done_explosions:
            self.explosions.remove(explosion)

        done_warp_effects = []
        for warp_effect in self.warp_effects:
            warp_effect.tick(self.tick_number, delta)
            if warp_effect.done:
                done_warp_effects.append(warp_effect)

        for warp_effect in done_warp_effects:
            self.warp_effects.remove(warp_effect)

        done_minigun_shots = []
        for shot in self.mini_gun_shots_effects:
            shot.tick(self)
            if shot.done:
                done_minigun_shots.append(shot)

        for shot in done_minigun_shots:
            self.mini_gun_shots_effects.remove(shot)

        self.last_delta = delta

def crate_minigun_shot_burst_effect(game, minigun_shot):
    origin_ship = game.ships[minigun_shot.shooter_ship_id]
    for i in range(100):
        game.mini_gun_shots_effects.append(
            MinigunShotEffect(
                minigun_shot.shooter_ship_id,
                minigun_shot.being_shot_ship_id,
                origin_ship.x,
                origin_ship.y,
                delay=i*1000,
            )
        )

def handle_server_tick_message(game, message):
    game.server_tick_number = message.server_tick_number
    game.last_delta = 0.0
    game.last_tick_time = datetime.now()
    game.tick_number += 1
    game.ship_id = message.ship_id
    game.solar_system_id = message.solar_system_id
    ships = {}

    for ship in message.ships:
        ships[ship.id] = ship

    active_laser_shots = {}
    for laser in message.active_laser_shots:
        active_laser_shots[laser.id] = laser

    in_flight_missiles = {}
    for missile in message.in_flight_missiles:
        in_flight_missiles[missile.id] = missile

    for shot in message.mini_gun_shots:
        if shot.being_shot_ship_id in game.ships and shot.shooter_ship_id in game.ships:
            crate_minigun_shot_burst_effect(game, shot)

    crates = {}
    for crate in message.crates:
        if crate.id in game.crates:
            crate.contents = game.crates[crate.id].contents
        crates[crate.id] = crate

    sensor_towers = {}
    for tower in message.sensor_towers:
        sensor_towers[tower.id] = tower

    warp_points = {}
    for warp_point in message.warp_points:
        warp_points[warp_point.id] = warp_point

    speed_boost_clouds = {}
    for sbc in message.speed_boost_clouds:
        speed_boost_clouds[sbc.id] = sbc

    game.active_laser_shots = active_laser_shots
    game.in_flight_missiles = in_flight_missiles
    game.ships = ships
    game.crates = crates
    game.sensor_towers = sensor_towers
    game.resources = message.resources
    game.power_allocation_shields = message.power_allocation_shields
    game.power_allocation_guns = message.power_allocation_guns
    game.power_allocation_engines = message.power_allocation_engines
    game.weapon_slots = message.weapon_slots
    game.shield_slots = message.shield_slots
    game.engine_slots = message.engine_slots
    game.hull_slots = message.hull_slots
    game.sensor_tower_boost = message.sensor_tower_boost
    game.warp_points = warp_points
    game.speed_boost_clouds = speed_boost_clouds

    if message.targeted_by_ship_id > -1:
        game.targeted_by_ship_id = message.targeted_by_ship_id
    else:
        game.targeted_by_ship_id = None

def handle_ship_damage_message(game, message):
    print("some damage init")

def handle_crate_contents_message(game, message):
    contents = {}
    for item in message.contents:
        contents[item.id] = item

    game.crates[message.crate_id].contents = contents
    if message.crate_id in game.crate_requests:
        game.crate_requests.remove(message.crate_id)

def handle_explosion_message(game, message):

    game.explosions.append(ExplosionEffect(
        message.x,
        message.y,
        message.radius,
    ))

def handle_warp_started_message(game, message):
    warping_ship = game.ships[message.ship_id]
    game.warp_effects.append(WarpEffect(
        game.tick_number,
        warping_ship.x,
        warping_ship.y,
        200,
        animation_ticks=message.ticks_to_complete,
    ))

def handle_warp_exit_appeared_message(game, message):
    game.warp_effects.append(WarpEffect(
        game.tick_number,
        message.x,
        message.y,
        200,
        animation_ticks=message.ticks_to_complete,
    ))

def pick_ship(game, ship, mouse):
    shipX, shipY = camera.world_to_screen(game, ship.x, ship.y)
    if mouse.x >= shipX - SHIP_WIDTH/2 and mouse.x <= shipX + SHIP_WIDTH/2:
        if mouse.y >= shipY - SHIP_HEIGHT/2 and mouse.y <= shipY + SHIP_HEIGHT/2:
            return True
    return False



message_handlers = {
    ServerTickMessage: handle_server_tick_message,
    ShipDamageMessage: handle_ship_damage_message,
    CrateContentsMessage: handle_crate_contents_message,
    ExplosionMessage: handle_explosion_message,
    WarpStartedMessage: handle_warp_started_message,
    WarpExitAppearedMessage: handle_warp_exit_appeared_message,
}
