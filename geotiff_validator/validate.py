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

from typing import Dict, List


def get_validations_for_validating_process(required_validations: str, recommended_validations: str,
                                           definitions: bool) -> (list, list):
    required_validators = []
    recommended_validators = []

    if required_validations == "" and recommended_validations == "":
        required_validators = get_default_validators(definitions)
    else:
        required_validations_list = []
        recommended_validations_list = []

        if required_validations != "":
            required_validations_list = [int(x.strip()) for x in required_validations.split(",")]
        if recommended_validations != "":
            recommended_validations_list = [int(x.strip()) for x in recommended_validations.split(",")]

        if definitions:
            if SchemaValidator.code not in required_validations_list:
                required_validations_list.append(SchemaValidator.code)

        # Deduplicate the required validations
        recommended_validations_list = [x for x in recommended_validations_list if x not in required_validations_list]

        validator_map = get_validator_map(definitions)
        for integer in required_validations_list:
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


def append_validations_for_file(file_path: str, validation_results, required_validators: List[validations.Validator], recommended_validators: List[validations.Validator],
                                definitions: dict | None):
    success = True
    dataset, error = utils.open_dataset(file_path)
    if error is not None:
        item = format_result(
            filename=file_path.rsplit("/", 1)[-1],
            validation_code=0,
            validation_description="The file must be a GeoTiff file",
            trace=["The file is not a GeoTiff file"],
        )
        validation_results.append(item)
        return False

    dataset_header_info = gdal.Info(dataset, format='json', showColorTable=False)
    for validator in required_validators:
        result = validator(file_path.rsplit("/", 1)[-1], dataset, dataset_header_info, definitions).validate()
        if result is not None:
            result["level"] = "error"
            success = False
            validation_results.append(result)
    for validator in recommended_validators:
        result = validator(file_path.rsplit("/", 1)[-1], dataset, dataset_header_info, definitions).validate()
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


def validate(geotiff_path, folder_path, required_validations: str, recommended_validations: str, definitions_path: str):
    success = True

    definitions = None
    try:
        definitions = get_definitions(definitions_path)
    except:
        pass
    required_validators, recommended_validators = get_validations_for_validating_process(required_validations,
                                                                                         recommended_validations,
                                                                                         definitions is not None)
    validation_results = []

    if geotiff_path is not None:
        success = success and append_validations_for_file(geotiff_path, validation_results, required_validators,
                                                          recommended_validators, definitions)
    else:
        # folder_path must be not None
        dir_list = listdir(folder_path)
        for filename in dir_list:
            if utils.file_has_tiff_extension(filename):
                file_path = folder_path
                if not file_path.endswith("/"):
                    file_path += "/"
                file_path += filename
                success = success and append_validations_for_file(file_path, validation_results, required_validators,
                                                                  recommended_validators, definitions)

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
    validation_classes = get_validator_classes(true)
    return OrderedDict(
        (klass.code, klass.__doc__) for klass in validation_classes
    )
