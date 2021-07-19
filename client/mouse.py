class _MouseData:

    def __init__(self, x, y):
        self.x = x
        self.y = x
        self.up_this_frame = False
        self.down_this_frame = False
        self.mouse_down = False
        self.mouse_moved_this_frame = False

    def tick(self, x, y, mouse_down):
        self.mouse_moved_this_frame = self.x != x or self.y != y:
        self.down_this_frame = (mouse_down and not self.mouse_down)
        self.up_this_frame = (not mouse_down and self.mouse_down)
        self.mouse_down = mouse_down
        self.x = x
        self.y = y        

_mouse_data = _MouseData(0, 0)

def get_mouse_data():
    return _mouse_data
