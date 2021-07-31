import pygame

from client.const import LOOT_ICON_WIDTH, LOOT_ICON_HEIGHT, SCREEN_H, SCREEN_W, scheme
from client.ui.components.banner import banner, ANCHOR_TOPLEFT
from client.ui.components.icon import icon


def action_bar(screen, game, font):
    active_slots = []

    slots = game.ships[game.ship_id].weapon_slots \
            + game.ships[game.ship_id].engine_slots \
            + game.ships[game.ship_id].shield_slots \
            + game.ships[game.ship_id].hull_slots

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
        pygame.draw.rect(
            screen,
            scheme["ui_boarder"],
            pygame.Rect(
                xpos-1,
                ypos-1,
                LOOT_ICON_WIDTH+2,
                LOOT_ICON_HEIGHT+2
            ),
            width=2,
        )
        banner(screen, xpos+1, ypos+1, str(slot_number), font, anchor=ANCHOR_TOPLEFT, padding=0)
        xpos += x_step
        slot_number+=1