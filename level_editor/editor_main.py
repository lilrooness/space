import pygame

from level_editor.editor import EditorState, SCREEN_W, SCREEN_H
from level_editor.mouse import get_mouse
from level_editor.render import render
from level_editor.texture import load_type_icon_textures
from level_editor.types import load_types

mouse_x, mouse_y = (0, 0)
mouse_button_up_this_frame = False
mouse_button_down = False

if __name__ == "__main__":
    pygame.init()
    pygame.font.init()
    pygame.image.get_extended()

    load_types()
    load_type_icon_textures()

    screen_rect = pygame.Rect(0, 0, SCREEN_W, SCREEN_H)
    screen = pygame.display.set_mode((SCREEN_W, SCREEN_H))

    state = EditorState()

    run = True

    while run:

        mouse_button_up_this_frame = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    state.selected = None

            if event.type == pygame.MOUSEMOTION:
                mouse_x, mouse_y = event.pos
                mouse = get_mouse()
                mouse.set_pos(mouse_x, mouse_y)

            if event.type == pygame.MOUSEBUTTONUP:
                mouse = get_mouse()
                mouse.set_mouse_up(pygame.mouse.get_pressed(num_buttons=3))

            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse = get_mouse()
                mouse.set_mouse_down(pygame.mouse.get_pressed(num_buttons=3))

        render(screen, screen_rect, state)
        get_mouse().use_all_button_events()
        pygame.display.flip()

