from geotiff_validator.validations import validator
from typing import Iterable

class SchemaValidator(validator.Validator):

    code = 4
    message = "GeoTiff must conform to generated schema"

    def check(self) -> Iterable[str]:
        return []