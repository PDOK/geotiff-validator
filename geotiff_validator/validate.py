from geotiff_validator import utils
from geotiff_validator.validations import CogValidator


def validate(geotiff_path, folder_path, required_validations="", recommended_validations=""):
    success = True
    validation_results = []

    if geotiff_path is not None:
        dataset = utils.open_dataset(geotiff_path)
        validators = [CogValidator]
        for validator in validators:
            result = validator(dataset).validate()
            if result is not None:
                validation_results.append(result)
                validation_error = True
                success = False
    else:
        # folder_path must be not None
        pass
    print(validation_results)