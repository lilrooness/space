import pygame

from client.const import scheme, LOOT_ICON_WIDTH, LOOT_ICON_HEIGHT
from client.mouse import get_mouse
from client.ui.components.icon import icon


def slot_window(screen, game, x=0, y=0):
    longest_row_length = max(
        max(len(game.hull_slots), len(game.weapon_slots)),
        max(len(game.shield_slots), len(game.engine_slots))
    )
    x_spacing = LOOT_ICON_WIDTH + 10
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
        pygame.draw.rect(screen, scheme["ui_background_highlight"], rect)
        if slot.type_id:
            icon(screen, slot.type_id, rect)

        mouse = get_mouse()
        if game.dragged_item and rect.collidepoint(mouse.x, mouse.y) and mouse.up_this_frame:
            _drop_onto_slot(game, slot.id)

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
        if slot.type_id:
            icon(screen, slot.type_id, rect)

        mouse = get_mouse()
        if game.dragged_item and rect.collidepoint(mouse.x, mouse.y) and mouse.up_this_frame:
            _drop_onto_slot(game, slot.id)

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
        if slot.type_id:
            icon(screen, slot.type_id, rect)

        mouse = get_mouse()
        if game.dragged_item and rect.collidepoint(mouse.x, mouse.y) and mouse.down_this_frame:
            _drop_onto_slot(game, slot.id)

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
        if slot.type_id:
            icon(screen, slot.type_id, rect)

        mouse = get_mouse()
        if game.dragged_item and rect.collidepoint(mouse.x, mouse.y) and mouse.up_this_frame:
            _drop_onto_slot(game, slot.id)

def _drop_onto_slot(game, slot_id):
    game.dragged_item.dropped_callback(slot_id)
    game.dragged_item = None
    get_mouse().use_button_event("down_this_frame")
