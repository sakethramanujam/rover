import os
import shutil
from .tools import checkpath, get, n_pages, mission_exists
from .config import MISSIONS
from .version import __version__ as version


def create_rover(mission_id: str, **config):
    """
        Verifies input parameters, creates rover object
    """
    return Rover(mission_id, **config)


class Rover:
    __attrs__ = ["resolution", "path", "page_num", "cameras", ""]

    def __init__(self, mission_id:str, **config):
        self.init(mission_id=mission_id,**config)

    def init(self, mission_id:str, **config):
        self.id = mission_id
        self.name = MISSIONS.get(self.id)["name"]
        self.resolution_name = config.get("resolution")
        self.resolution = MISSIONS.get(self.id)['resolutions'][self.resolution_name]
        self.basepath = config.get("path")
        self.page_num = config.get("npages")
        self.format = MISSIONS.get(self.id)['formats'][self.resolution_name]

    def __repr__(self):
        return(f"<{self.name}:{version}>")

    def _download_image(self, image_url: str):
        try:
            image_data = get(image_url, stream=True)
            return image_data
        except Exception as e:
            print(f"Exception {e}")

    def _saveimage(self,
                   image_data,
                   filename: str):
        with open(filename, 'wb') as img:
            shutil.copyfileobj(image_data.raw, img)

    def _get_image_list(self, url: str):
        try:
            r = get(url)
            image_list = r.json()["images"]
            return image_list
        except Exception as e:
            print(f"Error: {e}")

    def _get_image_urls_by_type(self, imagelist: list):
        """
        Takes large, medium, small, fullres
        """
        urls = []
        ids = []
        for item in imagelist:
            urls.append(item["image_files"][self.resolution])
            ids.append(item["imageid"])
        return urls, ids

    def download_images(self):
        """
        Parses through all of the pages and downloads images
        """
        resolution = self.resolution
        basepath = self.basepath
        page_num = self.page_num
        filepath = os.path.join(basepath, self.id, resolution)
        if not checkpath(filepath):
            os.makedirs(filepath)
        url = f"https://mars.nasa.gov/rss/api/?feed=raw_images&category={self.id}&feedtype=json&num=50&page={page_num}&order=sol+desc&&&undefined"
        if page_num > 1:
            url = f"https://mars.nasa.gov/rss/api/?feed=raw_images&category={self.id}&feedtype=json&num=50&page={page_num}&order=sol+desc&&&extended="

        print(
            f"Fetching images with resolution: {self.resolution_name}, from page:{page_num}")
        imagelist = self._get_image_list(url=url)
        urls, ids = self._get_image_urls_by_type(imagelist=imagelist)
        for u, _id in zip(urls, ids):
            try:
                image_data = self._download_image(image_url=u)
                filename = os.path.join(filepath, f"{_id}.{self.format}")
                print(f"Now saving:{_id}")
                self._saveimage(image_data=image_data,
                                filename=filename)
            except Exception as e:
                print(f"Error {e} occured downloading image {_id}")
        print("Download Complete!")
