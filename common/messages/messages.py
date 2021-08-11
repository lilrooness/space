from common.messages.crate_contents import CrateContentsMessage
from common.messages.explosion import ExplosionMessage
from common.messages.server_tick import ServerTickMessage
from common.messages.ship_damage import ShipDamageMessage
from common.messages.warp_started import WarpStartedMessage

message_types = {
    ServerTickMessage.MESSAGE_NAME: ServerTickMessage,
    ShipDamageMessage.MESSAGE_NAME: ShipDamageMessage,
    CrateContentsMessage.MESSAGE_NAME: CrateContentsMessage,
    ExplosionMessage.MESSAGE_NAME: ExplosionMessage,
    WarpStartedMessage.MESSAGE_NAME: WarpStartedMessage,
}
