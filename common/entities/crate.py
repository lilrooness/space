from common.entities.entity import Entity


class Crate(Entity):

    def __init__(
            self,
            x,
            y,
            contents={},
            id=None,
            id_fun=None,
    ):
        super(Crate).__init__(id, id_fun)
        self.x = x
        self.y = y
        self.contents = contents