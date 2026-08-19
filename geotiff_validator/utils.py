from osgeo import gdal
from pathlib import Path


def open_dataset(filename: str) -> (gdal.Dataset, Exception):
    if not Path(filename).is_file():
        return None, Exception("File does not exist")

    dataset = None
    try:
        dataset = gdal.Open(filename)
    except Exception as e:
        return None, e

    return dataset, None

def file_has_tiff_extension(filename: str) -> bool:
    return filename.endswith(".tif") or filename.endswith(".tiff")