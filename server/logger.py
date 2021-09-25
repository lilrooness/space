from datetime import datetime

class LogLine():
    def __init__(self, line, time):
        self.line = line
        self.time = time

class ServerSessionLogger():

    def __init__(self, global_session_name=None):
        if global_session_name:
            self.global_session_name = global_session_name
        else:
            self.global_session_name = datetime.now().strftime("%d_%m_%y_%H_%M_%S")

        self.session_logs = {}

    def to_client_log(self, session_id, serialisable):
        log_line_str = "OUT:" + serialisable.marshal()
        log_line = LogLine(log_line_str, datetime.now())
        if session_id not in self.session_logs:
            self.session_logs[session_id] = []

        self.session_logs[session_id].append(log_line)

    def to_server_log(self, session_id, serialisable):
        log_line_str = "IN:" + serialisable.marshal()
        log_line = LogLine(log_line_str, datetime.now())

        if session_id not in self.session_logs:
            self.session_logs[session_id] = []

        self.session_logs[session_id].append(log_line)

    def flush_session_logs(self, session_id, clear_session_log=True):
        if session_id in self.session_logs:
            with open(str(session_id) + "S_" + self.global_session_name + ".log", "w") as log_file:
                log_file.writelines(f'{s.time} {s.line}\n' for s in self.session_logs[session_id])

            if clear_session_log:
                del self.session_logs[session_id]
        else:
            print("WARN: trying to flush logs for unknown session_id: {}".format(session_id))

    def flush_all_session_logs(self):
        for session_id, _ in self.session_logs:
            self.flush_session_logs(session_id, clear_session_log=False)

        self.session_logs = {}

session_logger = ServerSessionLogger()

def get_session_logger():
    global session_logger
    return session_logger
