_camera_x_transform = 0
_camera_y_transform = 0

def get_camera():
    return _camera_x_transform, _camera_y_transform,

def set_camera(x_transform, y_transform):
    global _camera_y_transform
    global _camera_x_transform
    _camera_x_transform = x_transform
    _camera_y_transform = y_transform

