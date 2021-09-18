from math import floor

import pygame

from client.camera import world_to_screen
from client.const import LOOT_ICON_WIDTH, LOOT_ICON_HEIGHT, SCREEN_H, SCREEN_W, scheme, CYAN, GRAY
from client.mouse import get_mouse
from client.ui.components.banner import banner, ANCHOR_TOPLEFT
from client.ui.components.icon import icon
from common.const import SLOT_AMMO_INFINITY, module_ticks_frequencies


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
        for target_id in slot.target_ids:
            target_screen_coords = world_to_screen(game, game.ships[target_id].x, game.ships[target_id].y)
            pygame.draw.line(screen, GRAY, (xpos, ypos), target_screen_coords)

        icon(
            screen,
            slot.type_id,
            pygame.Rect(xpos, ypos, LOOT_ICON_WIDTH, LOOT_ICON_HEIGHT),
        )

        proportion_loaded = 1.0
        if slot.last_slot_tick > -1:
            # TODO: use the server tick number here,
            #  game.tick_number is local, rename this

            ticks_since_last_tick = game.server_tick_number - slot.last_slot_tick
            proportion_loaded = min(1.0, ticks_since_last_tick * module_ticks_frequencies[slot.type_id])

        if proportion_loaded < 1.0:
            height = float(LOOT_ICON_HEIGHT) * (1.0 - proportion_loaded)
            loading_overlay_rect = pygame.Rect(xpos, ypos, LOOT_ICON_WIDTH, height)
            pygame.draw.rect(screen, GRAY, loading_overlay_rect)

        boarder_rect = pygame.Rect(
            xpos - 1,
            ypos - 1,
            LOOT_ICON_WIDTH + 2,
            LOOT_ICON_HEIGHT + 2
        )
        if slot.max_ammo != SLOT_AMMO_INFINITY:
            for x in range(slot.max_ammo):
                spacing = 2
                ammo_square_width = floor(LOOT_ICON_WIDTH/(slot.max_ammo-0.22)) - spacing
                ammo_rect = pygame.Rect(
                    xpos + x * (ammo_square_width + spacing),
                    ypos + LOOT_ICON_HEIGHT + 4,
                    ammo_square_width,
                    5,
                )
                if x < slot.ammo:
                    pygame.draw.rect(screen, CYAN, ammo_rect)
                else:
                    pygame.draw.rect(screen, GRAY, ammo_rect)

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
        if slot.ammo != SLOT_AMMO_INFINITY:
            banner(screen, xpos+1, ypos+1, str(slot.ammo), font, anchor=ANCHOR_TOPLEFT, padding=0)
        xpos += x_step
        slot_number+=1