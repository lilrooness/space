from common.space import Entity, Ship

FIELD_TYPE_VALUE = 1
FIELD_TYPE_MULTIPLE_SHIPS = 2
FIELD_TYPE_MULTIPLE_PROJECTILES = 3

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
                extracted_fields[field_name] = type_info[1](part)
            elif type_info[0] == FIELD_TYPE_MULTIPLE_SHIPS:
                nships = int(part)
                ships_idx = position+1
                encoded_ships = parts[ships_idx: ships_idx + nships*len(Ship.marshalled_fields())]
                ships = Entity.unmarshall_multiple_of_type(":".join(encoded_ships), Ship)
                extracted_fields[field_name] = ships
                increment = 1 + nships * len(Ship.marshalled_fields())

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