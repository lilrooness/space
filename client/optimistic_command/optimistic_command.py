from common.commands.request_moveto import RequestMoveToCommand
from common.commands.request_power_change import RequestPowerChange
from common.utils import normalise


def optmistic_request_move_to(game, command):
    ship = game.ships[game.ship_id]
    vector = (command.x - ship.x, command.y - ship.y)
    normalised_vector = normalise(*vector)
    ship.vx = normalised_vector[0]
    ship.vy = normalised_vector[1]


def optimistic_request_power_change(game, command):
    game.power_allocation_engines = command.engines

commands = {
    RequestMoveToCommand.COMMAND_NAME: optmistic_request_move_to,
    RequestPowerChange.COMMAND_NAME: optimistic_request_power_change,
}