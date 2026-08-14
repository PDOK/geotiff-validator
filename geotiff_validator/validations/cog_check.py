from geotiff_validator.geotiff import geotiff_is_cog
from geotiff_validator.validations import validator

from typing import Iterable
from osgeo import gdal

class CogValidator(validator.Validator):

    code = 1
    message = "Geotiff is not a Cloud Optimized GeoTIFF(COG)"

    def check(self) -> Iterable[str]:
        is_cog = geotiff_is_cog(self.dataset_header_info)
        if not is_cog:
            return [CogValidator.message]
        else:
            return []
