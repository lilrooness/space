import random

from common.const import LASER_TURRET, BASE_LASER_RANGE, get_speed, BASE_LASER_DAMAGE, MISSILE_LAUNCHER, \
    BASE_MISSILE_RANGE, BASE_MISSILE_DAMAGE
from common.entities.inflight_missile import InFlightMissile
from common.entities.laser_shot import LaserShot
from common.utils import dist, get_transversal_from_perspective_of_a
from server.id import new_id

BASE_LASER_MISS_CHANCE = 0.1
LASER_SHOT_FREQUENCY = 0.05
MISSILE_SHOT_FREQUENCY = 0.025

def slot_type_can_target(systems, owner_session, slot_type_id, target_id):
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


def set_slot_target(slot, target_id):
    if slot.type_id == LASER_TURRET:
        slot.target_ids = [target_id]
    if slot.type_id == MISSILE_LAUNCHER:
        slot.target_ids = [target_id]

def resolve_slot_tick(system, owner_id, slot, tick):
    if not slot.type_id:
        return

    owner_ship = system.ships[owner_id]
    type_id = slot.type_id

    if type_id == MISSILE_LAUNCHER:

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
                miss_chance = transversal_velocity * 10 * BASE_LASER_MISS_CHANCE

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

