from common.const import ENGINE_POWER_DAMAGE_THRESHOLD, ENGINE_DAMAGE_INCREASE_RATE, get_laser_range
from common.messages.explosion import ExplosionMessage
from common.messages.ship_damage import ShipDamageMessage
from common.utils import dist
from server.game.slot_types.slot_types import resolve_slot_tick
from server.sessions.sessions import queue_message_for_broadcast


def tick(systems, ticks):

    for _, system in systems.items():
        system.active_laser_shots = {}
        system.tick()

        # tick_ship_slots
        all_ship_ids = list(system.ships.keys())
        for ship_id, ship in system.ships.items():
            all_slots = ship.weapon_slots | ship.hull_slots | ship.shield_slots | ship.engine_slots
            for slot in all_slots.values():
                slot.target_ids = [target_id for target_id in slot.target_ids if target_id in all_ship_ids]
                resolve_slot_tick(system, ship_id, slot, ticks)


        exploded_missiles = []
        for missile_id, missile in system.in_flight_missiles.items():
            if missile.exploded:
                exploded_missiles.append(missile_id)

        for missile_id in exploded_missiles:
            del system.in_flight_missiles[missile_id]

        _resolve_laser_damage(system)
        missiles_to_detonate = _get_detonatable_missiles(system)

        for missile_id in missiles_to_detonate:
            _detonate_missile(system, missile_id)

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
    missile.exploded = True
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

def _resolve_laser_damage(system):
    for _id, shot in system.active_laser_shots.items():
        shooting_ship = system.ships[shot.shooter_ship_id]
        target_ship = system.ships[shot.being_shot_ship_id]
        range = dist(target_ship.x, target_ship.y, shooting_ship.x, shooting_ship.y)
        laser_range = get_laser_range()

        if not shot.miss and not shooting_ship.dead and not target_ship.dead and range <= laser_range:
            target_ship = system.ships[shot.being_shot_ship_id]
            _apply_damage_to_ship(target_ship, shot.power)

def _apply_damage_to_ship(ship, damage):
    death = False
    modified_damage = damage + _get_additional_damage_from_target_multipliers(ship, damage)
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