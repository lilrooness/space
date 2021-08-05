from common.commands.request_look_in_crate import RequestLookInCrateCommand
from common.commands.request_moveto import RequestMoveToCommand
from common.commands.request_power_change import RequestPowerChange
from common.commands.request_target import RequestTargetCommand
from common.commands.request_untarget import RequestUnTargetCommand
from common.const import CRATE_LOOT_RANGE
from common.messages.crate_contents import CrateContentsMessage
from common.utils import dist, normalise
from server.game.slot_types.slot_types import slot_type_can_target, set_slot_target
from server.sessions.sessions import queue_message


def process_command(systems, session, command):

    if command.COMMAND_NAME == RequestMoveToCommand.COMMAND_NAME:
        ship = systems[session.solar_system_id].ships[session.ship_id]
        vector = (command.x - ship.x, command.y - ship.y)
        unit_vector = normalise(vector[0], vector[1])
        ship.vx = unit_vector[0]
        ship.vy = unit_vector[1]
        return

    if command.COMMAND_NAME == RequestTargetCommand.COMMAND_NAME:
        ship = systems[session.solar_system_id].ships[session.ship_id]
        target_ship_id = command.target_ship_id
        slot_id = command.slot_id
        all_ship_slots = ship.weapon_slots | ship.shield_slots | ship.shield_slots | ship.hull_slots
        if slot_id in all_ship_slots:

            slot = all_ship_slots[slot_id]
            if slot.type_id and slot_type_can_target(systems, session, slot.type_id, target_ship_id):
                set_slot_target(slot, target_ship_id)
        return

    if command.COMMAND_NAME == RequestUnTargetCommand.COMMAND_NAME:
        ship = systems[session.solar_system_id].ships[session.ship_id]
        target_ship_id = command.target_ship_id
        slot_id = command.slot_id
        all_ship_slots = ship.weapon_slots | ship.shield_slots | ship.shield_slots | ship.hull_slots
        if slot_id in all_ship_slots:
            slot = all_ship_slots[slot_id]
            if target_ship_id in slot.target_ids:
                slot.target_ids.remove(target_ship_id)
    
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