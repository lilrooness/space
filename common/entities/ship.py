from common.const import get_speed
from common.entities.entity import Entity
from common.serializable.serializable import FIELD_TYPE_VALUE
from common.utils import dist


class Ship(Entity):

    def __init__(
            self,
            x,
            y,
            vx=0,
            vy=0,
            type_id=1,
            id=None,
            id_fun=None,
            ammo=1,
            health=100,
            shield=100,
            dead=False,
            power_allocation_guns=0.5,
            power_allocation_shields = 0.25,
            power_allocation_engines = 0.25,
            shield_slots = [],
            engine_slots = [],
            weapon_slots = [],
            hull_slots = [],
    ):
        super().__init__(id, id_fun)
        self.ammo = ammo
        self.health = health
        self.shield = shield
        self.x = x
        self.y = y
        self.type_id = type_id
        self.warp = None
        self.vx = vx
        self.vy = vy
        self.last_shot_time = -1
        self.shot_frequency = 0.5
        self.dead = dead
        self.power_allocation_guns = power_allocation_guns
        self.power_allocation_shields = power_allocation_shields
        self.power_allocation_engines = power_allocation_engines

        self.shield_slots = shield_slots
        self.engine_slots = engine_slots
        self.weapon_slots = weapon_slots
        self.hull_slots   = hull_slots

    def tick(self, delta=1.0, corrected_location=None):
        if self.warp:
            if self.x != self.warp.endPos[0] or self.y != self.warp.endPos[1]:
                dp = (self.warp.vector[0] * self.warp.speed, self.warp.vector[1] * self.warp.speed)
                self.x += dp[0]
                self.y += dp[1]
        else:
            speed = get_speed(self.power_allocation_engines)
            self.x += (self.vx * speed) * delta
            self.y += (self.vy * speed) * delta

    @classmethod
    def fields(cls):
        return {
            "id": (FIELD_TYPE_VALUE, int),
            "x": (FIELD_TYPE_VALUE, float),
            "y": (FIELD_TYPE_VALUE, float),
            "vx": (FIELD_TYPE_VALUE, float),
            "vy": (FIELD_TYPE_VALUE, float),
            "health": (FIELD_TYPE_VALUE, float),
            "shield": (FIELD_TYPE_VALUE, float),
            "dead": (FIELD_TYPE_VALUE, bool),
            "power_allocation_guns": (FIELD_TYPE_VALUE, float),
            "power_allocation_shields": (FIELD_TYPE_VALUE, float),
            "power_allocation_engines": (FIELD_TYPE_VALUE, float),
        }

class Warp():

    def __init__(self, startPos, endPos):
        self.startPos = startPos
        self.endPos = endPos

        d = dist(endPos[0], endPos[1], startPos[0], startPos[1])
        self.vector = ((endPos[0] - startPos[0]) / d, (endPos[1] - startPos[1]) / d)
        self.speed = d / 5
