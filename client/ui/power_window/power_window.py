import pygame

from client.const import SCREEN_W, scheme
from client.mouse import get_mouse
from client.ui.components.button import button
from client.ui.components.gauge import verticle_gauge
from client.ui.power_window.state import PowerWindowState


def power_window(game, screen, last_state):

    new_state = None
    if last_state is None:
        new_state = PowerWindowState(game_tick=game.tick_number)
    else:
        last_state.tick(game)
        new_state = last_state

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
    verticle_gauge(
        screen,
        scheme["ui_background_highlight"],
        scheme["engines_power"],
        engine_power_cont_rect,
        game.power_allocation_engines + new_state.engines,
        scroll_callback=lambda change : engine_power_change(0.05 * change, new_state, game)
    )
    button(screen, pygame.Rect(
        SCREEN_W - power_cont_W + 5,
        bar_height + 15,
        20,
        20,
        ),
        callback=lambda : engine_power_change(0.05, new_state, game),
    )
    button(screen, pygame.Rect(
        SCREEN_W - power_cont_W + 5,
        bar_height + 40,
        20,
        20,
        ),
        callback=lambda : engine_power_change(-0.05, new_state, game),
    )

    shields_power_cont_rect = pygame.Rect(
        SCREEN_W - power_cont_W + 30,
        5,
        20,
        bar_height
    )
    verticle_gauge(
        screen,
        scheme["ui_background_highlight"],
        scheme["shields_power"],
        shields_power_cont_rect,
        game.power_allocation_shields + new_state.shields,
        scroll_callback=lambda change: shield_power_change(0.05 * change, new_state, game)
    )
    button(screen, pygame.Rect(
        SCREEN_W - power_cont_W + 30,
        bar_height + 15,
        20,
        20,
        ),
        callback=lambda : shield_power_change(0.05, new_state, game),
    )
    button(screen, pygame.Rect(
        SCREEN_W - power_cont_W + 30,
        bar_height + 40,
        20,
        20,
        ),
        callback=lambda : shield_power_change(-0.05, new_state, game),
    )

    guns_power_cont_rect = pygame.Rect(
        SCREEN_W - power_cont_W + 55,
        5,
        20,
        bar_height
    )
    verticle_gauge(
        screen,
        scheme["ui_background_highlight"],
        scheme["guns_power"],
        guns_power_cont_rect,
        game.power_allocation_guns + new_state.guns,
        scroll_callback=lambda change: guns_power_change(0.05 * change, new_state, game)
    )
    button(screen, pygame.Rect(
        SCREEN_W - power_cont_W + 55,
        bar_height + 15,
        20,
        20,
        ),
        callback=lambda : guns_power_change(0.05, new_state, game),
    )
    button(screen, pygame.Rect(
        SCREEN_W - power_cont_W + 55,
        bar_height + 40,
        20,
        20,
        ),
        callback=lambda : guns_power_change(-0.05, new_state, game),
    )

    remaining_power_cont_rect = pygame.Rect(
        SCREEN_W - power_cont_W + 80,
        5,
        20,
        bar_height
    )
    verticle_gauge(screen, scheme["ui_background_highlight"], scheme["power"], remaining_power_cont_rect,
                   1.0 - (game.power_allocation_guns + game.power_allocation_shields + game.power_allocation_engines))

    # make the window intercept any scroll events that haven't been captures
    mouse = get_mouse()
    if power_container_rect.collidepoint(mouse.x, mouse.y):
        mouse.use_all_button_events()

    return new_state

def engine_power_change(delta, state, game):
    state.request_power_change(game, delta, 0, 0)

def shield_power_change(delta, state, game):
    state.request_power_change(game, 0, delta, 0)

def guns_power_change(delta, state, game):
    state.request_power_change(game, 0, 0, delta)

