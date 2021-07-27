_camera_x_transform = 0
_camera_y_transform = 0
_zoom = 1
_max_zoom = 8

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
    global _camera_y_transform
    global _camera_x_transform
    _camera_x_transform = x_transform
    _camera_y_transform = y_transform

def world_to_screen(game, x, y):
    # transform world space to camera space (0,0 in the center of the screen)
    ship = game.ships[game.ship_id]

    camera_space_x = (x - ship.x) / _zoom
    camera_space_y = (y - ship.y) / _zoom

    # transform camera space back to screen space
    screen_space_x = (camera_space_x + ship.x) - _camera_x_transform
    screen_space_y = (camera_space_y + ship.y) - _camera_y_transform

    return (screen_space_x, screen_space_y)
