from datetime import datetime

from client.session import queue_to_send
from common.commands.request_power_change import RequestPowerChange


class PowerWindowState():

    def __init__(self, engines=0, shields=0, guns=0, tick_interval=50000, game_tick=0):
        self.engines = engines
        self.shields = shields
        self.guns = guns
        self.tick_interval = tick_interval
        self.last_sync = datetime.now()
        self.game_tick = game_tick

    def request_power_change(self, game, engines, shields, guns):
        newEngines = self.engines + engines

        totalNewPowerAllocation = game.power_allocation_engines + newEngines

        if totalNewPowerAllocation > 1.0 or totalNewPowerAllocation < 0:
            return

        self.engines = newEngines

    def tick(self, game):
        now = datetime.now()
        time_since_last_sync = now - self.last_sync

        if time_since_last_sync.microseconds >= self.tick_interval:
            self._push_request(game)
            self.last_sync = now

        if self.game_tick < game.tick_number:
            self.game_tick = game.tick_number
            self.engines = 0
            self.shields = 0
            self.guns = 0

    def _push_request(self, game):
        if self.engines or self.shields or self.guns:
            queue_to_send(
                RequestPowerChange(
                    max(0, self.engines + game.power_allocation_engines),
                    max(0, self.shields + game.power_allocation_shields),
                    max(0, self.guns + game.power_allocation_guns)
                )
            )
