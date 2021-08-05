from common.commands.command import Command

class RequestSlotChange(Command):

    COMMAND_NAME = "request_slot_changes"

    def __init__(self, slot_id, type_id):
        self.slot_id = slot_id
        self.type_id = type_id

    def marshal(self):
        message = [
            self.COMMAND_NAME,
            str(self.slot_id),
            str(self.type_id),
        ]
        return ":".join(message)

    @classmethod
    def unmarshal(cls, serialized_string):
        parts = serialized_string.split(":")

        if len(parts) != 3:
            print(cls.COMMAND_NAME + " COMMAND SIZE WRONG: <'{}'>".format(serialized_string))
            return

        name = parts[0]
        if name != cls.COMMAND_NAME:
            print(cls.COMMAND_NAME + " WRONG NAME <'{}'>".format(serialized_string))

        slot_id = int(parts[1])
        type_id = int(parts[2])

        return RequestSlotChange(slot_id, type_id)