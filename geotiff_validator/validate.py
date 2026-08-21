from collections import OrderedDict

import json
import yaml

from os import listdir

from geotiff_validator import utils

from osgeo import gdal
from geotiff_validator import validations as validation
from geotiff_validator import validations
from geotiff_validator.validations.schema_check import SchemaValidator
from geotiff_validator.validations.validator import format_result

from typing import List

def get_validators(required_validations_ints: list[int], recommended_validations_ints: list[int], definitions: bool) -> (list, list):
    required_validators = []
    recommended_validators = []

    if definitions:
        if SchemaValidator.code not in required_validations_ints:
            required_validations_ints.append(SchemaValidator.code)

   # Deduplicate the required validations
    recommended_validations_list = [x for x in recommended_validations_ints if x not in required_validations_ints]

    validator_map = get_validator_map(definitions)
    for integer in required_validations_ints:
        matched = validator_map.get(integer, None)
        if matched is None:
            print("Could not find the validating rule")
        else:
            required_validators.append(matched)

    for integer in recommended_validations_list:
        matched = validator_map.get(integer, None)
        if matched is None:
            print("Could not find the validating rule")
        else:
            recommended_validators.append(matched)

    return required_validators, recommended_validators

def get_validations_from_validations_path(validations_path: str, definitions: bool) -> (list, list):
    data = None
    if validations_path.endswith(".yaml"):
        with open(validations_path, "r") as file:
            data = json.load(file)
    else:
        with open(validations_path, "r") as file:
            data = json.load(file)

    required_validations_ints = data.get("required_validations", [])
    recommended_validations_ints = data.get("recommended_validations", [])

    return get_validators(required_validations_ints, recommended_validations_ints, definitions)

def get_validations_for_validating_process(required_validations: str, recommended_validations: str,
                                           definitions: bool, validations_path: str) -> (list, list):
    required_validators = []
    recommended_validators = []

    if validations_path != "":
        required_validators, recommended_validators = get_validations_from_validations_path(validations_path, definitions)
    elif required_validations == "" and recommended_validations == "" and not definitions:
        required_validators = get_default_validators(definitions)
    else:
        required_validations_list = []
        recommended_validations_list = []

        if required_validations != "":
            required_validations_list = [int(x.strip()) for x in required_validations.split(",")]
        if recommended_validations != "":
            recommended_validations_list = [int(x.strip()) for x in recommended_validations.split(",")]

        required_validators, recommended_validators = get_validators(required_validations_list, recommended_validations_list, definitions)

    return required_validators, recommended_validators


def append_validations_for_file(file_path: str, validation_results, required_validators: List[validations.Validator], recommended_validators: List[validations.Validator],
                                definitions: dict | None):
    success = True
    file_name = file_path.rsplit("/", 1)[-1]
    dataset, error = utils.open_dataset(file_path)
    if error is not None:
        item = format_result(
            filename=file_name,
            validation_code=0,
            validation_description="The file must be a GeoTiff file",
            trace=["The file is not a GeoTiff file"],
        )
        validation_results.append(item)
        return False

    dataset_header_info = gdal.Info(dataset, format='json', showColorTable=False)
    for validator in required_validators:
        result = validator(file_name, dataset, dataset_header_info, definitions).validate()
        if result is not None:
            result["level"] = "error"
            success = False
            validation_results.append(result)
    for validator in recommended_validators:
        result = validator(file_name, dataset, dataset_header_info, definitions).validate()
        if result is not None:
            result["level"] = "recommendation"
            validation_results.append(result)
    return success


def get_definitions(definitions_path: str):
    if definitions_path is None or definitions_path == "":
        return None

    if definitions_path.endswith(".json"):
        with open(definitions_path, "r") as file:
            data = json.load(file)
            return data

    return None

def check_expected_files(definitions: dict | None, geotiff_path, folder_path, validation_results):
    expected_files = set()
    for file_structure in definitions["files"]:
        expected_files.add(file_structure["file_name"])

    found_files = set()
    if geotiff_path is not None:
        geotiff_file = geotiff_path.rsplit("/", 1)[-1]
        found_files.add(geotiff_file)
    else:
        dir_list = listdir(folder_path)
        for filename in dir_list:
            if utils.file_has_tiff_extension(filename):
                found_files.add(filename.rsplit("/", 1)[-1])

    if found_files != expected_files:
        missing_files = expected_files - found_files
        extra_files = found_files - expected_files
        if len(missing_files) > 0:
            validation_results.append(format_result("-", SchemaValidator.code, SchemaValidator.__doc__, f"The following files were expected but missing: {missing_files}"))
        # This check could be removed as the check also happens in the SchemaValidator itself
        if len(extra_files) > 0:
            validation_results.append(format_result("-", SchemaValidator.code, SchemaValidator.__doc__, f"The following files not expected but present: {extra_files}"))

    return

def validate(geotiff_path, folder_path, required_validations: str, recommended_validations: str, definitions_path: str, validations_path):
    success = True

    definitions = None
    try:
        definitions = get_definitions(definitions_path)
    except Exception as e:
        print(f"Failed to parse definitions: Error message '{e}'")
        exit(1)
    try:
        required_validators, recommended_validators = get_validations_for_validating_process(required_validations,
                                                                                         recommended_validations,
                                                                                         definitions is not None, validations_path)
    except Exception as e:
        print(f"Failed to construct validations: Error message '{e}'")
        exit(1)
    validation_results = []

    # We need to validate that all files are present, this cannot be done on a file-by-file basis, so we do it separately
    if definitions is not None:
        check_expected_files(definitions, geotiff_path, folder_path, validation_results)

    if geotiff_path is not None:
        success = append_validations_for_file(geotiff_path, validation_results, required_validators,
                                                          recommended_validators, definitions) and success
    else:
        # folder_path must be not None
        dir_list = listdir(folder_path)
        for filename in dir_list:
            if utils.file_has_tiff_extension(filename):
                file_path = folder_path
                if not file_path.endswith("/"):
                    file_path += "/"
                file_path += filename
                file_success = append_validations_for_file(file_path, validation_results, required_validators,
                                                           recommended_validators, definitions)
                success = success and file_success

    return validation_results, required_validators, recommended_validators, success


def get_default_validators(definitions: bool):
    return get_validator_classes(definitions)


def get_validator_classes(definitions: bool):
    validator_classes = [
        getattr(validation, validator)
        for validator in validation.__all__
        if issubclass(getattr(validation, validator), validations.Validator)
    ]
    if definitions:
        validator_classes.append(SchemaValidator)

    return sorted(validator_classes, key=lambda v: v.code)


def get_validator_map(definitions: bool):
    return {x.code: x for x in get_validator_classes(definitions)}


def get_validation_descriptions(legacy):
    validation_classes = get_validator_classes(True)
    return OrderedDict(
        (klass.code, klass.__doc__) for klass in validation_classes
    )
