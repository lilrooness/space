BASE_SENSOR_RANGE = 1400

BASE_LASER_DAMAGE = 10
BASE_LASER_RANGE = 400

BASE_MISSILE_DAMAGE = 30
BASE_MISSILE_RANGE = 1000
BASE_MISSILE_SPEED = 3.0

BASE_MINI_GUN_RANGE = 400
BASE_MINI_GUN_DAMAGE = 6
BASE_MINI_GUN_VELOCITY = 6.0

BASE_LASER_MISS_CHANCE = 0.1
BASE_MINI_GUN_MISS_CHANCE = 0.1
LASER_SHOT_FREQUENCY = 0.05
MISSILE_SHOT_FREQUENCY = 0.005
MINI_GUN_SHOT_FREQUENCY = 0.05

# above this threshold, the ship will take more damage when hit by weapons
ENGINE_POWER_DAMAGE_THRESHOLD = 0.3

# amount of extra damage per 0.1 above the damage threshold that the target ship will take
# base_damage = 20, engine_power = 0.5, increase_rate = 1.6
# extra_damage = base_damage * max(0, engine_power - ENGINE_POWER_DAMAGE_THRESHOLD) * increase_rate
# (20 * (0.2 * 1.6)) = 6.4
# final_damage = 6.4 + 20
ENGINE_DAMAGE_INCREASE_RATE = 1.6

BASE_SPEED = 1.0

TOWER_CONNECTION_RANGE=400
WARP_POINT_RANGE=400
CRATE_LOOT_RANGE = 100
SPEED_BOOST_CLOUD_RANGE=400

# loot
MISSILE_LAUNCHER = 1
LASER_TURRET = 2
MINI_GUN = 3

# map items
TOWER_TYPE_ID = -1
CRATE_TYPE_ID = -2
WARP_POINT_TYPE_ID = -3
SPAWN_POINT_TYPE_ID = -4
SPEED_BOOST_TYPE_ID = -5

def get_speed(engines_power_allocation):
    return BASE_SPEED * engines_power_allocation

def get_laser_range():
    return BASE_LASER_RANGE
