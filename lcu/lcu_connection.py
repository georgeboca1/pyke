from lcu.process_info import get_lockfile_information, _get_process_dir
from lcu.lcu_exceptions import *
from base64 import b64encode
import requests,urllib3,json

class LeagueClientConnection(object):
    def __init__(self, port = None, password = None):
        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
        if port and password:
            self.port = port
            self.password = password
        else:
            self.port, self.password = get_lockfile_information(_get_process_dir())

        self.host = "127.0.0.1"
        self.basic = f"Basic {b64encode(f'riot:{self.password}'.encode()).decode()}"
        self.endpoints: dict = {
            "mm-search" : "/lol-lobby/v2/lobby/matchmaking/search",
            "lobby" : "/lol-lobby/v2/lobby",
            "is-searching": "/lol-lobby/v2/lobby/matchmaking/search-state",
            "is-champion-select": "/lol-champ-select/v1/session",
            "selected-champion": "/lol-champ-select/v1/current-champion"
        }
        self.headers = {
            "Authorization": self.basic,
            "Username" : "riot",
            "Password" : self.password
        }
        self.current_patch = ""

    def start_search(self) -> bool:
        req: requests.Response = requests.post(
            f"https://127.0.0.1:{self.port}/{self.endpoints['mm-search']}",
            headers=self.headers,
            verify=False
        )
        return True
    
    def is_in_lobby(self) -> bool:
        req: requests.Response = requests.get(
            f"https://127.0.0.1:{self.port}/{self.endpoints['lobby']}",
            headers=self.headers,
            verify=False
        )
        return req.status_code == 200
    
    def is_in_queue(self) -> bool:
        req: requests.Response = requests.get(
            f"https://127.0.0.1:{self.port}/{self.endpoints['is-searching']}",
            headers=self.headers,        
            verify=False
        )
        return "Searching" in req.text
    
    def is_in_champion_select(self) -> bool:
        req: requests.Response = requests.get(
            f"https://127.0.0.1:{self.port}/{self.endpoints['is-champion-select']}",
            headers=self.headers,        
            verify=False
        )
        return req.status_code != 404
    
    def get_selected_champion(self) -> str:
        req: requests.Response = requests.get(
            f"https://127.0.0.1:{self.port}/{self.endpoints['selected-champion']}",
            headers=self.headers,        
            verify=False
        )
        if req.status_code == 404:
            return -1
        return req.text
    
    def get_champion_name_by_id(self, id: int) -> str:
        with open("data/champions.json", "r") as f:
            data = json.load(f)
            
        return req.text
    
    def fetch_champion_list(self) -> bool:
        self.fetch_latest_patch()

        req: requests.Response = requests.get(
            f"https://ddragon.leagueoflegends.com/cdn/{self.current_patch}/data/en_US/champion.json"
        )
        if req.status_code == 404:
            return False
        
        with open("data/champions.json", "w+") as f:
            f.write(req.text)

        return True
    
    def fetch_latest_patch(self) -> bool:
        req: requests.Response = requests.get(
            "https://ddragon.leagueoflegends.com/api/versions.json"
        )
        self.current_patch = req.json()[1]
        return True