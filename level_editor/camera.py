from level_editor.mouse import get_mouse

SCREEN_W = 640*2
SCREEN_H = 480*2

_zoom = 1
_max_zoom = 16

_camera_center_x = 0
_camera_center_y = 0

_camera_x_transform = _camera_center_x - SCREEN_W/2
_camera_y_transform = _camera_center_y - SCREEN_H/2



def get_camera():
    return _camera_x_transform, _camera_y_transform,

def get_camera_zoom():
    return _zoom

def set_camera_zoom(zoom):
    global _zoom

    if zoom == 0:
        return

    _zoom = min(zoom, _max_zoom)

def move_camera(x, y):
    global _camera_x_transform
    global _camera_y_transform
    set_camera(x + _camera_x_transform, y + _camera_y_transform)

def set_camera(x_transform, y_transform):
    global _camera_x_transform
    global _camera_y_transform
    global _camera_center_x
    global _camera_center_y

    x_difference = x_transform - _camera_x_transform
    y_difference = y_transform - _camera_y_transform

    _camera_center_x += x_difference
    _camera_center_y += y_difference

    _camera_y_transform = y_transform
    _camera_x_transform = x_transform

def world_to_screen(x, y):
    # transform world space to camera space (0,0 in the center of the screen)
    global _camera_x_transform
    global _camera_y_transform

    camera_space_x = (x - _camera_center_x) / _zoom
    camera_space_y = (y - _camera_center_y) / _zoom

    # transform camera space back to screen space
    screen_space_x = (camera_space_x + _camera_center_x) - _camera_x_transform
    screen_space_y = (camera_space_y + _camera_center_y) - _camera_y_transform

    return (screen_space_x, screen_space_y)

def screen_to_world(screen_x, screen_y):
    global _camera_x_transform
    global _camera_y_transform

    # inverse equation of world_to_screen
    world_x = ((screen_x + _camera_x_transform - _camera_center_x) * _zoom) + _camera_center_x
    world_y = ((screen_y + _camera_y_transform - _camera_center_y) * _zoom) + _camera_center_y

    return (world_x, world_y)
