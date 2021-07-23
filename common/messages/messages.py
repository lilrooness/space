from common.messages.server_tick import ServerTickMessage
from common.messages.ship_damage import ShipDamageMessage

message_types = {
    ServerTickMessage.MESSAGE_NAME: ServerTickMessage,
    ShipDamageMessage.MESSAGE_NAME: ShipDamageMessage,
}