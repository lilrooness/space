from math import sqrt, pow


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
        return []

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
                entity_fields[field_name] = value
            
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

class Ship(Entity):

    def __init__(self, x, y, type_id=1, id=None, id_fun=None, ammo=1, health=100):
        super().__init__(id, id_fun)
        self.ammo = 1
        self.health = 100
        self.x = x
        self.y = y
        self.type_id=type_id
        self.warp = None
    
    def tick(self):
        if self.warp:
            if self.x != self.warp.endPos[0] or self.y != self.warp.endPos[1]:
                dp = (self.warp.vector[0] * self.warp.speed, self.warp.vector[1] * self.warp.speed)
                self.x += dp[0]
                self.y += dp[1]
    
    @classmethod
    def marshalled_fields(cls):
        return [
            "id",
            "x",
            "y",
            "health",
            "ammo"
        ]


class SolarSystem(Entity):
    
    def __init__(self, ships={}, id=None, id_fun=None):
        super().__init__(id=id, id_fun=id_fun)
        self.ships = ships

    def tick(self):
        for _id, ship in self.ships.items():
            ship.tick()

