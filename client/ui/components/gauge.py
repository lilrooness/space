import pygame

from client.mouse import get_mouse


def gauge(screen, background_color, foreground_color, container_rect, value, scroll_callback=None, verticle=True):
    if verticle:
        value_rect = pygame.Rect(
            container_rect.x,
            container_rect.height - (container_rect.height * value) + container_rect.y,
            container_rect.width,
            container_rect.height * value,
        )
    else:
        value_rect = pygame.Rect(
            container_rect.x,
            container_rect.y,
            container_rect.width * value,
            container_rect.height,
        )
    pygame.draw.rect(screen, background_color, container_rect)
    pygame.draw.rect(screen, foreground_color, value_rect)

    mouse = get_mouse()

    collision = container_rect.collidepoint(mouse.x, mouse.y)

    if scroll_callback and collision and mouse.wheel_scrolled:
        wheel_scroll_amount = mouse.wheel_scroll_amount
        mouse.use_button_event("wheel_scrolled")
        scroll_callback(wheel_scroll_amount)
