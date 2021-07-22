from common.space import LaserShot
from server.id import new_id


def get_new_laser_shots(system, ticks):
    shots = {}
    for _, ship in system.ships.items():
        if ship.targeting_ship_id and ship.targeting_ship_id > -1:

            if ship.targeting_ship_id not in system.ships:
                ship.targeting_ship_id = -1
                continue

            time_since_last_shot = ticks - ship.last_shot_time
            if time_since_last_shot * ship.shot_frequency >= 1.0:
                shot = LaserShot(ship.id, ship.targeting_ship_id, 100, id_fun=new_id)
                shots[shot.id] = shot
                ship.last_shot_time = ticks
    return shots
