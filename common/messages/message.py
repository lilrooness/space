from common.space import Entity
from common.utils import string_to_bool

FIELD_TYPE_VALUE = 1
FIELD_TYPE_MULTIPLE_ENTITIES = 2

class Message():

    MESSAGE_NAME = None

    def marshal(self):
        pass

    @classmethod
    def unmarshal(cls, encoded):
        pass

    @classmethod
    def _unmarshal_fields_map(cls, encoded):
        """
        uses the message structure defined in cls.fields() to unmarhalled fields into a map
        of field_name -> value, which it returns
        :param encoded:
        :return extracted_fields:
        """
        parts = encoded.split(":")
        message_name = parts[0]

        extracted_fields = {
            "message_name": message_name,
        }

        position = 1
        for field_name, type_info in cls.fields().items():
            if position >= len(parts):
                break
            part = parts[position]
            increment = 1
            if type_info[0] == FIELD_TYPE_VALUE:
                if type_info[1] == bool:
                    extracted_fields[field_name] = string_to_bool(part)
                else:
                    extracted_fields[field_name] = type_info[1](part)
            elif type_info[0] == FIELD_TYPE_MULTIPLE_ENTITIES:
                entity_type = type_info[1]
                nEntities = int(part)
                if nEntities == 0:
                    extracted_fields[field_name] = []
                    increment = 2
                else:
                    entities_idx = position + 1
                    encoded_entities = parts[entities_idx: entities_idx + nEntities * len(entity_type.marshalled_fields())]
                    entities = Entity.unmarshall_multiple_of_type(":".join(encoded_entities), entity_type)
                    extracted_fields[field_name] = entities
                    increment = 1 + nEntities * len(entity_type.marshalled_fields())
            position += increment

        return extracted_fields

    @classmethod
    def fields(cls):
        """
        describes the structure of the marshalled message
        override this field
        :return:
        """
        return {}