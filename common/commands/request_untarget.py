from common.commands.command import Command


class RequestUnTargetCommand(Command):
    COMMAND_NAME = "request_un_target"

    def __init__(self, slot_id):
        self.slot_id = slot_id

    def marshal(self):
        return self.COMMAND_NAME + ":" + str(self.slot_id)

    @classmethod
    def unmarshal(cls, serialized_string):
        parts = serialized_string.split(":")

        if len(parts) != 2:
            print(cls.COMMAND_NAME + " COMMAND SIZE WRONG: <'{}'>".format(serialized_string))
            return

        name = parts[0]
        if name != cls.COMMAND_NAME:
            print(cls.COMMAND_NAME + " WRONG NAME <'{}'>".format(serialized_string))

        slot_id = int(parts[1])
        return RequestUnTargetCommand(slot_id)
