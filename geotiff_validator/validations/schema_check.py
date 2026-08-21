from geotiff_validator.generate import from_gdal_info, from_generated_schema, get_file_specifics
from geotiff_validator.validations import validator
from typing import Iterable


class SchemaValidator(validator.Validator):
    """The GeoTiff must match the generated schema"""

    code = 4
    message = "GeoTiff must conform to generated schema"

    def check(self) -> Iterable[str]:
        result = []
        if self.schema is None:
            result.append("The schema definition is missing")
            return result

        file_shared_tif_attributes = from_gdal_info(self.dataset_header_info)
        schema_shared_tif_attributes = from_generated_schema(self.schema)
        if file_shared_tif_attributes != schema_shared_tif_attributes:
            result.append(f"Expected attributes {vars(schema_shared_tif_attributes)} but got {vars(file_shared_tif_attributes)}")

        matched_schema_specifics = next((item for item in self.schema["files"] if item["file_name"] == self.filename), None)
        if matched_schema_specifics is None:
            result.append(f"File '{self.filename}' was not found in schema")
            return result

        file_specifics = get_file_specifics(self.dataset_header_info, self.filename, self.dataset)
        if matched_schema_specifics != file_specifics:
            diffs = {k
             for k in matched_schema_specifics.keys() | file_specifics.keys()
             if matched_schema_specifics.get(k) != file_specifics.get(k)}
            for diff in diffs:
                result.append(f"File '{self.filename}' has a mismatch in key '{diff}'")

        return result