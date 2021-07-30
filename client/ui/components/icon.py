import pygame

from client.texture import get_loot_icon_texture

def icon(screen, type_id, rect):
    scaled_icon = pygame.transform.scale(get_loot_icon_texture(type_id), (rect.width, rect.height))
    screen.blit(scaled_icon, rect)