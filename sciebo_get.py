import zipfile
from urllib import request
import tempfile


class content:
    def __init__(self, zip: zipfile.Zipfile):
        self.zip = zip

    def ls(self) -> [str]:
        all_files = self.zip.namelist()
        not_dir = filter(lambda f: not self.zip.getinfo(f).is_dir(), all_files)
        return list(not_dir)

    def read_file(self, file: str) -> bytes:
        with self.zip.open(file) as handle:
            return handle.read()

    def np_loadable(self, file: str):
        data = str(self.read_file(file)).split("\n")
        return (line for line in data)

    def open(self, file: str):
        return self.zip.open(file)


def get_sciebo_directory(url: str, cache_locally=False) -> zipfile.ZipFile:
    response = request.urlopen(url)
    storage = tempfile.TemporaryFile()
    storage.write(response.read())
    storage.seek(0)
    zf = zipfile.ZipFile(storage)
    # print(zf.namelist())
    return zf


def fetch(url: str):
    return content(get_sciebo_directory(url))
    
