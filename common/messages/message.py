from common.serializable.serializable import Serializable


class Message(Serializable):

    @classmethod
    def message_unmarshal_fields_map(cls, encoded):
        parts = encoded.split(":")
        message_name = parts[0]

        extracted_fields, remaining = cls._unmarshal_fields_map(":".join(parts[1:]))
        extracted_fields["message_name"] = message_name

        return extracted_fields, remaining