from common.commands.request_look_in_crate import RequestLookInCrateCommand
from common.commands.request_power_change import RequestPowerChange
from common.commands.request_moveto import RequestMoveToCommand
from common.commands.request_slot_change import RequestSlotChange
from common.commands.request_target import RequestTargetCommand
from common.commands.request_untarget import RequestUnTargetCommand
from common.commands.request_warp import RequestWarpCommand

commands = {
    RequestWarpCommand.COMMAND_NAME: RequestWarpCommand,
    RequestTargetCommand.COMMAND_NAME: RequestTargetCommand,
    RequestMoveToCommand.COMMAND_NAME: RequestMoveToCommand,
    RequestPowerChange.COMMAND_NAME: RequestPowerChange,
    RequestLookInCrateCommand.COMMAND_NAME: RequestLookInCrateCommand,
    RequestSlotChange.COMMAND_NAME: RequestSlotChange,
    RequestUnTargetCommand.COMMAND_NAME: RequestUnTargetCommand,
}