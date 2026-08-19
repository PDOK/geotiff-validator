from click.testing import CliRunner

from geotiff_validator.cli import cli
from geotiff_validator.generate import generate_definitions

import json
import pytest

def test_generate_definitions_with_file():
    result = None
    try:
        result = generate_definitions(file="tests/data/single_files/test_plaingeotiff.tif", folder=None)
    except Exception as e:
        print(e)
        assert False
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
    assert result == expected


def test_generate_definitions_with_folder():
    result = None
    try:
        result = generate_definitions(file=None, folder="tests/data/multiple_files/plain_geotiffs")
    except Exception as e:
        print(e)
        assert False
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
    assert result == expected

def test_generate_definitions_with_empty_folder():
    result = None
    try:
        with pytest.raises(SystemExit):
            result = generate_definitions(file=None, folder="tests/data/multiple_files/empty")
        assert False
    except Exception as e:
        pass


def test_generate_definitions_with_mixed_attributes():
    """Shared attributes like pixel dimensions and CRS must not differ between files"""
    result = None
    try:
        with pytest.raises(SystemExit):
            result = generate_definitions(file=None, folder="tests/data/multiple_files/different_sizes")
        assert False
    except Exception as e:
        pass
