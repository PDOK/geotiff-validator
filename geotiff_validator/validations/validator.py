
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

    def __init__(self, dataset, **kwargs):
        self.dataset: gdal.Dataset = dataset

    def validate(self) -> Dict[str, List[str]]:
        """Run validation at geopackage."""
        results = list(self.check())
        if results:
            return format_result(
                validation_code=self.validation_code,
                validation_description=self.__doc__,
                trace=results,
            )

    @abstractmethod
    def check(self) -> Iterable[str]:
        """Check the tiff file and return a list of validation results."""
        ...
