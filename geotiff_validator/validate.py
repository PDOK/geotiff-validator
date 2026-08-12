from geotiff_validator import utils


def validate(geotiff_path, folder_path, required_validations="", recommended_validations=""):
    if geotiff_path is not None:
        dataset = utils.open_dataset(geotiff_path)

    else:
        # folder_path must be not None
        pass