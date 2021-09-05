import random

from common.ballistics import get_laser_turret_miss_chance, get_mini_gun_miss_chance
from common.const import LASER_TURRET, BASE_LASER_RANGE, get_speed, BASE_LASER_DAMAGE, MISSILE_LAUNCHER, \
    BASE_MISSILE_RANGE, BASE_MISSILE_DAMAGE, MINI_GUN, BASE_MINI_GUN_RANGE, BASE_MINI_GUN_VELOCITY, \
    MINI_GUN_SHOT_FREQUENCY, MISSILE_SHOT_FREQUENCY, LASER_SHOT_FREQUENCY, SHIELD_REPAIRER, MAX_SHIELD_HEALTH, \
    HULL_REPAIRER, MAX_HULL_HEALTH, SHIELD_REPAIRER_FREQUENCY, SHIELD_REPAIRER_HEAL_AMOUNT, HULL_REPAIRER_FREQUENCY, \
    HULL_REPAIRER_HEAL_AMOUNT
from common.entities.inflight_missile import InFlightMissile
from common.entities.laser_shot import LaserShot
from common.entities.mini_gun_shot import MinigunShot
from common.utils import dist, get_transversal_from_perspective_of_a, get_radial_velocity
from server.id import new_id


def slot_type_can_target(systems, owner_session, slot_type_id, target_id):

    if slot_type_id == SHIELD_REPAIRER:
        system = systems[owner_session.solar_system_id]
        target_ship = system.ships[target_id]
        if owner_session.ship_id == target_id and target_ship.shield < MAX_SHIELD_HEALTH:
            return True
        else:
            return False

    if slot_type_id == HULL_REPAIRER:
        system = systems[owner_session.solar_system_id]
        target_ship = system.ships[target_id]
        if owner_session.ship_id == target_id and target_ship.health < MAX_HULL_HEALTH:
            return True
        else:
            return False

    if slot_type_id == LASER_TURRET:
        if owner_session.ship_id != target_id:
            if target_id not in systems[owner_session.solar_system_id].ships:
                return False

            owner_ship = systems[owner_session.solar_system_id].ships[owner_session.ship_id]
            target_ship = systems[owner_session.solar_system_id].ships[target_id]

            if dist(owner_ship.x, owner_ship.y, target_ship.x, target_ship.y) <= BASE_LASER_RANGE:
                return True
    if slot_type_id == MISSILE_LAUNCHER:
        if owner_session.ship_id != target_id:
            if target_id not in systems[owner_session.solar_system_id].ships:
                return False

            owner_ship = systems[owner_session.solar_system_id].ships[owner_session.ship_id]
            target_ship = systems[owner_session.solar_system_id].ships[target_id]

            if dist(owner_ship.x, owner_ship.y, target_ship.x, target_ship.y) <= BASE_MISSILE_RANGE:
                return True
    if slot_type_id == MINI_GUN:
        if owner_session.ship_id != target_id:
            if target_id not in systems[owner_session.solar_system_id].ships:
                return False

            owner_ship = systems[owner_session.solar_system_id].ships[owner_session.ship_id]
            target_ship = systems[owner_session.solar_system_id].ships[target_id]

            if dist(owner_ship.x, owner_ship.y, target_ship.x, target_ship.y) <= BASE_MINI_GUN_RANGE:
                return True


def set_slot_target(slot, target_id):
    if slot.type_id == LASER_TURRET:
        slot.target_ids = [target_id]
    if slot.type_id == MISSILE_LAUNCHER:
        slot.target_ids = [target_id]
    if slot.type_id == MINI_GUN:
        slot.target_ids = [target_id]
    if slot.type_id == SHIELD_REPAIRER:
        slot.target_ids = [target_id]
    if slot.type_id == HULL_REPAIRER:
        slot.target_ids = [target_id]

def resolve_slot_tick(system, owner_id, slot, tick):
    if not slot.type_id:
        return

    owner_ship = system.ships[owner_id]
    type_id = slot.type_id

    if type_id == SHIELD_REPAIRER:
        if slot.target_ids:
            pulse_now = False

            if slot.ammo < 1:
                slot.target_ids = []
                return

            if system.ships[slot.target_ids[0]].dead:
                slot.target_ids = []
                return

            if "last_shot_tick" not in slot.userdata:
                pulse_now = True
            else:
                last_shot_tick = slot.userdata["last_shot_tick"]
                ticks_since_last_shot = tick - last_shot_tick
                if ticks_since_last_shot * SHIELD_REPAIRER_FREQUENCY >= 1.0:
                    pulse_now = True

            if pulse_now:
                slot.ammo -= 1
                slot.userdata["last_shot_tick"] = tick
                target_ship = system.ships[slot.target_ids[0]]
                target_ship.shield = min(MAX_SHIELD_HEALTH, target_ship.shield + SHIELD_REPAIRER_HEAL_AMOUNT)

    if type_id == HULL_REPAIRER:
        if slot.target_ids and slot.ammo > 0:
            pulse_now = False

            if slot.ammo < 1:
                slot.target_ids = []
                return

            if system.ships[slot.target_ids[0]].dead:
                slot.target_ids = []
                return

            if "last_shot_tick" not in slot.userdata:
                pulse_now = True
            else:
                last_shot_tick = slot.userdata["last_shot_tick"]
                ticks_since_last_shot = tick - last_shot_tick
                if ticks_since_last_shot * HULL_REPAIRER_FREQUENCY >= 1.0:
                    pulse_now = True

            if pulse_now:
                slot.ammo -= 1
                slot.userdata["last_shot_tick"] = tick
                target_ship = system.ships[slot.target_ids[0]]
                target_ship.health = min(MAX_HULL_HEALTH, target_ship.health + HULL_REPAIRER_HEAL_AMOUNT)

    if type_id == MINI_GUN:
        if slot.target_ids:
            shoot_now = False
            if system.ships[slot.target_ids[0]].dead:
                slot.target_ids = []
                return

            if "last_shot_tick" not in slot.userdata:
                shoot_now = True
            else:
                last_shot_tick = slot.userdata["last_shot_tick"]
                ticks_since_last_shot = tick - last_shot_tick
                if ticks_since_last_shot * MINI_GUN_SHOT_FREQUENCY >= 1.0:
                    shoot_now = True

            if shoot_now:
                slot.userdata["last_shot_tick"] = tick
                target_ship = system.ships[slot.target_ids[0]]
                owner_vx = owner_ship.vx * get_speed(owner_ship.power_allocation_engines)
                owner_vy = owner_ship.vy * get_speed(owner_ship.power_allocation_engines)

                target_vx = target_ship.vx * get_speed(target_ship.power_allocation_engines)
                target_vy = target_ship.vy * get_speed(target_ship.power_allocation_engines)

                transversal_velocity = get_transversal_from_perspective_of_a(
                    owner_ship.x,
                    owner_ship.y,
                    owner_vx,
                    owner_vy,
                    target_ship.x,
                    target_ship.y,
                    target_vx,
                    target_vy
                )
                miss_chance = get_mini_gun_miss_chance(transversal_velocity)
                missed = True
                if random.random() > miss_chance:
                    missed =  False

                radial_velocity = -1.0 * get_radial_velocity(
                    owner_ship.x,
                    owner_ship.y,
                    owner_vx,
                    owner_vy,
                    target_ship.x,
                    target_ship.y,
                    target_vx,
                    target_vy
                )
                shot = MinigunShot(
                    owner_ship.id,
                    target_ship.id,
                    BASE_MINI_GUN_VELOCITY + radial_velocity,
                    miss=missed,
                    id_fun=new_id
                )
                system.mini_gun_shots[shot.id] = shot

    elif type_id == MISSILE_LAUNCHER:

        if slot.target_ids:
            shoot_now = False
            if system.ships[slot.target_ids[0]].dead:
                slot.target_ids = []
                return

            if "last_shot_tick" not in slot.userdata:
                shoot_now = True
            else:
                last_shot_tick = slot.userdata["last_shot_tick"]
                ticks_since_last_shot = tick - last_shot_tick
                if ticks_since_last_shot * MISSILE_SHOT_FREQUENCY >= 1.0:
                    shoot_now = True

            if shoot_now:
                slot.userdata["last_shot_tick"] = tick
                new_missile = InFlightMissile(
                    damage=BASE_MISSILE_DAMAGE,
                    owner_id=owner_id,
                    target_id=slot.target_ids[0],
                    x=owner_ship.x,
                    y=owner_ship.y,
                    id_fun=new_id,
                )
                system.in_flight_missiles[new_missile.id] = new_missile


    elif type_id == LASER_TURRET:
        if slot.target_ids:
            shoot_now = False
            if system.ships[slot.target_ids[0]].dead:
                slot.target_ids = []
                return

            if "last_shot_tick" not in slot.userdata:
                shoot_now = True
            else:
                last_shot_tick = slot.userdata["last_shot_tick"]
                ticks_since_last_shot =  tick - last_shot_tick
                if ticks_since_last_shot * LASER_SHOT_FREQUENCY >= 1.0:
                    shoot_now = True

            if shoot_now:
                slot.userdata["last_shot_tick"] = tick
                target_ship = system.ships[slot.target_ids[0]]
                owner_vx = owner_ship.vx * get_speed(owner_ship.power_allocation_engines)
                owner_vy = owner_ship.vy * get_speed(owner_ship.power_allocation_engines)

                target_vx = target_ship.vx * get_speed(target_ship.power_allocation_engines)
                target_vy = target_ship.vy * get_speed(target_ship.power_allocation_engines)

                transversal_velocity = get_transversal_from_perspective_of_a(
                    owner_ship.x,
                    owner_ship.y,
                    owner_vx,
                    owner_vy,
                    target_ship.x,
                    target_ship.y,
                    target_vx,
                    target_vy
                )
                miss_chance = get_laser_turret_miss_chance(transversal_velocity)

                missed = True
                if random.random() > miss_chance:
                    missed =  False

                shot = LaserShot(
                    shooter_ship_id=owner_ship.id,
                    being_shot_ship_id=target_ship.id,
                    power=BASE_LASER_DAMAGE,
                    id_fun=new_id,
                    miss=missed,
                )

                system.active_laser_shots[shot.id] = shot

