from geotiff_validator import __version__
from osgeo import gdal
from os import listdir

import json
import sys
import typing

class SharedTifAttributes:
    cog_enabled: bool
    cog_block_size_x: typing.Optional[int]
    cog_block_size_y: typing.Optional[int]
    compression: typing.Optional[str]
    interleave: str
    size_x: int
    size_y: int
    crs: int
    data_type: str

    def __init__(self, cog_enabled: bool, compression: typing.Optional[str], interleave: str, size_x: int, size_y: int, crs: str, data_type: str, cog_block_size_x: typing.Optional[int], cog_block_size_y: typing.Optional[int]):
        self.cog_enabled = cog_enabled
        self.compression = compression
        self.interleave = interleave
        self.size_x = size_x
        self.size_y = size_y
        self.crs = crs
        self.data_type = data_type
        self.cog_block_size_x = cog_block_size_x
        self.cog_block_size_y = cog_block_size_y

    def __eq__(self, other):
        return (self.cog_enabled == other.cog_enabled and self.compression == other.compression
                and self.interleave == other.interleave and self.size_x == other.size_x
                and self.size_y == other.size_y and self.crs == other.crs and self.data_type == other.data_type
                and self.cog_block_size_x == other.cog_block_size_x and self.cog_block_size_y == other.cog_block_size_y)

def from_gdal_info(gdal_info: dict) -> SharedTifAttributes:
    stac = gdal_info["stac"]
    metadata = gdal_info["metadata"]

    interleave = ""
    cog_enabled = False
    compression = None
    crs = stac["proj:epsg"]
    data_type = stac["raster:bands"][0]["data_type"] # This should probably be checked conditionally
    cog_block_size_x = None
    cog_block_size_y = None

    image_structure = metadata.get("IMAGE_STRUCTURE")
    if image_structure is not None:
        interleave = image_structure["INTERLEAVE"]
        if image_structure.get("LAYOUT") == "COG":
            cog_enabled = True
            cog_block_size_x = gdal_info["bands"][0]["block"][0]
            cog_block_size_y = gdal_info["bands"][0]["block"][1]
        compression = image_structure.get("COMPRESSION")

    return SharedTifAttributes(cog_enabled, compression, interleave, gdal_info["size"][0], gdal_info["size"][1], crs, data_type, cog_block_size_x, cog_block_size_y)

def get_shared_attributes(folder: str, dir_list: typing.List[str]):
    for file in dir_list:
        if file.endswith(".tif"):
            full_path = folder + "/" + file
            ds = None
            try:
                ds = gdal.Open(full_path)
            except:
                print(f"Could not parse header from file '{full_path}'")
                sys.exit(1)
            header_info = gdal.Info(ds, format='json', showColorTable=False)
            return from_gdal_info(header_info)
    return None

def generate_definitions(folder: str):
    result = {}

    dir_list = listdir(folder)
    shared_attributes = get_shared_attributes(folder, dir_list)
    if shared_attributes is None:
        print("Could not find any tif file in folder")
        sys.exit(1)

    result["cog_enabled"] = shared_attributes.cog_enabled
    result["cog_block_size_x"] = shared_attributes.cog_block_size_x
    result["cog_block_size_y"] = shared_attributes.cog_block_size_y
    result["compression"] = shared_attributes.compression
    result["crs"] = shared_attributes.crs
    result["data_type"] = shared_attributes.data_type
    result["interleave"] = shared_attributes.interleave
    result["size_x"] = shared_attributes.size_x
    result["size_y"] = shared_attributes.size_y

    file_structures = []

    for file in dir_list:
        if file.endswith(".tif"):
            full_path = folder + "/" + file
            ds = None
            try:
                ds = gdal.Open(full_path)
            except:
                print(f"Could not parse header from file '{full_path}'")
                sys.exit(1)
            header_info = gdal.Info(ds, format='json', showColorTable=False)
            file_attributes = from_gdal_info(header_info)
            if file_attributes != shared_attributes:
                print(f"Mismatched attributes, expected {vars(shared_attributes)} but got {vars(file_attributes)}")
                sys.exit(1)

            my_struct = {"bands": header_info["bands"], "cornerCoordinates": header_info["cornerCoordinates"], "file_name": file, "raster_count": ds.RasterCount }
            file_structures.append(my_struct)

    result["files"] = file_structures

    return result