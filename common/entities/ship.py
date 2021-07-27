from common.entities.entity import Entity
from common.utils import string_to_bool, dist


class Ship(Entity):

    def __init__(self, x, y, type_id=1, id=None, id_fun=None, ammo=1, health=100, shield=100, dead=False):
        super().__init__(id, id_fun)
        self.ammo = ammo
        self.health = health
        self.shield = shield
        self.x = x
        self.y = y
        self.type_id = type_id
        self.warp = None
        self.vx = 2
        self.vy = 2
        self.targeting_ship_id = None
        self.last_shot_time = -1
        self.shot_frequency = 0.5
        self.dead = dead
        self.power_allocation_guns = 0.5
        self.power_allocation_shields = 0.25
        self.power_allocation_engines = 0.25

    def tick(self):
        if self.warp:
            if self.x != self.warp.endPos[0] or self.y != self.warp.endPos[1]:
                dp = (self.warp.vector[0] * self.warp.speed, self.warp.vector[1] * self.warp.speed)
                self.x += dp[0]
                self.y += dp[1]
        else:
            self.x += self.vx
            self.y += self.vy

    @classmethod
    def marshalled_field_types(cls):
        return {
            "id": lambda id: int(id),
            "x": lambda x: float(x),
            "y": lambda y: float(y),
            "health": lambda health: float(health),
            "shield": lambda shield: float(shield),
            "dead": lambda dead: string_to_bool(dead),
        }

class Warp():

    def __init__(self, startPos, endPos):
        self.startPos = startPos
        self.endPos = endPos

        d = dist(endPos[0], endPos[1], startPos[0], startPos[1])
        self.vector = ((endPos[0] - startPos[0]) / d, (endPos[1] - startPos[1]) / d)
        self.speed = d / 5


