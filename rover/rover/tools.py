import os
import requests
from .config import MISSIONS
from datetime import datetime as dt 

def mission_exists(mission_id: str) -> bool:
    if mission_id not in MISSIONS.keys():
        print(f"{mission_id} doesn't exist")
        return False
    return True

def n_pages(stats_url:str):
    """
    Finds total number of available pages
    """
    try:
        r = get(stats_url)
        stats = r.json()
        n = round(stats["total"]/50)
        return n
    except Exception as e:
        print(f"Error: {e}")


def checkpath(path: str) -> bool:
    """
    Checks if a give path exists
    Creates dirs if doesn't exist
    """
    if not os.path.exists(path):
        return False
    return True


def get(url: str, **kwargs):
    """
    Wrapper for requests.get
    """
    r = requests.get(url, **kwargs)
    if r.status_code == 200:
        return r
    else:
        raise Exception(
            f"Network Exception, failed to fetch requested page {url}")

def give_me_time():
    """
    Creates a timestamp with current system time
    used in metadata updation and filenames
    """
    return dt.strftime(dt.now(), '%Y-%m-%d-%H_%M_%S')