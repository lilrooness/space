from common.commands.command import Command


class RequestMoveToCommand(Command):
    COMMAND_NAME = "request_moveto"

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def marshal(self):
        return self.COMMAND_NAME + ":" + str(self.x) + ":" + str(self.y)

    @classmethod
    def unmarshal(cls, serialized_string):
        parts = serialized_string.split(":")

        if len(parts) != 3:
            print(cls.COMMAND_NAME + " COMMAND SIZE WRONG: <'{}'>".format(serialized_string))
            return

        name = parts[0]
        if name != cls.COMMAND_NAME:
            print(cls.COMMAND_NAME + " WRONG NAME <'{}'>".format(serialized_string))

        x = float(parts[1])
        y = float(parts[2])

        return RequestMoveToCommand(x, y)