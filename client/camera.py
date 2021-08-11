from common.utils import mag, normalise

_camera_x_transform = None
_camera_y_transform = None

_zoom = 1
_max_zoom = 8

_target_x = 0
_target_y = 0

_vx = 0
_vy = 0

_camera_mass = 50

def get_camera():
    return _camera_x_transform, _camera_y_transform,

def get_camera_zoom():
    return _zoom

def set_camera_zoom(zoom):
    global _zoom

    if zoom == 0:
        return

    _zoom = min(zoom, _max_zoom)

def set_camera(x_transform, y_transform):
    global _camera_x_transform
    global _camera_y_transform

    if _camera_y_transform is None or _camera_x_transform is None:
        _camera_x_transform = x_transform
        _camera_y_transform = y_transform
        return

    global _target_y
    global _target_x
    _target_x = x_transform
    _target_y = y_transform
    _tick_camera()

def _tick_camera():
    global _camera_x_transform
    global _camera_y_transform
    global _vx
    global _vy

    dx = _target_x - _camera_x_transform
    dy = _target_y - _camera_y_transform

    unit_vector = normalise(dx, dy)
    distance = mag((dx, dy))

    _apply_force(unit_vector[0] * (distance/5), unit_vector[1] * (distance/5))
    _camera_x_transform += _vx
    _camera_y_transform += _vy
    _vx = 0
    _vy = 0


def _apply_force(x, y):
    global _vx
    global _vy

    _vx += x / _camera_mass
    _vy += y / _camera_mass

def world_to_screen(game, x, y):
    # transform world space to camera space (0,0 in the center of the screen)
    ship = game.ships[game.ship_id]

    camera_space_x = (x - ship.x) / _zoom
    camera_space_y = (y - ship.y) / _zoom

    # transform camera space back to screen space
    screen_space_x = (camera_space_x + ship.x) - _camera_x_transform
    screen_space_y = (camera_space_y + ship.y) - _camera_y_transform

    return (screen_space_x, screen_space_y)

def screen_to_world(game, screen_x, screen_y):
    ship = game.ships[game.ship_id]

    # inverse equation of world_to_screen
    world_x = ((screen_x + _camera_x_transform - ship.x) * _zoom) + ship.x
    world_y = ((screen_y + _camera_y_transform - ship.y) * _zoom) + ship.y

    return (world_x, world_y)