import pygame

from client.camera import world_to_screen
from client.const import LOOT_ICON_WIDTH, LOOT_ICON_HEIGHT, scheme
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
        banner_rect = banner(screen, crate_screen_space_coords[0], crate_screen_space_coords[1], "Open", font,
                             top=-10)
        button_rect = pygame.Rect(
            banner_rect.x + banner_rect.width + 5,
            banner_rect.y,
            banner_rect.height,
            banner_rect.height,
        )

        def _reqest_crate():
            request_crate_content(game, crate_id)

        button(screen, button_rect, callback=_reqest_crate)

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
        icon(
            screen,
            item.type_id,
            pygame.Rect(
                xpos+2 + x_counter,
                ypos+2,
                LOOT_ICON_WIDTH-4,
                LOOT_ICON_HEIGHT-4,
            )
        )
        button_rect = pygame.Rect(
            xpos + 2 + x_counter,
            ypos + 2 + LOOT_ICON_HEIGHT-4,
            LOOT_ICON_WIDTH-4,
            10,
        )

        def loot():
            _take_loot(game, item.type_id)

        button(screen, button_rect, callback=loot)
        x_counter += LOOT_ICON_WIDTH

def _take_loot(game, type_id):

    slot_id = None

    for slot in game.weapon_slots:
        if slot.type_id == 0:
            slot_id = slot.id
            break

    if slot_id is None and game.weapon_slots:
        slot_id = game.weapon_slots[0].id

    if slot_id:
        queue_to_send(
            RequestSlotChange(slot_id, type_id)
        )
