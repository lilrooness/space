from common.commands.command import Command


class RequestTargetCommand(Command):

    COMMAND_NAME = "request_target"

    def __init__(self, target_ship_id, slot_id):
        self.target_ship_id = target_ship_id
        self.slot_id = slot_id

    def marshal(self):
        return self.COMMAND_NAME + ":" + str(self.target_ship_id) + ":" + str(self.slot_id)

    @classmethod
    def unmarshal(cls, serialized_string):
        parts = serialized_string.split(":")

        if len(parts) != 3:
            print(cls.COMMAND_NAME + " COMMAND SIZE WRONG: <'{}'>".format(serialized_string))
            return

        name = parts[0]
        if name != cls.COMMAND_NAME:
            print(cls.COMMAND_NAME + " WRONG NAME <'{}'>".format(serialized_string))

        target_ship_id = int(parts[1])
        slot_id = int(parts[2])
        return RequestTargetCommand(target_ship_id, slot_id)
