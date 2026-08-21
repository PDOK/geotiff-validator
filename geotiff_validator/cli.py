import logging

import sys
import click
import click_log
import json
import time

from osgeo import gdal
from geotiff_validator.generate import generate_definitions
from geotiff_validator import validate
from geotiff_validator import output

from datetime import datetime

logger = logging.getLogger(__name__)
click_log.basic_config(logger)

@click.group()
def cli():
    pass


# noinspection unreachable-code
@cli.command(
    name="validate",
    help=(
            "Geotiff validator validating one or more tiff files."
    ),
)
@click.option(
    "--geotiff-path",
    envvar="GEOTIFF_PATH",
    show_envvar=True,
    required=False,
    default=None,
    help="Path pointing to the geotiff .tif file",
    type=click.types.Path(
        file_okay=True,
        dir_okay=False,
        readable=True,
        writable=False,
        allow_dash=False,
    ),
)
@click.option(
    "--folder-path",
    envvar="FOLDER_PATH",
    show_envvar=True,
    required=False,
    default=None,
    help="Path pointing to a folder containing geotiff .tif files",
    type=click.types.Path(
        file_okay=False,
        dir_okay=True,
        readable=True,
        writable=False,
        allow_dash=False,
    ),
)
@click.option(
    "--definitions-path",
    show_envvar=True,
    required=False,
    default=None,
    help=(
            "Path pointing to the geotiff-definitions JSON or YAML file (generate this file by calling the "
            "generate-definitions command)"
    ),
    type=click.types.Path(
        exists=True,
        file_okay=True,
        dir_okay=False,
        readable=True,
        writable=False,
        allow_dash=False,
    ),
)
@click.option(
    "--required-validations",
    show_envvar=True,
    required=False,
    default="",
    envvar="REQUIRED_VALIDATIONS",
    help=(
            "Comma-separated list of validations to run (e.g. --required-validations 1,2,3). If validations-path, required-validations and recommended-validations "
            "are not given, validate runs all validations"
    ),
)
@click.option(
    "--recommended-validations",
    show_envvar=True,
    required=False,
    default="",
    envvar="RECOMMENDED_VALIDATIONS",
    help=(
            "Comma-separated list of validations to run (e.g. --recommended-validations 1,2,3). If validations-path, required-validations and recommended-validations "
            "are not given, validate runs all validations"
    ),
)
@click.option(
    "--validations-path",
    show_envvar=True,
    required=False,
    default="",
    envvar="VALIDATIONS_PATH",
    help=(
            "Path pointing to the set of validations to run. If validations-path, required-validations and recommended-validations are not given, validate "
            "runs all validations"
    ),
)
@click.option(
    "--exit-on-fail",
    required=False,
    is_flag=True,
    help="Exit with code 1 when validation success is false.",
)
def geotiff_validator_command(
        geotiff_path: str,
        folder_path: str,
        required_validations: str,
        recommended_validations: str,
        validations_path: str,
        definitions_path: str,
        exit_on_fail: bool
):
    start_time = datetime.now()
    duration_start = time.monotonic()

    gdal.UseExceptions()

    if (geotiff_path is None and folder_path is None) or (geotiff_path is not None and folder_path is not None):
        logger.error("Give exactly one of --geotiff-path and --folder-path")
        sys.exit(2)

    validations, required_validators, recommended_validators, success = validate.validate(geotiff_path, folder_path, required_validations, recommended_validations, definitions_path, validations_path)

    duration_seconds = time.monotonic() - duration_start

    output.log_output(
        results=validations,
        success=success,
        start_time=start_time,
        duration_seconds=duration_seconds,
        required_validations_executed=[x.code for x in required_validators],
        recommended_validations_executed=[x.code for x in recommended_validators]
    )

    if not success and exit_on_fail:
        sys.exit(1)


# noinspection unreachable-code
@cli.command(
    name="generate-definitions",
    help=(
            "Generate schema definition for one or multiple tifs . Use the\
            generated definition JSON or YAML in the validation step by providing the\
            table definitions with the --definitions-path parameter."
    ),
)
@click.option(
    "--folder-path",
    envvar="FOLDER_PATH",
    required=False,
    default=None,
    show_envvar=True,
    help="Path pointing to the folder containing the geotiff files",
    type=click.types.Path(
        file_okay=False,
        dir_okay=True,
        readable=True,
        writable=False,
        allow_dash=False,
    ),
)
@click.option(
    "--geotiff-path",
    envvar="GEOTIFF_PATH",
    show_envvar=True,
    required=False,
    default=None,
    help="Path pointing to the geotiff .tif file",
    type=click.types.Path(
        file_okay=True,
        dir_okay=False,
        readable=True,
        writable=False,
        allow_dash=False,
    ),
)
def geotiff_generate_definitions_command(
        geotiff_path: str,
        folder_path: str
):
    gdal.UseExceptions()

    if (geotiff_path is None and folder_path is None) or (geotiff_path is not None and folder_path is not None):
        logger.error("Give exactly one of --geotiff-path and --folder-path")
        sys.exit(2)

    definitions = generate_definitions(geotiff_path, folder_path)
    json_string = json.dumps(definitions, indent=2)
    print(json_string)


@cli.command(
    name="show-validations",
    help="Show all the possible validations that can be executed in the validate command.",
)
@click.option(
    "--no-legacy",
    required=False,
    is_flag=True,
    help="Output without Legacy checks",
)
@click.option(
    "--yaml",
    required=False,
    is_flag=True,
    help="Output yaml",
)
@click_log.simple_verbosity_option(logger)
def geotiff_validator_command_show_validations(no_legacy, yaml):
    try:
        legacy = not no_legacy
        validation_codes = validate.get_validation_descriptions(legacy)
        output.print_output(validation_codes, yaml, yaml_indent=5)
    except Exception:
        logger.exception("Error while listing validations")
        sys.exit(1)

if __name__ == "__main__":
    cli()