from common.commands.command import Command


class RequestLookInCrateCommand(Command):

    COMMAND_NAME = "request_look_in_crate"

    def __init__(self, crate_id):
        self.crate_id = crate_id

    def marshal(self):
        message = [
            self.COMMAND_NAME,
            str(self.crate_id)
        ]
        return ":".join(message)

    @classmethod
    def unmarshal(cls, serialized_string):
        parts = serialized_string.split(":")

        if len(parts) != 2:
            print(cls.COMMAND_NAME + " COMMAND SIZE WRONG: <'{}'>".format(serialized_string))
            return

        name = parts[0]
        if name != cls.COMMAND_NAME:
            print(cls.COMMAND_NAME + " WRONG NAME <'{}'>".format(serialized_string))

        crate_id = int(parts[1])

        return RequestLookInCrateCommand(crate_id)