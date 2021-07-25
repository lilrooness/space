from common.commands.request_power_change import RequestPowerChange
from common.commands.request_moveto import RequestMoveToCommand
from common.commands.request_shoot import RequestShootCommand
from common.utils import mag

def process_command(systems, session, command):

    if command.COMMAND_NAME == RequestMoveToCommand.COMMAND_NAME:
        ship = systems[session.solar_system_id].ships[session.ship_id]
        vector = (command.x - ship.x, command.y - ship.y)
        magnitude = mag(vector)
        unit_vector = (vector[0]/magnitude, vector[1]/magnitude)
        ship.vx = unit_vector[0] * 2
        ship.vy = unit_vector[1] * 2
        return

    if command.COMMAND_NAME == RequestShootCommand.COMMAND_NAME:
        target_ship_id = command.target_ship_id
        if target_ship_id != session.ship_id:
            session_ship = systems[session.solar_system_id].ships[session.ship_id]
            session_ship.targeting_ship_id = target_ship_id
        return
    
    if command.COMMAND_NAME == RequestPowerChange.COMMAND_NAME:
        totalPower = command.engines + command.shields + command.guns
        if totalPower > 1.0:
            print("Not Enough Power")
            return
        else:
            ship = systems[session.solar_system_id].ships[session.ship_id]

            if command.engines >= 0:
                ship.power_allocation_engines = command.engines
            if command.shields >= 0:
                ship.power_allocation_shields = command.shields
            if command.guns > 0:
                ship.power_allocation_guns = command.guns
