from math import sqrt, pow

from common.utils import string_to_bool

system_ids = [
    1,2
]

ship_ids = [
    1,2
]

class Entity():
    def __init__(self, id=None, id_fun=None):
        if id:
            self.id = id
        if id_fun:
            self.id = id_fun()
    
    @classmethod
    def marshalled_fields(cls):
        return list(cls.marshalled_field_types().keys())

    @classmethod
    def marshalled_field_types(cls):
        return {}

    def marshal(self):
        stringified_fields = [
            str(self.__dict__[field]) 
            for field in self.marshalled_fields()
        ]
        return ":".join(stringified_fields)
    
    @classmethod
    def unmarshall_multiple_of_type(cls, encoded_entities, type):
        fields = type.marshalled_fields()
        parts = encoded_entities.split(":")

        entities = []

        while len(parts) >= len(fields):
            entity_fields = {}
            for i in range(len(fields)):
                field_name = fields[i]
                value = parts[i]
                if type.marshalled_field_types()[field_name] == bool:
                    entity_fields[field_name] = string_to_bool(value)
                else:
                    entity_fields[field_name] = type.marshalled_field_types()[field_name](value)

            entities.append(type(**entity_fields))
            parts = parts[len(fields):]

        return  entities



