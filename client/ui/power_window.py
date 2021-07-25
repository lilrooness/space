import pygame

from client.const import SCREEN_W, scheme
from client.session import queue_to_send
from client.ui.components.button import button
from client.ui.components.gauge import verticle_gauge
from common.commands.request_power_change import RequestPowerChange


def power_window(game, screen):
    power_cont_W = 160
    power_cont_H = 320
    power_container_rect = pygame.Rect(
        SCREEN_W - power_cont_W-2,
        2,
        power_cont_W,
        power_cont_H
    )

    pygame.draw.rect(screen, scheme["ui_background"], power_container_rect)
    pygame.draw.rect(screen, scheme["ui_boarder"], power_container_rect, width=1)
    bar_height = power_cont_H - 75
    engine_power_cont_rect = pygame.Rect(
        SCREEN_W - power_cont_W + 5,
        5,
        20,
        bar_height
    )
    verticle_gauge(screen, scheme["ui_background_highlight"], scheme["engines_power"], engine_power_cont_rect, game.power_allocation_engines)
    button(screen, pygame.Rect(
        SCREEN_W - power_cont_W + 5,
        bar_height + 15,
        20,
        20,
        ),
        callback=lambda : engine_power_change(game, 0.05),
    )
    button(screen, pygame.Rect(
        SCREEN_W - power_cont_W + 5,
        bar_height + 40,
        20,
        20,
        ),
        callback=lambda : engine_power_change(game, -0.05),
    )

    shields_power_cont_rect = pygame.Rect(
        SCREEN_W - power_cont_W + 30,
        5,
        20,
        bar_height
    )
    verticle_gauge(screen, scheme["ui_background_highlight"], scheme["shields_power"], shields_power_cont_rect, game.power_allocation_shields)
    button(screen, pygame.Rect(
        SCREEN_W - power_cont_W + 30,
        bar_height + 15,
        20,
        20,
        ),
        callback=lambda : shield_power_change(game, 0.05),
    )
    button(screen, pygame.Rect(
        SCREEN_W - power_cont_W + 30,
        bar_height + 40,
        20,
        20,
        ),
        callback=lambda : shield_power_change(game, -0.05),
    )

    guns_power_cont_rect = pygame.Rect(
        SCREEN_W - power_cont_W + 55,
        5,
        20,
        bar_height
    )
    verticle_gauge(screen, scheme["ui_background_highlight"], scheme["guns_power"], guns_power_cont_rect, game.power_allocation_guns)
    button(screen, pygame.Rect(
        SCREEN_W - power_cont_W + 55,
        bar_height + 15,
        20,
        20,
        ),
        callback=lambda : guns_power_change(game, 0.05),
    )
    button(screen, pygame.Rect(
        SCREEN_W - power_cont_W + 55,
        bar_height + 40,
        20,
        20,
        ),
        callback=lambda : guns_power_change(game, -0.05),
    )

    remaining_power_cont_rect = pygame.Rect(
        SCREEN_W - power_cont_W + 80,
        5,
        20,
        bar_height
    )
    verticle_gauge(screen, scheme["ui_background_highlight"], scheme["power"], remaining_power_cont_rect,
                   1.0 - (game.power_allocation_guns + game.power_allocation_shields + game.power_allocation_engines))

def engine_power_change(game, delta):
    request_power_change(game.power_allocation_engines + delta, game.power_allocation_shields, game.power_allocation_guns)

def shield_power_change(game, delta):
    request_power_change(game.power_allocation_engines, game.power_allocation_shields + delta, game.power_allocation_guns)

def guns_power_change(game, delta):
    request_power_change(game.power_allocation_engines, game.power_allocation_shields, game.power_allocation_guns + delta)

def request_power_change(engines, shields, guns):
    queue_to_send(RequestPowerChange(engines, shields, guns))

