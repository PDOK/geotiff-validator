from geotiff_validator import __version__
from osgeo import gdal
from os import listdir

import json
import sys
import typing

from geotiff_validator.geotiff import geotiff_is_cog, get_geotiff_interleave, get_geotiff_compression, \
    get_geotiff_cog_block_dimensions, get_geotiff_data_type, get_geotiff_dimensions, get_geotiff_crs
from geotiff_validator.utils import file_has_tiff_extension

from typing import Dict, List

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

    def __init__(self, cog_enabled: bool, compression: typing.Optional[str], interleave: str, size_x: int, size_y: int, crs: int, data_type: str, cog_block_size_x: typing.Optional[int], cog_block_size_y: typing.Optional[int]):
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
    dimensions = get_geotiff_dimensions(gdal_info)
    interleave = get_geotiff_interleave(gdal_info)
    cog_enabled = geotiff_is_cog(gdal_info)
    compression = get_geotiff_compression(gdal_info)
    crs = get_geotiff_crs(gdal_info)
    data_type = get_geotiff_data_type(gdal_info)
    cog_block_size = get_geotiff_cog_block_dimensions(gdal_info)

    return SharedTifAttributes(cog_enabled, compression, interleave, dimensions[0], dimensions[1], crs, data_type, cog_block_size[0], cog_block_size[1])

def get_shared_attributes(file:str | None, folder: str, dir_list: typing.List[str]):
    if file is not None:
        ds = None
        try:
            ds = gdal.Open(file)
        except:
            print(f"Could not parse header from file '{file}'")
            sys.exit(1)
        header_info = gdal.Info(ds, format='json', showColorTable=False)
        return from_gdal_info(header_info)
    else:
        for file in dir_list:
            if file_has_tiff_extension(file):
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

def get_file_specifics(header_info, file_name: str, dataset):
    return {"bands": header_info["bands"], "cornerCoordinates": header_info["cornerCoordinates"], "file_name": file_name, "raster_count": dataset.RasterCount}

def append_file_structure(filepath: str, file_name: str, file_structures: List[str], shared_attributes: SharedTifAttributes):
    ds = None
    try:
        ds = gdal.Open(filepath)
    except Exception:
        print(f"Could not parse header from file '{filepath}'")
        sys.exit(1)
    header_info = gdal.Info(ds, format='json', showColorTable=False)
    file_attributes = from_gdal_info(header_info)
    if file_attributes != shared_attributes:
        print(f"Mismatched attributes, expected {vars(shared_attributes)} but got {vars(file_attributes)}")
        sys.exit(1)

    file_structure_dict = get_file_specifics(header_info, file_name, ds)
    file_structures.append(file_structure_dict)

def generate_definitions(file:str, folder: str):
    result = {}

    dir_list = listdir(folder)
    shared_attributes = get_shared_attributes(file, folder, dir_list)
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

    if folder is not None and folder != "":
        for file in dir_list:
            if file_has_tiff_extension(file):
                full_path = folder + "/" + file
                append_file_structure(full_path, file, file_structures, shared_attributes)
    else:
        append_file_structure(file, file.rsplit("/", 1)[-1], file_structures, shared_attributes)

    result["files"] = file_structures

    return result