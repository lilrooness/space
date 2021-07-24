import pygame

from client.const import SCREEN_W, scheme
from client.mouse import get_mouse


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
    ))
    button(screen, pygame.Rect(
        SCREEN_W - power_cont_W + 5,
        bar_height + 40,
        20,
        20,
    ))

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
    ))
    button(screen, pygame.Rect(
        SCREEN_W - power_cont_W + 30,
        bar_height + 40,
        20,
        20,
    ))

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
    ))
    button(screen, pygame.Rect(
        SCREEN_W - power_cont_W + 55,
        bar_height + 40,
        20,
        20,
    ))

    remaining_power_cont_rect = pygame.Rect(
        SCREEN_W - power_cont_W + 80,
        5,
        20,
        bar_height
    )
    verticle_gauge(screen, scheme["ui_background_highlight"], scheme["power"], remaining_power_cont_rect,
                   1.0 - (game.power_allocation_guns + game.power_allocation_shields + game.power_allocation_engines))


def verticle_gauge(screen, background_color, foreground_color, container_rect, value):
    value_rect = pygame.Rect(
        container_rect.x,
        container_rect.height - (container_rect.height * value) + container_rect.y,
        container_rect.width,
        (container_rect.height * value),
    )
    pygame.draw.rect(screen, background_color, container_rect)
    pygame.draw.rect(screen, foreground_color, value_rect)

def button(screen, rect, callback=lambda : None):
    mouse = get_mouse()
    color = scheme["button_idle"]
    trigger_callback = False
    collision = rect.collidepoint(mouse.x, mouse.y)

    if collision and mouse.up_this_frame:
        trigger_callback = True
        mouse.use_button_event()
        color = scheme["button_hover"]
    elif collision and mouse.mouse_down:
        color = scheme["button_down"]
        mouse.use_button_event()
    elif collision:
        color = scheme["button_hover"]

    pygame.draw.rect(screen, color, rect)

    if trigger_callback:
        callback()
