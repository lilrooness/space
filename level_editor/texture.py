import os

import pygame

from level_editor.types import types

_images = {}

def _load_image(filename):
    global _images
    path = os.path.join(*filename.split("/"))
    print(path)
    _images[filename] = pygame.image.load_extended(path)

def load_type_icon_textures():
    for _id, type in types.items():
        _load_image(type["icon_path"])

def get_type_icon_texture(type_id):
    return _images[types[type_id]["icon_path"]]
