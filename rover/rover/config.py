MISSIONS = {
    "mars2020": {
        "name":"Mars 2020/Perseverance",
        "id": "mars2020",
        "status_url":"https://mars.nasa.gov/mars_relay_items/?lander=M20",
        "stats_url":"https://mars.nasa.gov/rss/api/?feed=raw_images&category=mars2020&feedtype=json&latest=true",
        "cameras": {
            "NAVCAM_LEFT": "Navigation Camera - Left",
            "NAVCAM_RIGHT": "Navigation Camera - Right",
            "FRONT_HAZCAM_LEFT_A|FRONT_HAZCAM_LEFT_B": "Front Hazcam - Left",
            "FRONT_HAZCAM_RIGHT_A|FRONT_HAZCAM_RIGHT_B": "Front Hazcam - Right",
            "REAR_HAZCAM_LEFT": "Rear Hazcam - Left",
            "REAR_HAZCAM_RIGHT": "Rear Hazcam - Right",
            "MCZ_LEFT": "Mastcam-Z - Left",
            "MCZ_RIGHT": "Mastcam-Z - Right",
            "SKYCAM": "MEDA SkyCam",
            "SHERLOC_WATSON": "SHERLOC - WATSON",
            "SHERLOC_ACI": "SHERLOC - Context Imager",
            "SUPERCAM_RMI": "SuperCam Remote Micro Imager",
            "EDL_PUCAM1": "Parachute Up-Look Camera A",
            "EDL_PUCAM2": "Parachute Up-Look Camera B",
            "EDL_DDCAM": "Descent Stage Down-Look Camera",
            "EDL_RUCAM": "Rover Up-Look Camera",
            "EDL_RDCAM": "Rover Down-Look Camera",
            "LCAM": "Lander Vision System Camera",
            "HELI_NAV": "Navigation Camera",
            "HELI_RTE": "Color Camera"
        },
        "resolutions" : {
            "full": "full_res",
            "large": "large",
            "medium": "medium",
            "small": "small"
        },
        "formats" : {
            "full": "png",
            "large": "jpg",
            "medium": "jpg",
            "small": "jpg"
        }
    },
    "msl": {
        "id":"msl",
        "name":"Mars Science Laboratory/Curiosity",
        "status_url":"https://mars.nasa.gov/mars_relay_items/?lander=MSL",
        "stats_url":"https://mars.nasa.gov/rss/api/?feed=raw_images&category=msl&feedtype=json&latest=true",
        "cameras":{

        },
        "resolutions":{

        },
        "formats":{

        }
    }
}



METADATA_TEMPLATE = {
            "images": {
                "full": {"last_updated": "", "current_counts": "", },
                "large": {"last_updated": "", "current_counts": ""},
                "medium": {"last_updated": "", "current_counts": ""},
                "small": {"last_updated": "", "current_counts": ""}
            },
            "metadata": {
                "last_updated": "",
                "n_pages": "",
                "n_rows": ""
            }
        }

#M20CAMERA_CODES = MISSIONS.get('m20')["cameras"].keys()
#M20CAMERA_NAMES = MISSIONS.get('m20')["cameras"].values()
#MSLCAMERA_CODES = MISSIONS.get('msl')["cameras"].keys()
#MSLCAMERA_NAMES = MISSIONS.get('msl')["cameras"].values()

def get_stats_url(mission_id:str):
    return f"https://mars.nasa.gov/rss/api/?feed=raw_images&category={mission_id}&feedtype=json&latest=true"
