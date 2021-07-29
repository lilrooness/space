BASE_LASER_DAMAGE = 10
BASE_LASER_RANGE = 400

# above this threshold, the ship will take more damage when hit by weapons
ENGINE_POWER_DAMAGE_THRESHOLD = 0.3

# amount of extra damage per 0.1 above the damage threshold that the target ship will take
# base_damage = 20, engine_power = 0.5, increase_rate = 1.6
# extra_damage = base_damage * max(0, engine_power - ENGINE_POWER_DAMAGE_THRESHOLD) * increase_rate
# (20 * (0.2 * 1.6)) = 6.4
# final_damage = 6.4 + 20
ENGINE_DAMAGE_INCREASE_RATE = 1.6

BASE_SPEED = 10.0

def get_speed(engines_power_allocation):
    return BASE_SPEED * engines_power_allocation

def get_laser_range():
    return BASE_LASER_RANGE