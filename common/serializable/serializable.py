from common.net_const import NONE_MARKER
from common.utils import string_to_bool

FIELD_TYPE_VALUE = 1
FIELD_TYPE_MULTIPLE_ENTITIES = 2
FIELD_TYPE_MULTIPLE_VALUES = 3

class Serializable():

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

        extracted_fields = {}

        position = 0
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
                    encoded_entities = parts[entities_idx: entities_idx + nEntities * len(entity_type.fields().keys())]
                    entities = entity_type.unmarshall_multiple_of_type(":".join(encoded_entities), entity_type)
                    extracted_fields[field_name] = entities
                    increment = 1 + nEntities * len(entity_type.fields().keys())
            elif type_info[0] == FIELD_TYPE_MULTIPLE_VALUES:
                value_type = type_info[1]
                if value_type not in [int, float]:
                    print("ERROR: FIELD_TYPE_MULTIPLE_VALUES doesnt support {}".format(value_type))
                    raise

                string_list = part.split(",")
                unmarshalled_list = [value_type(elem) for elem in string_list]
                if unmarshalled_list == [NONE_MARKER]:
                    extracted_fields[field_name] = []
                else:
                    extracted_fields[field_name] = unmarshalled_list


            position += increment

        return extracted_fields, parts[position:]

    @classmethod
    def fields(cls):
        """
        describes the structure of the marshalled message
        override this field
        :return:
        """
        return {}