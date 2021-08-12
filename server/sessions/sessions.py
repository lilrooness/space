_sessions = {}

# session_id: [message, mess..]
_message_queue = {}

def get_sessions():
    return _sessions

def get_message_queue():
    return _message_queue

def queue_message(message, session_ids):
    for session_id in session_ids:
        if session_id in _message_queue:
            _message_queue[session_id].append(message)
        else:
            _message_queue[session_id] = [message]

def queue_message_for_broadcast(message):
    for id, session in _sessions.items():
        if id in _message_queue:
            _message_queue[id].append(message)
        else:
            _message_queue[id] = [message]

def get_session_ids_for_ship_ids(ship_ids):
    session_ids = []
    for session_id, session in _sessions.items():
        if session.ship_id in ship_ids:
            session_ids.append(session_id)

    return session_ids
