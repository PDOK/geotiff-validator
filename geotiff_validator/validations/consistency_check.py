from typing import Iterable

from geotiff_validator.generate import get_shared_attributes, SharedTifAttributes
from geotiff_validator.validations import validator

class ConsistencyValidator(validator.Validator):
    """Data structure must be equal for all files"""

    code = 5
    message = "File dimensions, CRS, compression, data type and interleave must be equal for all files"
    all_files = True

    def check(self) -> Iterable[str]:
        result = []

        if self.file_list is None or len(self.file_list) <= 1:
            return []
        first_attributes = get_shared_attributes(self.file_list[0], None, None)
        for other_file in self.file_list[1:]:
            other_attributes = get_shared_attributes(other_file, None, None)
            if first_attributes != other_attributes:
                error_message = f"File {self.file_list[0]} has an attribute mismatch with {other_file}:"
                error_message += "\n"
                error_message += SharedTifAttributes.diff_string(first_attributes, other_attributes)
                result.append(error_message)
        return result