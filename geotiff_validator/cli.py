import logging

import sys
import click
import click_log
import json

from osgeo import gdal
from geotiff_validator.generate import generate_definitions

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
    "--exit-on-fail",
    required=False,
    is_flag=True,
    help="Exit with code 1 when validation success is false.",
)
def geotiff_validator_command(
        geotiff_path: str,
        exit_on_fail: bool
):

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