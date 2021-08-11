from client.vfx.explosion_effect import ExplosionEffect


class WarpEffect(ExplosionEffect):

    def __init__(self, start_tick, *args, **kwargs):
        super(WarpEffect, self).__init__(*args, **kwargs)

        self.start_tick = start_tick

    def tick(self, current_tick, delta=0.0):

        if self.done:
            return

        ticksSinceStart = current_tick - self.start_tick

        if ticksSinceStart >= self.animation_ticks:
            self.done = True
            return

        tick_growth = self.radius / self.animation_ticks * delta

        progress = ticksSinceStart / self.animation_ticks

        self.drawRadius = progress * self.radius + tick_growth
