from common.serializable.serializable import Serializable, FIELD_TYPE_VALUE, FIELD_TYPE_MULTIPLE_ENTITIES

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
        stringified_fields = []

        for field_name, type_info in self.fields().items():
            if type_info[0] == FIELD_TYPE_VALUE:
                stringified_fields.append(str(self.__dict__[field_name]))
            else:
                raise Exception("only FIELD_TYPE_VALUE allowed in Entity types")

        return ":".join(stringified_fields)

    @classmethod
    def unmarshall_multiple_of_type(cls, encoded_entities, type):
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
