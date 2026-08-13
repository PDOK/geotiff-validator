from geotiff_validator.validations import validator

from typing import Iterable
from osgeo import gdal

class CogValidator(validator.Validator):

    code = 1
    message = "Geotiff is not a Cloud Optimized GeoTIFF(COG)"

    def check(self) -> Iterable[str]:
        header_info = gdal.Info(self.dataset, format='json', showColorTable=False)

        return ["Not cog"]


