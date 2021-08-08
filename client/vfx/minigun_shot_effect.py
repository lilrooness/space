from datetime import datetime


class MinigunShotEffect():

    def __init__(self, origin_ship_id, target_ship_id, start_x, start_y, duration=100000, delay=0):
        self.origin_ship_id = origin_ship_id
        self.target_ship_id = target_ship_id
        self.current_animation_tick = 0
        self.done = False
        self.time_started = datetime.now()
        self.duration = duration
        self.x = start_x
        self.y = start_y
        self.delay = delay

    def tick(self, game):

        now = datetime.now()
        time_since_started = now - self.time_started

        if self.delay:
            if time_since_started.microseconds >= self.delay:
                self.delay = 0
                self.time_started = datetime.now()
            return

        if self.done:
            return

        if self.target_ship_id not in game.ships or self.origin_ship_id not in game.ships:
            self.done = True
            return

        origin_ship = game.ships[self.origin_ship_id]
        target_ship = game.ships[self.target_ship_id]

        proportion_done = min(1.0, time_since_started.microseconds / self.duration)

        if proportion_done == 0.0:
            self.x = origin_ship.x
            self.y = origin_ship.y
            return

        if proportion_done == 1.0:
            self.done = True
            self.x = target_ship.x
            self.y = target_ship.y
        else:
            total_x_dist = target_ship.x - origin_ship.x
            total_y_dist = target_ship.y - origin_ship.y

            self.x = origin_ship.x + (total_x_dist * proportion_done)
            self.y = origin_ship.y + (total_y_dist * proportion_done)