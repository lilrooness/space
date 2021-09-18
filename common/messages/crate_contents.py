from common.entities.loot.lootitem import LootItem
from common.messages.message import Message
from common.net_const import NONE_MARKER
from common.serializable.serializable import FIELD_TYPE_VALUE, FIELD_TYPE_MULTIPLE_ENTITIES


class CrateContentsMessage(Message):

    MESSAGE_NAME = "crate_contents_message"

    def __init__(self, crate_id=0, contents=None):
        self.crate_id = crate_id
        if contents == None:
            self.contents = []
        self.contents = contents

    @classmethod
    def fields(cls):
        return {
            "crate_id": (FIELD_TYPE_VALUE, int),
            "contents": (FIELD_TYPE_MULTIPLE_ENTITIES, LootItem),
        }

    def marshal(self):
        marshalled_loots = [loot.marshal() for loot in self.contents]
        message = [
            CrateContentsMessage.MESSAGE_NAME,
            "%d" % self.crate_id,
            "%d" % len(self.contents),
            ":".join(marshalled_loots or [str(NONE_MARKER)]),
        ]

        return ":".join(message)

    @classmethod
    def unmarshal(cls, encoded):
        fields_map, _remaining = CrateContentsMessage.message_unmarshal_fields_map(encoded)

        return CrateContentsMessage(
            crate_id=fields_map["crate_id"],
            contents=fields_map["contents"]
        )
