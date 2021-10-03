from .tools import get
from .config import MISSIONS
from .tools import checkpath


def mission_exists(mission_id: str) -> bool:
    if mission_id not in MISSIONS.keys():
        print(f"{mission_id} doesn't exist")
        return False
    return True


def show_missions():
    print("Mission Name | Mission id")
    print("-------------------------")
    for mission in MISSIONS.keys():
        print(f"{MISSIONS.get(mission)['name']} | {mission} ")
    return 0


def show_downlink_status(mission_id: str, timeline: str):
    if not mission_exists(mission_id=mission_id):
        return 1
    status_url = MISSIONS.get(mission_id)['status_url']
    resp = get(status_url).json()[timeline]
    if resp is not None:
        print(resp)
        return 0
    print("Mission Status unavailable!")
    return 0


def show_stats(mission_id: str):
    if not mission_exists(mission_id=mission_id):
        return 1
    stats_url = MISSIONS.get(mission_id)['stats_url']
    resp = get(stats_url).json()
    if resp is not None:
        print(resp)
        return 0
    print("Mission Stats unavailable!")
    return 0


def get_cameras(mission_id: str, what: str):
    if not mission_exists(mission_id=mission_id):
        return 1
    camera_info = MISSIONS.get(mission_id)["cameras"]
    if what == "ids":
        print(
            f"Camera ids for instruments in in {MISSIONS.get(mission_id)['name']}")
        print("----------------------------------")
        for i, camid in enumerate(camera_info.keys()):
            print(f"{i+1}. {camid}")
        return 0
    if what == "names":
        print(f"List of Cameras in {MISSIONS.get(mission_id)['name']}")
        print("----------------------------------")
        for i, camname in enumerate(camera_info.values()):
            print(f"{i+1}. {camname}")
        return 0


def download(mission_id: str,
             path: str,
             resolution: int = "full",
             ):
    if not mission_exists(mission_id=mission_id):
        return 1
    if not path or path==None:
        print(f"storage path not found, saving to current ./{mission_id}")
        path = f"./{mission_id}"

    
