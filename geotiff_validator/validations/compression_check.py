from geotiff_validator.geotiff import get_geotiff_compression
from geotiff_validator.validations import validator

from typing import Iterable

class CompressionValidator(validator.Validator):
    """The GeoTiff must be compressed with LZW"""

    code = 2
    message = "Geotiff is not compressed with LZW"

    def check(self) -> Iterable[str]:
        compression = get_geotiff_compression(self.dataset_header_info)
        if compression is None:
            return [self.message + ", no compression was found"]
        elif compression != "LZW":
            return [self.message + f", compression '{compression}' was found"]
        else:
            return []
