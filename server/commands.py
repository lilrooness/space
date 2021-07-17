from common.commands.request_moveto import RequestMoveToCommand
from common.utils import mag


def process_command(systems, session, command):
    if command.COMMAND_NAME == RequestMoveToCommand.COMMAND_NAME:
        ship = systems[session.solar_system_id].ships[session.ship_id]
        vector = (command.x - ship.x, command.y - ship.y)
        magnitude = mag(vector)
        unit_vector = (vector[0]/magnitude, vector[1]/magnitude)
        ship.vx = unit_vector[0] * 2
        ship.vy = unit_vector[1] * 2
