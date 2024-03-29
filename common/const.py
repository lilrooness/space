MAX_SHIELD_HEALTH = 100
MAX_HULL_HEALTH = 100

BASE_SENSOR_RANGE = 1400

# TODO: move this to types.yaml
BASE_LASER_DAMAGE = 10
BASE_LASER_RANGE = 400

# TODO: move this to types.yaml
BASE_MISSILE_DAMAGE = 30
BASE_MISSILE_RANGE = 1000
BASE_MISSILE_SPEED = 3.0

# TODO: move this to types.yaml
BASE_MINI_GUN_RANGE = 400
BASE_MINI_GUN_DAMAGE = 6
BASE_MINI_GUN_VELOCITY = 6.0

# TODO: move this to types.yaml
SHIELD_REPAIRER_HEAL_AMOUNT = 40
HULL_REPAIRER_HEAL_AMOUNT = 30

# TODO: move this to types.yaml
BASE_LASER_MISS_CHANCE = 0.1
BASE_MINI_GUN_MISS_CHANCE = 0.1
LASER_SHOT_FREQUENCY = 0.05
MISSILE_SHOT_FREQUENCY = 0.005
MINI_GUN_SHOT_FREQUENCY = 0.05
SHIELD_REPAIRER_FREQUENCY = 0.005
HULL_REPAIRER_FREQUENCY = 0.005

BASE_SPEED = 5.0

# TODO: move this to types.yaml
TOWER_CONNECTION_RANGE=400
WARP_POINT_RANGE=400
CRATE_LOOT_RANGE = 100
SPEED_BOOST_CLOUD_RANGE=400
SPEED_BOOST_CLOUD_SPEED_BOOST=1.5
SPEED_BOOST_CLOUD_SPEED_CAP=10.0

# loot
MISSILE_LAUNCHER = 1
LASER_TURRET = 2
MINI_GUN = 3
SHIELD_REPAIRER = 4
HULL_REPAIRER = 5

# map items
TOWER_TYPE_ID = -1
CRATE_TYPE_ID = -2
WARP_POINT_TYPE_ID = -3
SPAWN_POINT_TYPE_ID = -4
SPEED_BOOST_CLOUD_TYPE_ID = -5

SLOT_AMMO_INFINITY = -1

# TODO: move the module tick frequency to types.yaml to types.yaml
module_ticks_frequencies = {
    MISSILE_LAUNCHER: MISSILE_SHOT_FREQUENCY,
    LASER_TURRET: LASER_SHOT_FREQUENCY,
    MINI_GUN: MINI_GUN_SHOT_FREQUENCY,
    SHIELD_REPAIRER: SHIELD_REPAIRER_FREQUENCY,
    HULL_REPAIRER: HULL_REPAIRER_FREQUENCY,
}

def get_speed(engines_power_allocation):
    return BASE_SPEED * engines_power_allocation

def get_laser_range():
    return BASE_LASER_RANGE
