from common.messages.ship_damage import ShipDamageMessage
from common.space import LaserShot
from server.id import new_id
from server.sessions.sessions import queue_message_for_broadcast


def tick(systems, ticks):
    for _, system in systems.items():
        system.tick()
        system.active_laser_shots = get_new_laser_shots(system, ticks)
        resolve_laser_damage(system)

def resolve_laser_damage(system):
    for _id, shot in system.active_laser_shots.items():
        target_ship = system.ships[shot.being_shot_ship_id]
        apply_damage_to_ship(target_ship, shot.power)

def get_new_laser_shots(system, ticks):
    shots = {}
    for _, ship in system.ships.items():
        if ship.targeting_ship_id and ship.targeting_ship_id > -1:

            if ship.targeting_ship_id not in system.ships:
                ship.targeting_ship_id = -1
                continue

            time_since_last_shot = ticks - ship.last_shot_time
            if time_since_last_shot * ship.shot_frequency >= 1.0:
                shot = LaserShot(ship.id, ship.targeting_ship_id, 5, id_fun=new_id)
                shots[shot.id] = shot
                ship.last_shot_time = ticks
    return shots

def apply_damage_to_ship(ship, damage):
    ship.health -= damage
    death = False
    if ship.health <= 0:
        ship.health = 0
        death = True
        ship.dead = True

    queue_message_for_broadcast(ShipDamageMessage(ship.id, damage, death=death))
