import json
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
    runner = CliRunner()
    result = runner.invoke(cli, ["generate-definitions"])
    assert result.output == "error: Give exactly one of --geotiff-path and --folder-path\n"
    assert result.exit_code == 2

def test_generate_definitions_with_file():
    runner = CliRunner()
    result = runner.invoke(cli, ["generate-definitions", "--geotiff-path", "tests/data/single_files/test_plaingeotiff.tif"])
    assert result.exit_code == 0
    expected = {
        "cog_enabled": False,
        "cog_block_size_x": None,
        "cog_block_size_y": None,
        "compression": None,
        "crs": 28992,
        "data_type": "uint8",
        "interleave": "BAND",
        "size_x": 10,
        "size_y": 20,
        "files": [
            {
                "bands": [
                    {
                        "band": 1,
                        "block": [
                            10,
                            20
                        ],
                        "type": "Byte",
                        "colorInterpretation": "Palette",
                        "metadata": {}
                    }
                ],
                "cornerCoordinates": {
                    "upperLeft": [
                        -40000.0,
                        725000.0
                    ],
                    "lowerLeft": [
                        -40000.0,
                        724500.0
                    ],
                    "lowerRight": [
                        -39750.0,
                        724500.0
                    ],
                    "upperRight": [
                        -39750.0,
                        725000.0
                    ],
                    "center": [
                        -39875.0,
                        724750.0
                    ]
                },
                "file_name": "test_plaingeotiff.tif",
                "raster_count": 1
            }
        ]
    }
    assert json.loads(result.output) == expected

def test_generate_definitions_with_folder():
    runner = CliRunner()
    result = runner.invoke(cli, ["generate-definitions", "--folder-path", "tests/data/multiple_files/plain_geotiffs"])
    assert result.exit_code == 0
    expected = {
        "cog_enabled": False,
        "cog_block_size_x": None,
        "cog_block_size_y": None,
        "compression": None,
        "crs": 28992,
        "data_type": "uint8",
        "interleave": "BAND",
        "size_x": 10,
        "size_y": 20,
        "files": [
            {
                "bands": [
                    {
                        "band": 1,
                        "block": [
                            10,
                            20
                        ],
                        "type": "Byte",
                        "colorInterpretation": "Palette",
                        "metadata": {}
                    }
                ],
                "cornerCoordinates": {
                    "upperLeft": [
                        -40000.0,
                        725000.0
                    ],
                    "lowerLeft": [
                        -40000.0,
                        724500.0
                    ],
                    "lowerRight": [
                        -39750.0,
                        724500.0
                    ],
                    "upperRight": [
                        -39750.0,
                        725000.0
                    ],
                    "center": [
                        -39875.0,
                        724750.0
                    ]
                },
                "file_name": "geotiff_01.tif",
                "raster_count": 1
            },
            {
                "bands": [
                    {
                        "band": 1,
                        "block": [
                            10,
                            20
                        ],
                        "type": "Byte",
                        "colorInterpretation": "Palette",
                        "metadata": {}
                    }
                ],
                "cornerCoordinates": {
                    "upperLeft": [
                        160000.0,
                        725000.0
                    ],
                    "lowerLeft": [
                        160000.0,
                        724500.0
                    ],
                    "lowerRight": [
                        160250.0,
                        724500.0
                    ],
                    "upperRight": [
                        160250.0,
                        725000.0
                    ],
                    "center": [
                        160125.0,
                        724750.0
                    ]
                },
                "file_name": "geotiff_02.tif",
                "raster_count": 1
            }
        ]
    }
    assert json.loads(result.output) == expected

def test_validate_all():
    runner = CliRunner()
    result = runner.invoke(cli, ["validate", "--geotiff-path", "tests/data/single_files/test_correct.tif", "--exit-on-fail"])
    assert result.exit_code == 0

def test_validate_incorrect():
    runner = CliRunner()
    result = runner.invoke(cli, ["validate", "--geotiff-path", "tests/data/single_files/test_nocog.tif", "--required-validations", "1", "--exit-on-fail"])
    assert result.exit_code == 1
