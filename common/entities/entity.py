from common.serializable.serializable import Serializable

system_ids = [
    1,2
]

ship_ids = [
    1,2
]

class Entity(Serializable):
    def __init__(self, id=None, id_fun=None):

        self.id = id
        if id_fun:
            self.id = id_fun()

    def marshal(self):
        stringified_fields = [
            str(self.__dict__[field])
            for field in self.fields().keys()
        ]
        return ":".join(stringified_fields)

    @classmethod
    def unmarshall_multiple_of_type(cls, encoded_entities, type):
        # fields = type.marshalled_fields()
        parts = encoded_entities.split(":")

        entities = []

        while len(parts):
            entity_fields, remaining = type._unmarshal_fields_map(":".join(parts))
            parts = remaining
            if entity_fields is {}:
                break
            else:
                entities.append(type(**entity_fields))

        return  entities
