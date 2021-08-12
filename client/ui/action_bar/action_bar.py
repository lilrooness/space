import pygame

from client.const import LOOT_ICON_WIDTH, LOOT_ICON_HEIGHT, SCREEN_H, SCREEN_W, scheme
from client.mouse import get_mouse
from client.ui.components.banner import banner, ANCHOR_TOPLEFT
from client.ui.components.icon import icon


def action_bar(screen, game, font):
    active_slots = []

    slots = game.weapon_slots \
            + game.engine_slots \
            + game.shield_slots \
            + game.hull_slots

    for slot in slots:
        if slot.type_id:
            active_slots.append(slot)

    x_step = LOOT_ICON_WIDTH + 10
    xpos = SCREEN_W / 2 - ((len(active_slots) * x_step) / 2)
    ypos = SCREEN_H - 200

    slot_number = 1
    for slot in active_slots:
        icon(
            screen,
            slot.type_id,
            pygame.Rect(xpos, ypos, LOOT_ICON_WIDTH, LOOT_ICON_HEIGHT)
        )
        boarder_rect = pygame.Rect(
            xpos - 1,
            ypos - 1,
            LOOT_ICON_WIDTH + 2,
            LOOT_ICON_HEIGHT + 2
        )
        mouse = get_mouse()
        mouse_hover = boarder_rect.collidepoint(mouse.x, mouse.y)
        boarder_color = scheme["ui_boarder"]

        if mouse_hover and mouse.up_this_frame:
            if game.selected_slot_id == slot.id:
                game.selected_slot_id = None
            else:
                game.selected_slot_id = slot.id
        if game.selected_slot_id == slot.id:
            boarder_color = scheme["ui_boarder_selected"]
        elif mouse_hover:
            boarder_color = scheme["ui_boarder_highlight"]


        if mouse_hover:
            mouse.use_all_button_events()

        pygame.draw.rect(
            screen,
            boarder_color,
            boarder_rect,
            width=2,
        )
        banner(screen, xpos+1, ypos+1, str(slot_number), font, anchor=ANCHOR_TOPLEFT, padding=0)
        xpos += x_step
        slot_number+=1