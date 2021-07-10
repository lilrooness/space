

class Command():

    COMMAND_NAME = None

    def marshal(self):
        pass

    def unmarshal(self):
        pass

class RequestWarpCommand(Command):

    COMMAND_NAME = "request_warp"

    def __init__(self, x, y):
        super(RequestWarpCommand).__init__(self)
        self.x = x
        self.y = y

    def marshal(self):
        self.COMMAND_NAME + ":" + self.x + ":" + self.y

    @classmethod
    def unmarshal(cls, serialized_string):
        parts = serialized_string.split(":")
        
        if len(parts) != 3:
            print(cls.COMMAND_NAME + " COMMAND TOO LONG: <'{}'>".format(serialized_string))
            return
        
        name = parts[0]
        if name != cls.COMMAND_NAME:
            print(cls.COMMAND_NAME + " WRONG NAME <'{}'>".format(serialized_string))
        
        x = float(parts[1])
        y = float(parts[2])

        return RequestWarpCommand(x, y)

commands = {
    RequestWarpCommand.COMMAND_NAME: RequestWarpCommand,
}