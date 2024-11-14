import os, psutil

def _get_process_dir() -> str:
    lc_procid: int = -1 # process id of the league client
    lc_install_dir: str = ""
    
    for proc in psutil.process_iter():
        if proc.name() == "LeagueClientUx.exe":
            lc_procid = proc.pid
            break

    if lc_procid != 1:
        # Future argument changes may break this
        proc_args: list[str] = psutil.Process(lc_procid).cmdline() # Get the argument list of the LeagueClientUx.exe process
        lc_install_dir = proc_args[14].split("=")[1]

    return lc_install_dir

def get_lockfile_information(lc_install_dir) -> list[str]:
    lockfile_path: str = os.path.join(lc_install_dir, "lockfile")
    lockfile: list[str] = []

    with open(lockfile_path, "r") as f:
        line = f.readline().split(":")
        lockfile = [line[2], line[3]] #2: port, 3: password
    
    return lockfile


print(get_lockfile_information(_get_process_dir()))
