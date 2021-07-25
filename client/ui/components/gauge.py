import pygame


def verticle_gauge(screen, background_color, foreground_color, container_rect, value):
    value_rect = pygame.Rect(
        container_rect.x,
        container_rect.height - (container_rect.height * value) + container_rect.y,
        container_rect.width,
        (container_rect.height * value),
    )
    pygame.draw.rect(screen, background_color, container_rect)
    pygame.draw.rect(screen, foreground_color, value_rect)

