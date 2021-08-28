import pygame

from common.const import CRATE_LOOT_RANGE, TOWER_CONNECTION_RANGE, WARP_POINT_RANGE, SPEED_BOOST_CLOUD_RANGE
from level_editor.camera import world_to_screen, screen_to_world, get_camera_zoom
from level_editor.editor import BLACK, WHITE, GREEN, SCREEN_W, SCREEN_H, GRAY, RED, YELLOW
from level_editor.mouse import get_mouse
from level_editor.types import types, CRATE_TYPE_ID, TOWER_TYPE_ID, WARP_POINT_TYPE_ID, SPEED_BOOST_TYPE_ID
from level_editor.ui.components.banner import banner, ANCHOR_LEFT, ANCHOR_CENTER, ANCHOR_RIGHT
from level_editor.ui.components.icon import icon

def render_ui(screen, font, state):
    mouse = get_mouse()

    if state.selected and state.focus_editor_ui:
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

        world_coords = screen_to_world(mouse.x, mouse.y)
        banner(screen, SCREEN_W/2, 25, "{}, {}".format(world_coords[0], world_coords[1]), font)

    if state.last_error:
        banner(screen, 0, SCREEN_H-20, state.last_error, font, anchor=ANCHOR_LEFT, background_color=RED, foregound_color=WHITE)

    if state.asking_for_load_path:
        dialogue_w = 400
        dialogue_h = 200
        pygame.draw.rect(screen, GRAY, pygame.Rect(
            SCREEN_W/2-dialogue_w/2, SCREEN_H/2-dialogue_h/2, dialogue_w, dialogue_h
        ))
        banner(screen, SCREEN_W/2, (SCREEN_H/2) - 50, "Load File: (Please Type)", font, anchor=ANCHOR_CENTER, background_color=GRAY)
        banner(screen, SCREEN_W / 2 - dialogue_w/4, SCREEN_H/2+50, "Load: [ENTER]", font, anchor=ANCHOR_CENTER)
        banner(screen, SCREEN_W / 2 + dialogue_w/4, SCREEN_H/2+50, "Cancel: [ESC]", font, anchor=ANCHOR_CENTER)

        # text box
        banner(screen, SCREEN_W/2 + dialogue_w/2 - 5, SCREEN_H/2, state.load_path, font, anchor=ANCHOR_RIGHT)

    if state.asking_for_save_path:
        dialogue_w = 400
        dialogue_h = 200
        pygame.draw.rect(screen, GRAY, pygame.Rect(
            SCREEN_W/2-dialogue_w/2, SCREEN_H/2-dialogue_h/2, dialogue_w, dialogue_h
        ))
        banner(screen, SCREEN_W / 2, (SCREEN_H / 2) - 50, "Save File As: (Please Type)", font, anchor=ANCHOR_CENTER, background_color=GRAY)
        banner(screen, SCREEN_W / 2 - dialogue_w/4, SCREEN_H/2+50, "Save: [ENTER]", font, anchor=ANCHOR_CENTER)
        banner(screen, SCREEN_W / 2 + dialogue_w/4, SCREEN_H/2+50, "Cancel: [ESC]", font, anchor=ANCHOR_CENTER)

        # text box
        banner(screen, SCREEN_W/2 + dialogue_w/2 - 5, SCREEN_H / 2, state.save_path, font, anchor=ANCHOR_RIGHT)


    left = 10
    top = 10
    dim = 50
    for type_id, type in types.items():
        if "placeable" in type:
            rect = pygame.Rect(
                left, top, dim, dim
            )

            hover = False

            if rect.collidepoint(mouse.x, mouse.y):
                hover = True
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
            if hover:
                banner(screen, get_mouse().x, get_mouse().y, types[type_id]["name"], font, anchor=ANCHOR_LEFT)
            top += dim*2


def render(screen, screen_rect, state):

    background_color = BLACK

    font = pygame.font.SysFont("sourcecodeproblack", 27)

    pygame.draw.rect(screen, background_color, screen_rect)

    for type_id, coord_list in state.placeables.items():
        for coords in coord_list:
            s_coords = world_to_screen(*coords)
            if type_id == CRATE_TYPE_ID:
                pygame.draw.circle(screen, WHITE, s_coords, CRATE_LOOT_RANGE/get_camera_zoom(), width=2)
            elif type_id == TOWER_TYPE_ID:
                pygame.draw.circle(screen, WHITE, s_coords, TOWER_CONNECTION_RANGE / get_camera_zoom(), width=2)
            elif type_id == WARP_POINT_TYPE_ID:
                pygame.draw.circle(screen, WHITE, s_coords, WARP_POINT_RANGE / get_camera_zoom(), width=2)
            elif type_id == SPEED_BOOST_TYPE_ID:
                pygame.draw.circle(screen, YELLOW, s_coords, SPEED_BOOST_CLOUD_RANGE / get_camera_zoom(), width=2)

            dim = 30
            icon(screen, type_id, pygame.Rect(
                s_coords[0]-dim/2, s_coords[1]-dim/2, dim, dim
            ))

    render_ui(screen, font, state)
