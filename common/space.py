from math import sqrt, pow

from common.utils import string_to_bool

system_ids = [
    1,2
]

ship_ids = [
    1,2
]

def dist(x1, y1, x2, y2):
    return sqrt(pow(x1 - x2, 2) + pow(y1 - y2, 2))

class Entity():
    def __init__(self, id=None, id_fun=None):
        if id:
            self.id = id
        if id_fun:
            self.id = id_fun()
    
    @classmethod
    def marshalled_fields(cls):
        return list(cls.marshalled_field_types().keys())

    @classmethod
    def marshalled_field_types(cls):
        return {}

    def marshal(self):
        stringified_fields = [
            str(self.__dict__[field]) 
            for field in self.marshalled_fields()
        ]
        return ":".join(stringified_fields)
    
    @classmethod
    def unmarshall_multiple_of_type(cls, encoded_entities, type):
        fields = type.marshalled_fields()
        parts = encoded_entities.split(":")

        entities = []

        while len(parts) >= len(fields):
            entity_fields = {}
            for i in range(len(fields)):
                field_name = fields[i]
                value = parts[i]
                if type.marshalled_field_types()[field_name] == bool:
                    entity_fields[field_name] = string_to_bool(value)
                else:
                    entity_fields[field_name] = type.marshalled_field_types()[field_name](value)

            entities.append(type(**entity_fields))
            parts = parts[len(fields):]

        return  entities



class Warp():

    def __init__(self, startPos, endPos):
        self.startPos = startPos
        self.endPos = endPos

        d = dist(endPos[0], endPos[1], startPos[0], startPos[1]) 
        self.vector = ((endPos[0] - startPos[0]) / d, (endPos[1] - startPos[1]) / d)
        self.speed = dist / 5


class ProjectileSlug(Entity):
    def __init__(self, id, id_fun, vx, vy, x, y, damage):
        super().__init__(id=id, id_fun=id_fun)
        self.vx = vx
        self.vy = vy
        self.x = x
        self.y = y
        self.damage = damage
        self.lastx = x
        self.lasty = y
    
    @classmethod
    def marshalled_field_types(cls):
        return {
            "id": lambda id: int(id),
            "vx": lambda vx: float(vx),
            "vy": lambda vy: float(vy),
            "x": lambda x: float(x),
            "y": lambda y: float(y),
            "damage": lambda damage: int(damage),
        }
    
    def tick(self):
        self.lastx = self.x
        self.lasty = self.y
        self.x += self.vx
        self.y += self.vy

class LaserShot(Entity):

    def __init__(self, shooter_ship_id, being_shot_ship_id, power, id=None, id_fun=None):
        super().__init__(id, id_fun)
        self.shooter_ship_id = shooter_ship_id
        self.being_shot_ship_id = being_shot_ship_id
        self.power = power

    @classmethod
    def marshalled_field_types(cls):
        return {
            "id": lambda id: int(id),
            "shooter_ship_id": lambda id: int(id),
            "being_shot_ship_id": lambda id: int(id),
            "power": lambda id: int(id),
        }

class Ship(Entity):

    def __init__(self, x, y, type_id=1, id=None, id_fun=None, ammo=1, health=100, shield=100, dead=False):
        super().__init__(id, id_fun)
        self.ammo = ammo
        self.health = health
        self.shield = shield
        self.x = x
        self.y = y
        self.type_id=type_id
        self.warp = None
        self.vx = 2
        self.vy = 2
        self.targeting_ship_id = None
        self.last_shot_time = -1
        self.shot_frequency = 0.5
        self.dead = dead

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
            "x" : lambda x: float(x),
            "y" : lambda y :float(y),
            "health": lambda health : int(health),
            "shield": lambda shield : int(shield),
            "dead": lambda dead : bool(dead),
        }


class SolarSystem(Entity):
    
    def __init__(self, ships={}, projectiles={}, active_laser_shots={}, id=None, id_fun=None):
        super().__init__(id=id, id_fun=id_fun)
        self.ships = ships
        self.projectiles = projectiles
        self.active_laser_shots = active_laser_shots

    def tick(self):
        for _id, ship in self.ships.items():
            ship.tick()
        
        for _id, projectile in self.projectiles.items():
            projectile.tick()
