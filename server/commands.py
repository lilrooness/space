from common.commands.request_look_in_crate import RequestLookInCrateCommand
from common.commands.request_moveto import RequestMoveToCommand
from common.commands.request_power_change import RequestPowerChange
from common.commands.request_slot_change import RequestSlotChange
from common.commands.request_target import RequestTargetCommand
from common.commands.request_untarget import RequestUnTargetCommand
from common.commands.request_warp import RequestWarpCommand
from common.const import CRATE_LOOT_RANGE, SLOT_AMMO_INFINITY
from common.entities.loot.lootitem import LootItem
from common.entities.ship import Warp
from common.messages.crate_contents import CrateContentsMessage
from common.messages.warp_exit_appeared import WarpExitAppearedMessage
from common.messages.warp_started import WarpStartedMessage
from common.utils import dist, normalise
from server.const import global_types
from server.game.server_game import get_ship_ids_in_sensor_range_of_ship, get_ship_ids_in_sensor_range_of_point, \
    ship_can_initiate_warp
from server.game.slot_types.slot_types import slot_type_can_target, set_slot_target
from server.id import new_id
from server.sessions.sessions import queue_message, get_session_ids_for_ship_ids


def process_command(systems, session, command, current_tick):

    if command.COMMAND_NAME == RequestWarpCommand.COMMAND_NAME:
        session_system = systems[session.solar_system_id]
        session_ship = session_system.ships[session.ship_id]

        if ship_can_initiate_warp(session_system, session.ship_id, command.x, command.y):
            session_ship.warp = Warp((command.x, command.y), current_tick)
            session_ids_in_range = get_session_ids_for_ship_ids(
                get_ship_ids_in_sensor_range_of_ship(
                    session_system,
                    session_ship.id
                )
            )
            queue_message(
                WarpStartedMessage(
                    session_ship.id,
                    session_ship.warp.warpTicks,
                    session_ship.warp.endPos[0],
                    session_ship.warp.endPos[1]
                ),
                [session.id] + session_ids_in_range,
            )

            session_ids_can_see_dest = get_session_ids_for_ship_ids(
                get_ship_ids_in_sensor_range_of_point(
                    session_system,
                    session_ship.warp.endPos[0],
                    session_ship.warp.endPos[1]
                )
            )

            queue_message(
                WarpExitAppearedMessage(
                    session_ship.warp.warpTicks,
                    session_ship.warp.endPos[0],
                    session_ship.warp.endPos[1]
                ),
                session_ids_can_see_dest,
            )


    elif command.COMMAND_NAME == RequestSlotChange.COMMAND_NAME:
        session_system = systems[session.solar_system_id]
        session_ship = session_system.ships[session.ship_id]

        type_in_crate = False
        crate_id = None
        for id, crate in session_system.crates.items():
            if dist(crate.x, crate.y, session_ship.x, session_ship.y) <= CRATE_LOOT_RANGE:
                if crate.get(command.type_id):
                    type_in_crate = True
                    crate_id = id
                    break

        slots = session_ship.weapon_slots | session_ship.hull_slots | session_ship.shield_slots | session_ship.engine_slots
        if type_in_crate and command.slot_id in slots:

            ammo_in_module = session_system.crates[crate_id].get(command.type_id).ammo

            slot = slots[command.slot_id]
            session_system.crates[crate_id].remove(command.type_id)

            if slot.type_id != 0:
                item = LootItem(id_fun=new_id, type_id=slot.type_id, ammo=slot.ammo)
                session_system.crates[crate_id].contents[item.id] = item

            slot.type_id = command.type_id
            slot.target_ids = []

            if "max_ammo" in global_types[command.type_id]:
                slot.max_ammo = global_types[command.type_id]["max_ammo"]
                slot.ammo = ammo_in_module
            else:
                slot.max_ammo = SLOT_AMMO_INFINITY
                slot.ammo = SLOT_AMMO_INFINITY

        if crate_id:
            new_contents = []
            for _id, loot in session_system.crates[crate_id].contents.items():
                new_contents.append(loot)

            queue_message(CrateContentsMessage(crate_id, new_contents), [session.id])

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
        slot_id = command.slot_id
        all_ship_slots = ship.weapon_slots | ship.shield_slots | ship.shield_slots | ship.hull_slots
        if slot_id in all_ship_slots:
            slot = all_ship_slots[slot_id]
            slot.target_ids = []

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
                contents = []
                for _id, loot in crate.contents.items():
                    contents.append(loot)

                queue_message(CrateContentsMessage(crate.id, contents), [session.id])
        else:
            print("CRATE {} DOES NOT EXIST IN SYSTEM {}".format(command.crate_id, session.solar_system_id))