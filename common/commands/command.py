class Command():

    COMMAND_NAME = None

    def marshal(self):
        pass

    @classmethod
    def unmarshal(cls, _serialized_string):
        pass

