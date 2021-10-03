import os
import shutil
from .tools import checkpath, get, n_pages, give_me_time
from .config import MISSIONS
from .version import __version__ as version
import pandas as pd

def create_rover(mission_id: str, **config):
    """
        Verifies input parameters, creates rover object
    """
    return Rover(mission_id, **config)


class Rover:
    __attrs__ = ["resolution", "path", "page_num", "cameras", ""]

    def __init__(self, mission_id: str, **config):
        self.init(mission_id=mission_id, **config)

    def init(self, mission_id: str, **config):
        self.id = mission_id
        self.status_url = MISSIONS.get(self.id)["status_url"]
        self.stats_url = MISSIONS.get(self.id)["stats_url"]
        self.name = MISSIONS.get(self.id)["name"]
        self.resolution_name = config.get("resolution")
        self.resolution = MISSIONS.get(
            self.id)['resolutions'][self.resolution_name]
        self.basepath = config.get("path")
        self.pagenum = config.get("pagenum")
        self.npages = config.get("npages")
        self.format = MISSIONS.get(self.id)['formats'][self.resolution_name]

    def __repr__(self):
        return(f"<{self.name}:{version}>")

    def _get_image_data(self, image_url: str):
        try:
            image_data = get(image_url, stream=True)
            return image_data
        except Exception as e:
            print(f"Exception {e}")

    def _write_image(self,
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

    def _get_stub(self, pagenum: int):
        """
        data resource request url
        """
        url = f"https://mars.nasa.gov/rss/api/?feed=raw_images&category={self.id}&feedtype=json&num=50&page={pagenum}&order=sol+desc&&&undefined"
        if pagenum > 1:
            url = f"https://mars.nasa.gov/rss/api/?feed=raw_images&category={self.id}&feedtype=json&num=50&page={pagenum}&order=sol+desc&&&extended="
        return url

    def _image_download_wrapper(self, pagenums):
        filepath = os.path.join(self.basepath, self.id, self.resolution)
        if not checkpath(filepath):
            os.makedirs(filepath)
        try:
            for pagenum in pagenums:
                url = self._get_stub(pagenum=pagenum)
                print(
                    f"Fetching images with resolution: {self.resolution_name}, from page:{pagenum}")
                imagelist = self._get_image_list(url=url)
                urls, ids = self._get_image_urls_by_type(imagelist=imagelist)
                for u, _id in zip(urls, ids):
                    try:
                        image_data = self._get_image_data(image_url=u)
                        filename = os.path.join(filepath, f"{_id}.{self.format}")
                        print(f"Now saving:{_id}.{self.format}")
                        self._write_image(image_data=image_data,
                                        filename=filename)
                    except Exception as e:
                        print(f"Error {e} occured downloading image {_id}")
                        return 1
        except KeyboardInterrupt:
            print(f"Keyboard Interrupt occured, cancelling download operation!")
            return 1
        print("Download complete!")
        return 0

    def _pages_to_download(self):
        npages = self.npages
        existing_npages = n_pages(self.stats_url)
        if npages:
            if not npages <= existing_npages:
                print(
                    f"Value of npages can't be greater than {existing_npages}")
                return 1
            pagenums = [n for n in range(1, npages+1)]
        else:
            pagenums = [self.pagenum]
        return pagenums

    def download_images(self):
        """
        Parses through all of the pages and downloads images
        """
        pagenums = self._pages_to_download()
        self._image_download_wrapper(pagenums)

    def _metadata_download_wrapper(self, pagenums):
        filepath = os.path.join(self.basepath, self.id, self.resolution)
        if not os.path.exists:
            os.makedirs(filepath)
        try:
            dfs = []
            for pagenum in pagenums:
                url = self._get_stub(pagenum=pagenum)
                il = self._get_image_list(url=url)
                dfs.append(pd.json_normalize(il, sep="_"))
            df = pd.concat(dfs) 
            fn = os.path.join(filepath, f"{len(pagenum)}_metadata_at_{give_me_time}.xlsx")
            df.reset_index(drop=True).to_excel(fn,index=False)
        except KeyboardInterrupt:
            print("Keyboard interrupt occured, stopping download operation!")
            return 1
        return 0

    def download_metadata(self):
        pagenums = self._pages_to_download()
        raise self._metadata_download_wrapper(pagenums=pagenums)
