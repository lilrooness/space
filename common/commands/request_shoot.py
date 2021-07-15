from common.commands.command import Command


class RequestShoot(Command):

    COMMAND_NAME = "request_shoot"

    def __init__(self, target_ship_id):
        super(RequestShoot, self).__init__(self)
        self.target_ship_id = target_ship_id

    def marshal(self):
        return self.COMMAND_NAME + ":" + self.target_ship_id

    @classmethod
    def unmarshal(cls, serialized_string):
        parts = serialized_string.split(":")

        if len(parts) != 2:
            print(cls.COMMAND_NAME + " COMMAND SIZE WRONG: <'{}'>".format(serialized_string))
            return

        name = parts[0]
        if name != cls.COMMAND_NAME:
            print(cls.COMMAND_NAME + " WRONG NAME <'{}'>".format(serialized_string))

        target_ship_id = int(parts[1])
        return RequestShoot(target_ship_id)
