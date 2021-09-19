from common.entities.entity import Entity


class SpawnPoint(Entity):

    def __init__(self, x, y, id=None, id_fun=None):
        super().__init__(id=id, id_fun=id_fun)
        self.y = y
        self.x = x

