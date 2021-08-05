from common.const import BASE_MISSILE_SPEED
from common.entities.entity import Entity
from common.serializable.serializable import FIELD_TYPE_VALUE
from common.utils import normalise


class InFlightMissile(Entity):

    def __init__(
            self,
            damage=0,
            owner_id=None,
            target_id=None,
            id=None,
            max_flight_ticks=100,
            speed=BASE_MISSILE_SPEED,
            x=0,
            y=0,
            vx=0,
            vy=0,
            explosion_range=15,
            id_fun=None
    ):
        super().__init__(id, id_fun)

        self.damage = damage
        self.owner_id = owner_id
        self.target_id = target_id
        self.max_flight_ticks = max_flight_ticks
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
        self.speed=speed
        self.ticks_alive=0
        self.explosion_range=explosion_range

    @classmethod
    def fields(cls):
        return {
            "id": (FIELD_TYPE_VALUE, int),
            "owner_id": (FIELD_TYPE_VALUE, int),
            "target_id": (FIELD_TYPE_VALUE, int),
            "x": (FIELD_TYPE_VALUE, float),
            "y": (FIELD_TYPE_VALUE, float),
            "speed": (FIELD_TYPE_VALUE, float),
        }

    def tick(self, ships, delta=1.0):
        self.ticks_alive += delta
        target_ship = ships[self.target_id]
        vx = target_ship.x - self.x
        vy = target_ship.y - self.y
        nvx, nvy = normalise(vx, vy)
        self.x += (nvx * self.speed) * delta
        self.y += (nvy * self.speed) * delta
