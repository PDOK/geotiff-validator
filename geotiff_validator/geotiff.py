
def geotiff_is_cog(header: dict) -> bool:
    metadata = header["metadata"]
    image_structure = metadata.get("IMAGE_STRUCTURE")
    return image_structure is not None and image_structure.get("LAYOUT") == "COG"

def get_geotiff_interleave(header: dict) -> str:
    metadata = header["metadata"]
    image_structure = metadata.get("IMAGE_STRUCTURE")
    if image_structure is not None:
        return image_structure.get("INTERLEAVE", "")
    else:
        return ""

def get_geotiff_compression(header: dict) -> str | None:
    metadata = header["metadata"]
    image_structure = metadata.get("IMAGE_STRUCTURE")
    if image_structure is not None:
        return image_structure.get("COMPRESSION", None)
    else:
        return None

def get_geotiff_crs(header: dict) -> int:
    stac = header["stac"]
    return stac["proj:epsg"]

def get_geotiff_cog_block_dimensions(header: dict) -> (int | None, int | None):
    is_cog = geotiff_is_cog(header)
    if not is_cog:
        return None, None

    raster_bands = header.get("bands", None)
    if raster_bands is None or len(raster_bands) == 0:
        return None, None
    band = raster_bands[0]
    block = band.get("block", None)
    if block is None:
        return None, None
    return block[0], block[1]


def get_geotiff_data_type(header: dict) -> str | None:
    stac = header["stac"]
    raster_bands = stac.get("raster:bands")
    if raster_bands is None or len(raster_bands) == 0:
        return None
    return raster_bands[0]["data_type"]

def get_geotiff_dimensions(header: dict) -> (int, int):
    size = header["size"]
    return size[0], size[1]
