from common.net_const import HEADER_SIZE
import socket
from select import select

_out_message_queue = []

def send_request(client_socket, request):
    bytes = request.marshal().encode()
    message_size = len(bytes)
    header = message_size.to_bytes(HEADER_SIZE, "big")
    print("sending message {}".format(header + bytes))
    client_socket.send(header + bytes)

def queue_to_send(request):
    global _out_message_queue

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
