from osgeo import gdal, ogr

def open_dataset(filename: str) -> gdal.Dataset:
    dataset = None
    try:
        dataset = gdal.Open(filename)
    except Exception as e:
        return None, e

    return dataset, None
