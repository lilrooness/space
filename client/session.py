from select import select

from client.optimistic_command import optimistic_command
from common.commands.request_look_in_crate import RequestLookInCrateCommand
from common.net_const import HEADER_SIZE

_out_message_queue = []

def send_request(client_socket, request):
    bytes = request.marshal().encode()
    message_size = len(bytes)
    header = message_size.to_bytes(HEADER_SIZE, "big")
    print("sending message {}".format(header + bytes))
    client_socket.send(header + bytes)

def queue_to_send(request, optimistic_state=None):
    global _out_message_queue

    if optimistic_state:
        optimistic_command.commands[request.COMMAND_NAME](optimistic_state, request)

    _out_message_queue.append(request)

def process_out_message_queue(client_socket):
    global _out_message_queue

    def can_snd():
        _, writable, _ = select([], [client_socket], [], 0)
        return len(writable) > 0

    while _out_message_queue and can_snd():
        send_request(client_socket, _out_message_queue[0])
        _out_message_queue = _out_message_queue[1:]

    return _out_message_queue

def request_crate_content(game, crate_id):
    queue_to_send(RequestLookInCrateCommand(crate_id))
    if crate_id not in game.crate_requests:
        game.crate_requests.append(crate_id)

    if crate_id not in game.open_crates:
        game.open_crates.append(crate_id)
