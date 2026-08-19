from geotiff_validator.utils import open_dataset


def test_open_dataset():
    dataset, error = open_dataset("tests/data/single_files/test_plaingeotiff.tif")
    assert error is None
    assert dataset is not None

def test_error_on_missing_file():
    dataset, error = open_dataset("tests/data/single_files/nonexistent.tif")
    assert error is not None
    assert dataset is None