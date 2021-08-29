import pygame

from level_editor.camera import move_camera, screen_to_world, set_camera
from level_editor.editor_io import write_map_file, read_map_file
from level_editor.mouse import get_mouse

BLACK = pygame.Color(0, 0, 0, 255)
WHITE = pygame.Color(255, 255, 255, 255)
LIGHT_GRAY = pygame.Color(150, 150, 150, 100)
GRAY = pygame.Color(100, 100, 100, 100)
DARK_GRAY = pygame.Color(50, 50, 50, 100)
GREEN = pygame.Color(0, 255, 0, 255)
YELLOW = pygame.Color(255, 255, 0, 255)
RED = pygame.Color(255, 0, 0, 255)
RED_TRANSPARENT = pygame.Color(255, 0, 0, 1)
CYAN = pygame.Color(0, 255, 255, 255)
PINK = pygame.Color(255, 20, 147, 255)

SCREEN_W = 640*2
SCREEN_H = 480*2

CONTINUE_INPUT = 1
RETURN_INPUT = 2
CANCEL_INPUT = 3

class EditorState():

    def __init__(self, placeables={}, filename=None):
        self.placeables = placeables
        self.selected = None
        self.x_pan = 0
        self.y_pan = 0
        self.pan_speed = 2
        self.buttons_pressed = {
            "up": 0,
            "down": 0,
            "left": 0,
            "right": 0,
        }
        self.filename = filename
        self.asking_for_load_path = False
        self.asking_for_save_path = False
        self.load_path = None
        self.save_path = None
        self.focus_editor_ui = True
        self.last_error = None
        self.show_ship_scale = True

        self.input_buffer = []

    def buffer_input(self, key):
        self.input_buffer.append(key)

    def select_placeable(self, type_id):
        self.selected = type_id

    def tick(self):
        if self.focus_editor_ui:
            # we don't care about the input buffer in editor mode
            self.process_editor_commands()
            self.input_buffer = []
            horizontal_camera_movement = (self.pan_speed * self.buttons_pressed["right"]) - (self.pan_speed * self.buttons_pressed["left"])
            vertical_camera_movement = (self.pan_speed * self.buttons_pressed["down"]) - (self.pan_speed * self.buttons_pressed["up"])
            move_camera(horizontal_camera_movement, vertical_camera_movement)
            mouse = get_mouse()
            if mouse.up_this_frame and self.selected:
                world_coords = screen_to_world(mouse.x, mouse.y)
                if self.selected in self.placeables:
                    self.placeables[self.selected].append(world_coords)
                else:
                    self.placeables[self.selected] = [world_coords]
        elif self.asking_for_load_path or self.asking_for_save_path:
            self.process_text_input()

    def process_editor_commands(self):
        for event in self.input_buffer:
            if event.key == pygame.K_t:
                if pygame.key.get_mods() & pygame.KMOD_CTRL:
                    self.toggle_show_ship_scale()

    def process_text_input(self):
        if self.asking_for_load_path:
            input_state, self.load_path = self.process_input_buffer_as_text_field_input(self.load_path)
            self.input_buffer = []
            if input_state == RETURN_INPUT:
                self.asking_for_load_path = False
                self.focus_editor_ui = True
                self.load(self.load_path)
            elif input_state == CANCEL_INPUT:
                self.asking_for_load_path = False
                self.focus_editor_ui = True

        if self.asking_for_save_path:
            input_state, self.save_path = self.process_input_buffer_as_text_field_input(self.save_path)
            self.input_buffer = []

            if input_state == RETURN_INPUT:
                self.asking_for_save_path = False
                self.focus_editor_ui = True
                self.save(self.save_path)
            elif input_state == CANCEL_INPUT:
                self.asking_for_save_path = False
                self.focus_editor_ui = True

    def process_input_buffer_as_text_field_input(self, existing_text):
        for event in self.input_buffer:
            if event.key == pygame.K_BACKSPACE:
                existing_text = existing_text[:-1]
            elif event.key == pygame.K_SPACE:
                existing_text = existing_text + " "
            elif event.key == pygame.K_ESCAPE:
                return (CANCEL_INPUT, existing_text)
            elif event.key == pygame.K_RETURN:
                return (RETURN_INPUT, existing_text)
            else:
                newLetter = event.unicode
                if pygame.key.get_mods() & pygame.KMOD_SHIFT:
                    newLetter.upper()
                existing_text = existing_text + newLetter

        return (CONTINUE_INPUT, existing_text)

    def toggle_show_ship_scale(self):
        self.show_ship_scale = not self.show_ship_scale

    def ask_load(self, path=None):
        self.focus_editor_ui = False
        self.asking_for_load_path = True
        self.load_path = path

    def ask_save(self, path=None):
        self.focus_editor_ui = False
        self.asking_for_save_path = True
        self.save_path = path

    def save(self, filename=None):
        try:
            if filename:
                write_map_file(self.placeables, filename)
                return True
            else:
                if self.filename:
                    write_map_file(self.placeables, self.filename)
                    return True
        except:
            self.last_error = "Error saving file: {}".format(filename or self.filename)
            print(self.last_error)

    def load(self, filename):
        try:
            self.filename = filename
            data = read_map_file(filename)
            self.placeables = data
            if self.placeables:
                initial_camera_coords = self.placeables[list(self.placeables.keys())[0]][0]
                set_camera(*initial_camera_coords)
        except:
            self.last_error = "Error loading file: {}".format(filename)
            print(self.last_error)
