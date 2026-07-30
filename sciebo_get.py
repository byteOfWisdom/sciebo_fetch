import zipfile
from urllib import request
import tempfile
import glob


class content:
    def __init__(self, zip: zipfile.ZipFile, cache_as=False):
        self.zip = zip

    def ls(self) -> [str]:
        all_files = self.zip.namelist()
        not_dir = filter(lambda f: not self.zip.getinfo(f).is_dir(), all_files)
        return list(not_dir)

    def read_file(self, file: str) -> bytes:
        with self.zip.open(file) as handle:
            return handle.read()

    def np_loadable(self, file: str):
        raw_data = self.read_file(file)
        data = raw_data.decode("utf-8").split("\n")
        return (line for line in data)

    def open(self, file: str):
        return self.zip.open(file)


def get_sciebo_directory(url: str, cache_locally=False) -> zipfile.ZipFile:
    response = request.urlopen(url)
    storage = None
    if not cache_locally:
        storage = tempfile.TemporaryFile()
        storage.write(response.read())
    else:
        cache_file = open(cache_locally, "wb")
        cache_file.write(response.read())
        cache_file.close()
        storage = open(cache_locally, "rb")
    storage.seek(0)
    zf = zipfile.ZipFile(storage)
    return zf


def fetch(url: str, cache_as=False, force_load=False):
    if cache_as:
        temp_path = tempfile.gettempdir()
        if len(glob.glob(temp_path + cache_as)) > 0 and not force_load:
            print("caching and found")
            return content(zipfile.ZipFile(temp_path + cache_as, "r"))
        else:
            print("caching but not found")
            return content(get_sciebo_directory(url, temp_path + cache_as))
    return content(get_sciebo_directory(url))
    
