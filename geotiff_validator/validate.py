from geotiff_validator import utils
from geotiff_validator.validations import CogValidator
from osgeo import gdal

def validate(geotiff_path, folder_path, required_validations="", recommended_validations=""):
    success = True
    validation_results = []

    if geotiff_path is not None:
        dataset = utils.open_dataset(geotiff_path)
        dataset_header_info = gdal.Info(dataset, format='json', showColorTable=False)
        validators = [CogValidator]
        for validator in validators:
            result = validator(dataset, dataset_header_info).validate()
            if result is not None:
                validation_results.append(result)
                validation_error = True
                success = False
    else:
        # folder_path must be not None
        pass
    print(validation_results)