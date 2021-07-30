from common.commands.request_look_in_crate import RequestLookInCrateCommand
from common.commands.request_power_change import RequestPowerChange
from common.commands.request_moveto import RequestMoveToCommand
from common.commands.request_shoot import RequestShootCommand
from common.commands.request_warp import RequestWarpCommand

commands = {
    RequestWarpCommand.COMMAND_NAME: RequestWarpCommand,
    RequestShootCommand.COMMAND_NAME: RequestShootCommand,
    RequestMoveToCommand.COMMAND_NAME: RequestMoveToCommand,
    RequestPowerChange.COMMAND_NAME: RequestPowerChange,
    RequestLookInCrateCommand.COMMAND_NAME: RequestLookInCrateCommand,
}