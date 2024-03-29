from common.const import get_speed
from common.entities.entity import Entity
from common.serializable.serializable import FIELD_TYPE_VALUE


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
            speed_boost = 1.0,
            speed_cap = 0,
            shield_slots = None,
            engine_slots = None,
            weapon_slots = None,
            hull_slots = None,
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
        self.speed_boost = speed_boost
        self.speed_cap = speed_cap

        if shield_slots:
            self.shield_slots = shield_slots
        else:
            self.shield_slots = []

        if engine_slots:
            self.engine_slots = engine_slots
        else:
            self.engine_slots = []

        if weapon_slots:
            self.weapon_slots = weapon_slots
        else:
            self.weapon_slots = []

        if hull_slots:
            self.hull_slots = hull_slots
        else:
            self.hull_slots = []

    def tick(self, delta=1.0, currentTick=None):
        if self.warp:
            if self.warp.done:
                self.x = self.warp.endPos[0]
                self.y = self.warp.endPos[1]
                self.warp = None
            else:
                self.warp.tick(currentTick)
        else:
            speed = self.speed_boost * get_speed(self.power_allocation_engines)
            if self.speed_cap:
                speed = min(self.speed_cap, speed)
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
            "speed_boost": (FIELD_TYPE_VALUE, float),
            "speed_cap": (FIELD_TYPE_VALUE, float),
        }

class Warp():

    def __init__(self, endPos, serverTickStarted, warpTicks=100):
        self.endPos = endPos
        self.warpTicks = warpTicks
        self.serverTickStarted = serverTickStarted
        self.done = False

    def tick(self, tick):
        ticksSinceStarted = tick - self.serverTickStarted
        self.done = ticksSinceStarted >= self.warpTicks
