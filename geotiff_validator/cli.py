import logging

import sys
import click
import click_log
import json

from osgeo import gdal
from geotiff_validator.generate import generate_definitions
from geotiff_validator import validate

logger = logging.getLogger(__name__)
click_log.basic_config(logger)

@click.group()
def cli():
    pass

@cli.command(
    name="validate",
    help=(
            ""
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
            "Comma-separated list of validations to run (e.g. --required-validations 1,2,3). If validations-path and "
            "validations are not given, validate runs all validations"
    ),
)
@click.option(
    "--recommended-validations",
    show_envvar=True,
    required=False,
    default="",
    envvar="RECOMMENDED_VALIDATIONS",
    help=(
            "Comma-separated list of validations to run (e.g. --validations RQ1,RQ2,RQ3). If validations-path and "
            "validations are not given, validate runs all validations"
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
        definitions_path: str,
        exit_on_fail: bool
):
    if (geotiff_path is None and folder_path is None) or (geotiff_path is not None and folder_path is not None):
        logger.error("Give exactly one of --geotiff-path and --folder-path")
        sys.exit(1)

    validate.validate(geotiff_path, folder_path)

    success = True
    if not success and exit_on_fail:
        sys.exit(1)


@cli.command(
    name="generate-definitions",
    help=(
            ""
    ),
)
@click.option(
    "--folder-path",
    envvar="FOLDER_PATH",
    required=True,
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
def geotiff_generate_definitions_command(
        folder_path: str
):
    gdal.UseExceptions()

    definitions = generate_definitions(folder_path)
    json_string = json.dumps(definitions, indent=2)
    print(json_string)

if __name__ == "__main__":
    cli()