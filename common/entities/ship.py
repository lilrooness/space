from common.entities.entity import Entity
from common.net_const import SERVER_TICK_TIME
from common.utils import string_to_bool, dist
from common.const import BASE_SPEED, get_speed


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
        self.targeting_ship_id = None
        self.last_shot_time = -1
        self.shot_frequency = 0.5
        self.dead = dead
        self.power_allocation_guns = power_allocation_guns
        self.power_allocation_shields = power_allocation_shields
        self.power_allocation_engines = power_allocation_engines

    def tick(self, delta=1.0):
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
    def marshalled_field_types(cls):
        return {
            "id": lambda id: int(id),
            "x": lambda x: float(x),
            "y": lambda y: float(y),
            "vx": lambda vx: float(vx),
            "vy": lambda vy: float(vy),
            "health": lambda health: float(health),
            "shield": lambda shield: float(shield),
            "dead": lambda dead: string_to_bool(dead),
            "power_allocation_guns": lambda power: float(power),
            "power_allocation_shields": lambda power: float(power),
            "power_allocation_engines": lambda power: float(power),
        }

class Warp():

    def __init__(self, startPos, endPos):
        self.startPos = startPos
        self.endPos = endPos

        d = dist(endPos[0], endPos[1], startPos[0], startPos[1])
        self.vector = ((endPos[0] - startPos[0]) / d, (endPos[1] - startPos[1]) / d)
        self.speed = d / 5
