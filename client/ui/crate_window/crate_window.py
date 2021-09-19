import pygame

from client.camera import world_to_screen
from client.const import LOOT_ICON_WIDTH, LOOT_ICON_HEIGHT, scheme
from client.dragged_item import DraggedItem
from client.session import request_crate_content, queue_to_send
from client.ui.components.banner import banner
from client.ui.components.button import button
from client.ui.components.icon import icon
from common.commands.request_slot_change import RequestSlotChange


def crate_window(game, screen, font, crate_id):
    crate = game.crates[crate_id]
    crate_screen_space_coords = world_to_screen(game, crate.x, crate.y)

    if crate_id in game.open_crates:
        _crate_window_contents(game, screen, font, crate_screen_space_coords[0], crate_screen_space_coords[1], crate_id)
    else:
        banner_rect, render_banner_fun = banner(
            screen,
            crate_screen_space_coords[0],
            crate_screen_space_coords[1],
            "Open",
            font,
            top=-10,
            defer_renering=True
        )
        button_rect = pygame.Rect(
            banner_rect.x - 3,
            banner_rect.y - 3,
            banner_rect.width + 6,
            banner_rect.height + 6,
        )

        def _reqest_crate():
            request_crate_content(game, crate_id)

        button(screen, button_rect, callback=_reqest_crate)
        render_banner_fun()

def _crate_window_contents(game, screen, font, x, y, crate_id):
    if crate_id in game.crate_requests:
        banner(screen, x, y, "loading ...", font)
        return

    crate = game.crates[crate_id]


    width = LOOT_ICON_WIDTH * len(crate.contents)
    height = LOOT_ICON_HEIGHT
    xpos = x - width/2
    ypos = y - height/2

    windowRect = pygame.Rect(
        xpos,
        ypos,
        width,
        height,
    )
    pygame.draw.rect(screen, scheme["ui_background"], windowRect)
    pygame.draw.rect(screen, scheme["ui_boarder"], windowRect, width=2)

    x_counter = 0
    for _id, item in crate.contents.items():
        icon_xpos = xpos+2 + x_counter
        icon_ypos = ypos+2
        icon_w = LOOT_ICON_WIDTH-4
        icon_h = LOOT_ICON_HEIGHT - 4

        button_rect = pygame.Rect(
            icon_xpos - 3,
            icon_ypos - 3,
            icon_w + 6,
            icon_h + 6,
        )

        def loot():
            _attempt_take_loot(game, crate.id, item.type_id)

        button(screen, button_rect, callback=loot)

        icon(
            screen,
            item.type_id,
            pygame.Rect(
                icon_xpos,
                icon_ypos,
                icon_w,
                icon_h,
            )
        )

        x_counter += LOOT_ICON_WIDTH

def _attempt_take_loot(game, crate_id, type_id):
    if not _take_loot(game, type_id):
        _start_dragging_loot(game, crate_id, type_id)

def _start_dragging_loot(game, crate_id, type_id):
    def _replace_loot(slot_id):
        queue_to_send(
            RequestSlotChange(slot_id, type_id)
        )

    game.dragged_item = DraggedItem(crate_id, type_id, _replace_loot)

def _take_loot(game, type_id):

    slot_id = None

    ship_slots = game.weapon_slots + game.shield_slots + game.engine_slots + game.hull_slots

    for slot in ship_slots:
        if slot.type_id == 0:
            slot_id = slot.id
            break

    if slot_id:
        queue_to_send(
            RequestSlotChange(slot_id, type_id)
        )
        return True
    else:
        return False
