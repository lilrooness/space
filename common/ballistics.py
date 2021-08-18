from common.const import BASE_MINI_GUN_MISS_CHANCE, BASE_LASER_MISS_CHANCE, BASE_MINI_GUN_VELOCITY, BASE_MINI_GUN_DAMAGE


def get_mini_gun_miss_chance(transversal_velocity):
    return transversal_velocity * 5 * BASE_MINI_GUN_MISS_CHANCE

def get_laser_turret_miss_chance(transversal_velocity):
    return transversal_velocity * 5 * BASE_LASER_MISS_CHANCE

def get_mini_gun_shot_damage(velocity):
    velocityDamageModifier = velocity / BASE_MINI_GUN_VELOCITY * 2
    damage = velocityDamageModifier * BASE_MINI_GUN_DAMAGE
    return damage
