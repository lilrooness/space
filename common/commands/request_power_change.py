from common.commands.command import Command


class RequestPowerChange(Command):
    COMMAND_NAME = "request_power_change"

    def __init__(self, engines, shields, guns):
        self.engines = engines
        self.shields = shields
        self.guns = guns
    

    def marshal(self):
        message = [
            self.COMMAND_NAME,
            str(self.engines),
            str(self.shields),
            str(self.guns),
            ]
        return ":".join(message)
    
    @classmethod
    def unmarshal(cls, serialized_string):
        parts = serialized_string.split(":")

        if len(parts) != 4:
            print(cls.COMMAND_NAME + " COMMAND SIZE WRONG: <'{}'>".format(serialized_string))
            return

        name = parts[0]
        if name != cls.COMMAND_NAME:
            print(cls.COMMAND_NAME + " WRONG NAME <'{}'>".format(serialized_string))

        engines = float(parts[1])
        shields = float(parts[2])
        guns    = float(parts[3])

        return RequestPowerChange(engines, shields, guns)