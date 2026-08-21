from geotiff_validator.validations import validator
from typing import Iterable

class ViewsValidator(validator.Validator):
    """The GeoTiff must not have views"""

    code = 3
    message = "GeoTiff has views"

    def check(self) -> Iterable[str]:
        bands = self.dataset_header_info.get("bands", None)
        if bands is None:
            return []
        for band in bands:
            overviews = band.get("overviews", None)
            if overviews is not None:
                band_number = band.get("band")
                return [f"GeoTiff has unexpected views present on bands, example: band '{band_number}'"]

        return []