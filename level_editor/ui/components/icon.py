import pygame

from level_editor.texture import get_type_icon_texture


def icon(screen, type_id, rect):
    scaled_icon = pygame.transform.scale(get_type_icon_texture(type_id), (rect.width, rect.height))
    screen.blit(scaled_icon, rect)