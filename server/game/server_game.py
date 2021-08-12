from common.const import ENGINE_POWER_DAMAGE_THRESHOLD, ENGINE_DAMAGE_INCREASE_RATE, get_laser_range, \
    BASE_MINI_GUN_RANGE, BASE_MINI_GUN_VELOCITY, BASE_MINI_GUN_DAMAGE, BASE_SENSOR_RANGE
from common.entities.sensor_tower import ACTIVATION_TICK_AMOUNT
from common.messages.explosion import ExplosionMessage
from common.messages.ship_damage import ShipDamageMessage
from common.utils import dist
from server.game.slot_types.slot_types import resolve_slot_tick
from server.sessions.sessions import queue_message_for_broadcast


def tick(systems, ticks):

    for _, system in systems.items():
        system.active_laser_shots = {}
        system.tick(tick=ticks)

        # tick_ship_slots
        all_ship_ids = list(system.ships.keys())
        for ship_id, ship in system.ships.items():
            all_slots = ship.weapon_slots | ship.hull_slots | ship.shield_slots | ship.engine_slots
            for slot in all_slots.values():
                slot.target_ids = [target_id for target_id in slot.target_ids if target_id in all_ship_ids]
                resolve_slot_tick(system, ship_id, slot, ticks)

        _resolve_laser_damage(system)
        _resolve_mini_gun_damage(system)
        missiles_to_detonate = _get_detonatable_missiles(system)

        for missile_id in missiles_to_detonate:
            _detonate_missile(system, missile_id)
            del system.in_flight_missiles[missile_id]

        for _tower_id, tower in system.sensor_towers.items():
            tick_tower(tower, system)

def get_ship_ids_in_range_of_point(system, x, y, range, exclude_dead=False):
    ids = []
    for _, ship in system.ships.items():
        if exclude_dead:
            if ship.dead:
                continue
        if dist(x, y, ship.x, ship.y) <= range:
            ids.append(ship.id)

    return ids


def get_ship_ids_in_sensor_range_of_point(system, x, y):
    ids = []
    for _, ship in system.ships.items():
        if dist(x, y, ship.x, ship.y) <= BASE_SENSOR_RANGE:
            ids.append(ship.id)

    return ids

def get_ship_ids_in_sensor_range_of_ship(system, ship_id):
    ids = []
    this_ship = system.ships[ship_id]
    for _, ship in system.ships.items():
        if ship.id is not ship_id and dist(ship.x, ship.y, this_ship.x, this_ship.y) <= BASE_SENSOR_RANGE:
            ids.append(ship.id)

    return ids

def _get_detonatable_missiles(system):

    detonated_missile_ids = []

    for missile_id, missile in system.in_flight_missiles.items():
            target_ship = system.ships[missile.target_id]

            if missile.ticks_alive >= missile.max_flight_ticks:
                detonated_missile_ids.append(missile_id)
            elif dist(missile.x, missile.y, target_ship.x, target_ship.y) < missile.explosion_range:
                detonated_missile_ids.append(missile_id)

    return detonated_missile_ids


def _detonate_missile(system, missile_id):
    missile = system.in_flight_missiles[missile_id]
    # get all ships in range
    for _id, ship in system.ships.items():
        if dist(missile.x, missile.y, ship.x, ship.y) <= missile.explosion_range:
            _apply_damage_to_ship(ship, missile.damage)

    queue_message_for_broadcast(
        ExplosionMessage(
            missile.x,
            missile.y,
            radius=missile.explosion_range,
        )
    )

def _resolve_mini_gun_damage(system):
    for _id, shot in system.mini_gun_shots.items():
        if shot.resolved:
            continue
        shooting_ship = system.ships[shot.shooter_ship_id]
        target_ship = system.ships[shot.being_shot_ship_id]
        range = dist(target_ship.x, target_ship.y, shooting_ship.x, shooting_ship.y)

        if not shot.miss and not target_ship.dead and range <= BASE_MINI_GUN_RANGE:
            velocityDamageModifier = shot.velocity / BASE_MINI_GUN_VELOCITY * 2
            damage = velocityDamageModifier * BASE_MINI_GUN_DAMAGE
            _apply_damage_to_ship(target_ship, damage)

        shot.resolved = True

# TODO: shorter distance means more damage
def _resolve_laser_damage(system):
    for _id, shot in system.active_laser_shots.items():
        shooting_ship = system.ships[shot.shooter_ship_id]
        target_ship = system.ships[shot.being_shot_ship_id]
        range = dist(target_ship.x, target_ship.y, shooting_ship.x, shooting_ship.y)
        laser_range = get_laser_range()

        if not shot.miss and not shooting_ship.dead and not target_ship.dead and range <= laser_range:
            _apply_damage_to_ship(target_ship, shot.power)

def _apply_damage_to_ship(ship, damage):
    death = False
    modified_damage = damage# + _get_additional_damage_from_target_multipliers(ship, damage)
    shield_after_damage = max(ship.shield - modified_damage, 0)
    if shield_after_damage == 0:
        damage_after_shield = max(modified_damage - ship.shield, 0)
        ship.health = max(ship.health - damage_after_shield, 0)
        if ship.health == 0:
            death = True
            ship.dead = True

    ship.shield = shield_after_damage

    queue_message_for_broadcast(ShipDamageMessage(ship.id, modified_damage, death=death))

def _get_additional_damage_from_target_multipliers(ship, damage):
    enginePowerAboveDamageThreshold = max(0, ship.power_allocation_engines - ENGINE_POWER_DAMAGE_THRESHOLD)

    return enginePowerAboveDamageThreshold * ENGINE_DAMAGE_INCREASE_RATE * damage

def does_ship_have_sensor_tower_buff(system, ship_id):
    activated_towers = 0
    for _, tower in system.sensor_towers.items():
        if tower.online and tower.last_charged_by == ship_id:
            activated_towers += 1

    if activated_towers == len(system.sensor_towers):
        return True
    else:
        return False

def tick_tower(tower, system):

    ship_ids_in_range = get_ship_ids_in_range_of_point(
        system,
        tower.x,
        tower.y,
        tower.connection_range,
        exclude_dead=True
    )

    if tower.percent_activated == 0.0:
        tower.online = False
    elif tower.percent_activated == 1.0:
        tower.online = True

    if not ship_ids_in_range:
        tower.percent_activated = max(0.0, tower.percent_activated - ACTIVATION_TICK_AMOUNT/3)
    elif len(ship_ids_in_range) == 1:
        tower.connected_ship_id = ship_ids_in_range[0]

        if tower.percent_activated == 0.0:
            tower.last_charged_by = tower.connected_ship_id

        if tower.last_charged_by != tower.connected_ship_id:
            tower.percent_activated = max(0.0, tower.percent_activated - ACTIVATION_TICK_AMOUNT)
        elif tower.last_charged_by == tower.connected_ship_id:
            tower.percent_activated = min(1.0, tower.percent_activated + ACTIVATION_TICK_AMOUNT)

    elif len(ship_ids_in_range) > 1:
        if tower.last_charged_by in ship_ids_in_range:
            tower.percent_activated = tower.percent_activated
        else:
            tower.percent_activated = max(0.0, tower.percent_activated - ACTIVATION_TICK_AMOUNT)
