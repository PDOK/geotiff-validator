from osgeo import gdal, ogr

def open_dataset(filename: str) -> gdal.Dataset:
    dataset = None
    try:
        dataset = gdal.Open(filename)
    except Exception as e:
        return None, e

    return dataset, None

def file_has_tiff_extension(filename: str) -> bool:
    return filename.endswith(".tif") or filename.endswith(".tiff")