import logging

import click
import click_log

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
def geotiff_validator_command():
    print("Hello world")

if __name__ == "__main__":
    cli()