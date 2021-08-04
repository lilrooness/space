class Explosion():

    def __init__(self, x, y, radius, animation_ticks=500):
        self.x = x
        self.y = y
        self.radius = radius
        self.done = False
        self.drawRadius = 0
        self.animation_ticks = animation_ticks

    def tick(self):
        if self.done:
            return

        if self.drawRadius >= self.radius:
            self.done = True
            return

        growth_step = self.radius / self.animation_ticks
        self.drawRadius += growth_step