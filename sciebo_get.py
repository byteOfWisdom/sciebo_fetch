import zipfile
from urllib import request
import tempfile


def get_sciebo_directory(url: str, cache_locally=False) -> zipfile.ZipFile:
    response = request.urlopen(url)
    storage = tempfile.TemporaryFile()
    storage.write(response.read())
    storage.seek(0)
    zf = zipfile.ZipFile(storage)
    print(zf.namelist())
    return None


fetch = get_sciebo_directory
