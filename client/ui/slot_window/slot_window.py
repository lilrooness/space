import pygame

from client.const import scheme, LOOT_ICON_WIDTH, LOOT_ICON_HEIGHT
from client.texture import get_loot_icon_texture
from client.ui.components.icon import icon


def slot_window(screen, game, x=0, y=0):
    longest_row_length = max(
        max(len(game.hull_slots), len(game.weapon_slots)),
        max(len(game.shield_slots), len(game.engine_slots))
    )
    x_spacing = 50
    window_rect = pygame.Rect(
        x,
        y,
        50 + longest_row_length * x_spacing + 50,
        500,
    )
    pygame.draw.rect(screen, scheme["ui_background"], window_rect)
    pygame.draw.rect(screen, scheme["ui_boarder"], window_rect, width=2)

    slot_xpos = 0

    for slot in game.weapon_slots:
        rect = pygame.Rect(
            x + 50 + slot_xpos,
            y + 50,
            LOOT_ICON_WIDTH,
            LOOT_ICON_HEIGHT,
        )
        slot_xpos += x_spacing
        icon(screen, slot.type_id, rect)

    slot_xpos = 0
    for slot in game.shield_slots:
        rect = pygame.Rect(
            x + 50 + slot_xpos,
            y + 150,
            LOOT_ICON_WIDTH,
            LOOT_ICON_HEIGHT,
        )
        slot_xpos += x_spacing
        pygame.draw.rect(screen, scheme["ui_background_highlight"], rect)

    slot_xpos = 0
    for slot in game.engine_slots:
        rect = pygame.Rect(
            x + 50 + slot_xpos,
            y + 250,
            LOOT_ICON_WIDTH,
            LOOT_ICON_HEIGHT,
        )
        slot_xpos += x_spacing
        pygame.draw.rect(screen, scheme["ui_background_highlight"], rect)

    slot_xpos = 0
    for slot in game.hull_slots:
        rect = pygame.Rect(
            x + 50 + slot_xpos,
            y + 350,
            LOOT_ICON_WIDTH,
            LOOT_ICON_HEIGHT,
        )
        slot_xpos += x_spacing
        pygame.draw.rect(screen, scheme["ui_background_highlight"], rect)
