import pygame

from level_editor.editor import BLACK, WHITE, GREEN, SCREEN_W, SCREEN_H
from level_editor.mouse import get_mouse
from level_editor.types import types
from level_editor.ui.components.banner import banner
from level_editor.ui.components.icon import icon

def render_ui(screen, font, state):
    mouse = get_mouse()

    if state.selected:
        dim = 30
        icon(screen, state.selected, pygame.Rect(
            mouse.x - dim/2,
            mouse.y - dim/2,
            dim,
            dim,
        ))

        pygame.draw.line(screen, WHITE, (mouse.x, 0), (mouse.x, mouse.y))
        pygame.draw.line(screen, WHITE, (0, mouse.y), (mouse.x, mouse.y))
        pygame.draw.line(screen, WHITE, (SCREEN_W, mouse.y), (mouse.x, mouse.y))
        pygame.draw.line(screen, WHITE, (mouse.x, SCREEN_H), (mouse.x, mouse.y))

        banner(screen, SCREEN_W/2, 25, "{}, {}".format(mouse.x, mouse.y), font)


    left = 10
    top = 10
    dim = 50
    for type_id, type in types.items():
        if "placeable" in type:
            rect = pygame.Rect(
                left, top, dim, dim
            )

            if rect.collidepoint(mouse.x, mouse.y):
                color = WHITE

                if mouse.mouse_down:
                    color = GREEN
                elif mouse.up_this_frame:
                    state.select_placeable(type_id)
                    mouse.use_button_event("up_this_frame")

                pygame.draw.rect(screen, color, pygame.Rect(
                    left-1, top-1, dim+2, dim+2
                ))

            icon(screen, type_id, rect)
            top += dim*2


def render(screen, screen_rect, state):

    background_color = BLACK

    font = pygame.font.SysFont("sourcecodeproblack", 27)

    pygame.draw.rect(screen, background_color, screen_rect)
    render_ui(screen, font, state)
