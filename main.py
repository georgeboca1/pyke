from lcu.lcu_connection import LeagueClientConnection


if __name__ == "__main__":
    lcu = LeagueClientConnection()
    lcu.fetch_champion_list()
    print(lcu.current_patch)
