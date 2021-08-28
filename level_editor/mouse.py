class _MouseData:

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.up_this_frame = False
        self.down_this_frame = False
        self.mouse_down = False
        self.mouse_moved_this_frame = False
        self.wheel_scroll_amount = 0

    def set_mouse_down(self, button_states):
        if button_states[0]:
            self.mouse_down = True
            self.down_this_frame = True

    def set_mouse_up(self, button_states):
        if self.mouse_down:
            self.up_this_frame = True
            self.mouse_down = False

    def set_pos(self, x, y):
        self.mouse_moved_this_frame = self.x != x or self.y != y
        self.x = x
        self.y = y

    def use_button_event(self, key):
        if key == "wheel_scroll_amount":
            self.wheel_scroll_amount = 0
        self.__dict__[key] = False

    def use_all_button_events(self):
        self.down_this_frame = False
        self.up_this_frame = False
        self.mouse_moved_this_frame = False
        self.wheel_scrolled = False
        self.wheel_scroll_amount = 0

    def set_wheel_scrolled(self, amount):
        self.wheel_scrolled = True
        self.wheel_scroll_amount += amount

_mouse = _MouseData(0, 0)

def get_mouse():
    global _mouse
    return _mouse
