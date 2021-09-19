class DraggedItem():

    def __init__(self, crate_id, type_id, dropped_callback):
        self.crate_id = crate_id
        self.dropped_callback = dropped_callback
        self.type_id = type_id

