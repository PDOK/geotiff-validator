from typing import Iterable, List, Dict
from abc import ABC, abstractmethod
from osgeo import gdal

def format_result(
        validation_code: str,
        validation_description: str,
        trace: List[str],
):
    return {
        "validation_code": validation_code,
        "validation_description": validation_description,
        "locations": trace,
    }

class Validator:
    code: int
    message: str

    def __init__(self, dataset, dataset_header_info, **kwargs):
        self.dataset: gdal.Dataset = dataset
        self.dataset_header_info = dataset_header_info

    def validate(self) -> Dict[str, List[str]] | None:
        """Run validation at geopackage."""
        results = list(self.check())
        if results:
            return format_result(
                validation_code=self.code,
                validation_description=self.__doc__,
                trace=results,
            )
        else:
            return None

    @abstractmethod
    def check(self) -> Iterable[str]:
        """Check the tiff file and return a list of validation results."""
        ...
