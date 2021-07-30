from common.commands.request_look_in_crate import RequestLookInCrateCommand
from common.commands.request_power_change import RequestPowerChange
from common.commands.request_moveto import RequestMoveToCommand
from common.commands.request_shoot import RequestShootCommand
from common.const import get_laser_range, CRATE_LOOT_RANGE
from common.messages.crate_contents import CrateContentsMessage
from common.utils import mag, dist
from server.sessions.sessions import queue_message


def process_command(systems, session, command):

    if command.COMMAND_NAME == RequestMoveToCommand.COMMAND_NAME:
        ship = systems[session.solar_system_id].ships[session.ship_id]
        vector = (command.x - ship.x, command.y - ship.y)
        magnitude = mag(vector)
        unit_vector = (vector[0]/magnitude, vector[1]/magnitude)
        ship.vx = unit_vector[0]
        ship.vy = unit_vector[1]
        return

    if command.COMMAND_NAME == RequestShootCommand.COMMAND_NAME:
        target_ship_id = command.target_ship_id
        if target_ship_id != session.ship_id:
            session_ship = systems[session.solar_system_id].ships[session.ship_id]
            target_ship = systems[session.solar_system_id].ships[target_ship_id]
            range = dist(session_ship.x, session_ship.y, target_ship.x, target_ship.y)
            if range <= get_laser_range():
                session_ship = systems[session.solar_system_id].ships[session.ship_id]
                session_ship.targeting_ship_id = target_ship_id
        return
    
    if command.COMMAND_NAME == RequestPowerChange.COMMAND_NAME:
        totalPower = command.engines
        if totalPower > 1.0:
            return
        else:
            ship = systems[session.solar_system_id].ships[session.ship_id]

            if command.engines >= 0:
                ship.power_allocation_engines = command.engines

    if command.COMMAND_NAME == RequestLookInCrateCommand.COMMAND_NAME:
        session_system = systems[session.solar_system_id]
        session_ship  = session_system.ships[session.ship_id]
        if command.crate_id in session_system.crates:
            crate = session_system.crates[command.crate_id]
            if dist(session_ship.x, session_ship.y, crate.x, crate.y) <= CRATE_LOOT_RANGE:
                print("LOOTING CRATE {}".format(crate.id))
                contents = []
                for _id, loot in crate.contents.items():
                    contents.append(loot)

                queue_message(CrateContentsMessage(crate.id, contents), [session.id])
        else:
            print("CRATE {} DOES NOT EXIST IN SYSTEM {}".format(command.crate_id, session.solar_system_id))