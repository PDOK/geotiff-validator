
def geotiff_header_is_cog(header: dict) -> bool:
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