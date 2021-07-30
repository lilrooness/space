import pygame

from client.const import scheme
from client.mouse import get_mouse


def button(screen, rect, callback=lambda : None, icon_surface=None):
    mouse = get_mouse()
    color = scheme["button_idle"]
    trigger_callback = False
    collision = rect.collidepoint(mouse.x, mouse.y)

    if collision and mouse.up_this_frame:
        trigger_callback = True
        mouse.use_button_event("up_this_frame")
        color = scheme["button_hover"]
    elif collision and mouse.mouse_down:
        color = scheme["button_down"]
        mouse.use_button_event("down_this_frame")
    elif collision:
        color = scheme["button_hover"]

    pygame.draw.rect(screen, color, rect)

    if trigger_callback:
        callback()
        mouse.use_all_button_events()
