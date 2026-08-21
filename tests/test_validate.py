from geotiff_validator.validate import validate


def test_cog_valid():
    validations, required_validators, recommended_validators, success = validate(geotiff_path="tests/data/single_files/test_correct.tif", folder_path=None, required_validations="1", recommended_validations="", definitions_path=None, validations_path="")
    assert len(validations) == 0
    assert success
    assert len(required_validators) == 1

def test_cog_invalid():
    validations, required_validators, recommended_validators, success = validate(geotiff_path="tests/data/single_files/test_nocog.tif", folder_path=None, required_validations="1", recommended_validations="", definitions_path=None, validations_path="")
    assert not success
    assert len(validations) == 1
    assert len(required_validators) == 1

def test_compression_valid():
    validations, required_validators, recommended_validators, success = validate(geotiff_path="tests/data/single_files/test_correct.tif", folder_path=None, required_validations="2", recommended_validations="", definitions_path=None, validations_path="")
    assert success
    assert len(validations) == 0
    assert len(required_validators) == 1

def test_compression_no_compression():
    validations, required_validators, recommended_validators, success = validate(geotiff_path="tests/data/single_files/test_cog_no_compression.tif", folder_path=None, required_validations="2", recommended_validations="", definitions_path=None, validations_path="")
    assert not success
    assert len(validations) == 1
    assert len(required_validators) == 1

def test_compression_wrong_compression():
    validations, required_validators, recommended_validators, success = validate(geotiff_path="tests/data/single_files/test_cog_zstd_compression.tif", folder_path=None, required_validations="2", recommended_validations="", definitions_path=None, validations_path="")
    assert not success
    assert len(validations) == 1
    assert len(required_validators) == 1

def test_views_valid():
    validations, required_validators, recommended_validators, success = validate(geotiff_path="tests/data/single_files/test_correct.tif", folder_path=None, required_validations="3", recommended_validations="", definitions_path=None, validations_path="")
    assert success
    assert len(validations) == 0
    assert len(required_validators) == 1

def test_views_invalid():
    validations, required_validators, recommended_validators, success = validate(geotiff_path="tests/data/single_files/test_overviews.tif", folder_path=None, required_validations="3", recommended_validations="", definitions_path=None, validations_path="")
    assert not success
    assert len(validations) == 1
    assert len(required_validators) == 1

def test_recommendation():
    validations, required_validators, recommended_validators, success = validate(geotiff_path="tests/data/single_files/test_nocog.tif", folder_path=None, required_validations="", recommended_validations="1", definitions_path=None, validations_path="")
    assert success
    assert len(validations) == 1
    assert len(required_validators) == 0
    assert len(recommended_validators) == 1

def test_validation_schema_valid():
    validations, required_validators, recommended_validators, success = validate(geotiff_path=None, folder_path="tests/data/multiple_files/plain_geotiffs", required_validations="", recommended_validations="", definitions_path="tests/data/multiple_files/plain_geotiffs/schema_definition.json", validations_path="")
    assert len(validations) == 0
    assert success
    assert len(required_validators) == 1
    assert required_validators[0].code == 4

def test_validation_schema_invalid():
    validations, required_validators, recommended_validators, success = validate(geotiff_path=None, folder_path="tests/data/multiple_files/plain_geotiffs", required_validations="", recommended_validations="", definitions_path="tests/data/multiple_files/plain_geotiffs/differing_schema_definition.json", validations_path="")
    assert len(validations) == 3
    assert not success
    assert len(required_validators) == 1
    assert required_validators[0].code == 4

def test_validate_with_schema():
    validations, required_validators, recommended_validators, success = validate(geotiff_path=None, folder_path="tests/data/multiple_files/plain_geotiffs", required_validations="", recommended_validations="", definitions_path="", validations_path="tests/data/multiple_files/plain_geotiffs/validations.json")
    assert len(validations) == 2
    assert not success
    assert len(required_validators) == 1
    assert required_validators[0].code == 1