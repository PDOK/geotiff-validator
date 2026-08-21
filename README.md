# PDOK geotiff-validator

[![Tests](https://github.com/pdok/geotiff-validator/actions/workflows/pytest.yml/badge.svg)](https://github.com/pdok/geotiff-validator/actions/workflows/pytest.yml)[![PyPI version](https://badge.fury.io/py/pdok-geotiff-validator.svg)](https://pypi.org/project/pdok-geotiff-validator/)

The PDOK geotiff validator is used by [PDOK](https://www.pdok.nl/). PDOK is part of the Dutch government. This geotiff validator is used to validate a [set of requirements](#what-does-it-do) to make sure geotiffs adhere to our standardized ETL pipeline. It is possible to use this for your own purposes. The validations will not change (except for bugfixes); **new validations are always added to the list**.


## Table of Contents

- [geotiff-validator](#pdok-geotiff-validator)
    - [Table of Contents](#table-of-contents)
    - [What does it do](#what-does-it-do)
    - [Installation](#installation)
        - [Docker](#docker-installation)
    - [Usage](#usage)
        - [Schema Validation](#schema-validation)
        - [Show validations](#show-validations)
        - [Generate geotiff definitions](#generate-schema-definitions)
    - [Local development](#local-development)
        - [Docker run](#docker-run)
        - [Python console](#python-console)
        - [Code style](#code-style)
        - [Tests](#tests)
        - [Releasing](#releasing)

## TL;DR Commands

Either run through [docker](#docker) or [locally](#local).

### Docker

Validate a single GeoTiff file with the default set of validation rules:

```sh
geotiff_path=relative/path/to/the.tif
docker run -v "$(pwd)":/tiff --rm pdok/geotiff-validator validate --geotiff-path "/tiff/${geotiff_path}"
```

Validate a GeoTiff folder with the default set of validation rules:

```sh
geotiff_path=relative/path/to/the.tif
docker run -v "$(pwd)":/tiff --rm pdok/geotiff-validator validate --folder-path "/tiff/"
```

Generate definitions for a folder containing GeoTiffs:

```sh
geotiff_path=relative/path/to/the.tif
docker run -v "$(pwd)":/tiff --rm pdok/geotiff-validator generate-definitions --folder-path "/tiff/"
```

## What does it do

The GeoTiff validator can validate Geotiff files (.tif files with GeoTiff extension) to see if they conform to a set of standards.
The current checks are (see also the 'show-validations' command)

| Validation code | Description                                        |
|:---------------:|----------------------------------------------------|
|        0        | The file must exist and be a valid GeoTiff         |
|        1        | The GeoTiff must be a Cloud Optimized GeoTiff(COG) |
|        2        | The GeoTiff must be compressed with LZW            |
|        3        | The GeoTiff must not have views                    |
|        4        | The GeoTiff must match the generated schema        |


**Note to PDOK developers:** make sure to update the Kangaroo webinterface when adding a new validation.

## Installation

This package requires:

- [GDAL](https://gdal.org/) version == 3.11.5.
- And python >= 3.10 to run.

### Docker Installation

Pull the latest version of the Docker image (only once needed, or after an update)

```bash
docker pull pdok/geotiff-validator:latest
```

Or build the Docker image from source:

```bash
docker build -t pdok/geotiff-validator .
```

The command is directly called so subcommands can be run in the container directly:

```bash
docker run -v ${PWD}:/tiff --rm pdok/geotiff-validator validate --definitions-path /path/to/schema_definitions.json --geotiff-path /tiff/tests/data/single_files/test_correct.tif
```

## Usage

### Validate

```text
Geotiff validator validating one or more tiff files.
```

### Schema validation

To validate schemas (validation #4) you have to generate definitions first.

```bash
docker run -v ${PWD}:/gpkg --rm pdok/geotiff-validator geotiff-validator generate-definitions --folder-path /mytifffolder
```

### Show validations

Show all the possible validations that are executed in the validate command.

```text
Usage: geotiff-validator show-validations [OPTIONS]

  Show all the possible validations that can be executed in the validate
  command.

Options:
  --no-legacy          Output without Legacy checks
  --yaml               Output yaml
  -v, --verbosity LVL  Either CRITICAL, ERROR, WARNING, INFO or DEBUG
  --help               Show this message and exit.
```

### Generate schema definitions

```text
Usage: geotiff-validator generate-definitions [OPTIONS]

  Generate schema definition for one or multiple tifs . Use the
  generated definition JSON or YAML in the validation step by providing the
  table definitions with the --definitions-path parameter.

Options:
  --folder-path DIRECTORY  Path pointing to the folder containing the geotiff
                           files  [env var: FOLDER_PATH]
  --geotiff-path FILE      Path pointing to the geotiff .tif file  [env var:
                           GEOTIFF_PATH]
  --help                   Show this message and exit.
```

### Tests

Run the tests regularly.

```bash
pytest .
```

### Releasing

Release in github by creating a new release in github.
