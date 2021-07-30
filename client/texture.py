import os

import pygame.image

from client.const import loot_type_icons

_images = {}

def _load_image(filename):
    global _images
    path = os.path.join(*filename.split("/"))
    print(path)
    _images[filename] = pygame.image.load_extended(path)

def load_loot_icon_textures():
    for _id, filename in loot_type_icons.items():
        _load_image(filename)

def get_loot_icon_texture(type_id):
    return _images[loot_type_icons[type_id]]
