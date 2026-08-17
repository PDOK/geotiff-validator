from geotiff_validator.generate import SharedTifAttributes, from_gdal_info, from_generated_schema
from geotiff_validator.validations import validator
from typing import Iterable

class SchemaValidator(validator.Validator):

    code = 4
    message = "GeoTiff must conform to generated schema"

    def check(self) -> Iterable[str]:
        file_shared_tif_attributes = from_gdal_info(self.dataset_header_info)
        schema_shared_tif_attributes = from_generated_schema(self.schema)
        print(file_shared_tif_attributes)
        print(schema_shared_tif_attributes)
        print(file_shared_tif_attributes == schema_shared_tif_attributes)
        return []