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
        - [Generate table definitions](#generate-definitions)
    - [Local development](#local-development)
        - [Docker run](#docker-run)
        - [Python console](#python-console)
        - [Code style](#code-style)
        - [Tests](#tests)
        - [Releasing](#releasing)

## TL;DR Commands

Either run through [docker](#docker) or [locally](#local).

### Docker

Validate a GeoTiff with the default set of validation rules:

```sh
geotiff_path=relative/path/to/the.tif
docker run -v "$(pwd)":/tiff --rm pdok/geotiff-validator validate --geotiff-path "/tiff/${geotiff_path}"
```


### Releasing

Release in github by creating a new release in github.
