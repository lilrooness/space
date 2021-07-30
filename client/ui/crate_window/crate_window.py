import pygame

from client.camera import world_to_screen
from client.const import LOOT_ICON_WIDTH, LOOT_ICON_HEIGHT, scheme
from client.session import request_crate_content
from client.ui.components.banner import banner
from client.ui.components.button import button


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
    windowRect = pygame.Rect(
        x - width/2,
        y - height/2,
        width,
        height,
    )
    pygame.draw.rect(screen, scheme["ui_background"], windowRect)
    pygame.draw.rect(screen, scheme["ui_boarder"], windowRect, width=2)