import os
from datetime import datetime

import pygame

from level_editor.camera import set_camera_zoom, get_camera_zoom
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

    last_tick = datetime.now()
    tick_rate = 1000/60

    while run:

        mouse_button_up_this_frame = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if event.type == pygame.KEYDOWN:

                state.buffer_input(event)

                if event.key == pygame.K_ESCAPE:
                    state.selected = None

                if event.key == pygame.K_w:
                    state.buttons_pressed["up"] = 1
                if event.key == pygame.K_a:
                    state.buttons_pressed["left"] = 1
                if event.key == pygame.K_s:
                    if pygame.key.get_mods() & pygame.KMOD_CTRL and pygame.key.get_mods() & pygame.KMOD_SHIFT:
                        state.ask_save(os.getcwd().strip())
                    elif pygame.key.get_mods() & pygame.KMOD_CTRL:
                        if state.filename:
                            state.save(state.filename)
                        else:
                            state.ask_save(os.getcwd().strip())
                    else:
                        state.buttons_pressed["down"] = 1
                if event.key == pygame.K_d:
                    state.buttons_pressed["right"] = 1
                if event.key == pygame.K_o:
                    if pygame.key.get_mods() & pygame.KMOD_CTRL:
                        state.ask_load(os.getcwd().strip())

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_w:
                    state.buttons_pressed["up"] = 0
                if event.key == pygame.K_a:
                    state.buttons_pressed["left"] = 0
                if event.key == pygame.K_s:
                    state.buttons_pressed["down"] = 0
                if event.key == pygame.K_d:
                    state.buttons_pressed["right"] = 0

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

            if event.type == pygame.MOUSEWHEEL:
                set_camera_zoom(get_camera_zoom() + event.y)


        time_since_last_tick = datetime.now() - last_tick
        if time_since_last_tick.microseconds/1000 > tick_rate:
            state.tick()

        render(screen, screen_rect, state)
        get_mouse().use_all_button_events()
        pygame.display.flip()

