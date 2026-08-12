from osgeo import gdal, ogr

def open_dataset(filename: str) -> gdal.Dataset:
    dataset = None
    try:
        dataset = gdal.Open(filename)
    except Exception as e:
        print(e)
        #error_handler(gdal.CE_Failure, 0, e.args[0])

    return dataset
