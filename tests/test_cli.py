
import pytest
from click.testing import CliRunner

from geotiff_validator.cli import cli

def test_show_validations():
    runner = CliRunner()
    result = runner.invoke(cli, ["show-validations"])
    assert result.exit_code == 0
    assert (
            '1": "The GeoTiff must be a Cloud Optimized GeoTiff(COG)"'
            in result.output
    )

def test_generate_definitions_no_file_or_folder():
    pass

def test_generate_definitions_with_file():
    pass

def test_generate_definitions_with_folder():
    pass