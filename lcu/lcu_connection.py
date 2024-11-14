from process_info import get_lockfile_information, _get_process_dir
from base64 import b64encode

class LeagueClientConnection(object):
    def __init__(self, port = None, password = None):
        if port and password:
            self.port = port
            self.password = password
        else:
            self.port, self.password = get_lockfile_information(_get_process_dir())

        self.host = "127.0.0.1"
        self.basic = b64encode(f"{self.password}:{self.password}")