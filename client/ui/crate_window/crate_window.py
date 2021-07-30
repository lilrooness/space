import pygame

from client.const import LOOT_ICON_WIDTH, LOOT_ICON_HEIGHT, scheme
from client.ui.components.banner import banner


def crate_window(game, screen, font, x, y, crate_id):
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