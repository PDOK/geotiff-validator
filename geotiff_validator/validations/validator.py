from typing import Iterable, List, Dict
from osgeo import gdal

def format_result(
        filename: str,
        validation_code: int,
        validation_description: str,
        trace: List[str],
):
    return {
        "filename": filename,
        "validation_code": validation_code,
        "validation_description": validation_description,
        "locations": trace,
    }

class Validator:
    code: int # The code number for each validator, unique per validator
    message: str # The description of what the validator does
    all_files: bool # True if the Validator is for checking all the files simultaneously, False for checking the files separately

    def __init__(self, filename:str | None, file_list: list[str] | None, dataset: gdal.Dataset | None, dataset_header_info, schema, **kwargs):
        self.filename = filename
        self.file_list = file_list
        self.dataset: gdal.Dataset | None = dataset
        self.dataset_header_info = dataset_header_info
        self.schema = schema

    def validate(self) -> Dict[str, object] | None:
        """Run validation on geotiff."""
        results = list(self.check())
        if results:
            return format_result(
                filename=self.filename or "-",
                validation_code=self.code,
                validation_description=self.__doc__,
                trace=results,
            )
        else:
            return None

    def check(self) -> Iterable[str]:
        """Check the tiff file and return a list of validation results."""
        ...
