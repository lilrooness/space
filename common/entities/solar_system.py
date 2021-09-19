from common.entities.entity import Entity


class SolarSystem(Entity):

    def __init__(self, ships=None, projectiles=None, active_laser_shots=None, in_flight_missiles=None, mini_gun_shots=None, sensor_towers=None, warp_points=None, crates=None, speed_boost_clouds=None, spawn_points=None, id=None, id_fun=None):
        super().__init__(id=id, id_fun=id_fun)
        if ships:
            self.ships = ships
        else:
            self.ships = {}

        if projectiles:
            self.projectiles = projectiles
        else:
            self.projectiles = {}

        if active_laser_shots:
            self.active_laser_shots = active_laser_shots
        else:
            self.active_laser_shots = {}

        if in_flight_missiles:
            self.in_flight_missiles = in_flight_missiles
        else:
            self.in_flight_missiles = {}

        if mini_gun_shots:
            self.mini_gun_shots = mini_gun_shots
        else:
            self.mini_gun_shots = {}

        if sensor_towers:
            self.sensor_towers = sensor_towers
        else:
            self.sensor_towers = {}

        if warp_points:
            self.warp_points = warp_points
        else:
            self.warp_points = {}

        if crates:
            self.crates = crates
        else:
            self.crates = {}

        if speed_boost_clouds:
            self.speed_boost_clouds = speed_boost_clouds
        else:
            self.speed_boost_clouds = {}

        if spawn_points:
            self.spawn_points = spawn_points
        else:
            self.spawn_points = {}

    def tick(self, delta=1.0, tick=None):
        for _id, ship in self.ships.items():
            ship.tick(delta=delta, currentTick=tick)

        for _id, missile in self.in_flight_missiles.items():
            missile.tick(self.ships, delta=delta)
