cdd-python-gae
==============
![Python version range](https://img.shields.io/badge/python-3.6%20|%203.7%20|%203.8%20|%203.9%20|%203.10%20|%203.11-blue.svg)
![Python implementation](https://img.shields.io/badge/implementation-cpython-blue.svg)
[![License](https://img.shields.io/badge/license-Apache--2.0%20OR%20MIT-blue.svg)](https://opensource.org/licenses/Apache-2.0)
[![Linting, testing, coverage, and release](https://github.com/offscale/cdd-python-gae/workflows/Linting,%20testing,%20coverage,%20and%20release/badge.svg)](https://github.com/offscale/cdd-python-gae/actions)
![Tested OSs, others may work](https://img.shields.io/badge/Tested%20on-Linux%20|%20macOS%20|%20Windows-green)
![Documentation coverage](https://raw.githubusercontent.com/offscale/cdd-python-gae/master/.github/doccoverage.svg)
[![codecov](https://codecov.io/gh/offscale/cdd-python-gae/branch/master/graph/badge.svg)](https://codecov.io/gh/offscale/cdd-python-gae)
[![black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Imports: isort](https://img.shields.io/badge/%20imports-isort-%231674b1?style=flat&labelColor=ef8336)](https://pycqa.github.io/isort)
[![PyPi: release](https://img.shields.io/pypi/v/python-cdd-gae.svg?maxAge=3600)](https://pypi.org/project/python-cdd-gae)

Migration tooling from Google App Engine (webapp2, ndb) to python-cdd supported (FastAPI, SQLalchemy).

Public SDK works with filenames, source code, and even in memory constructs (e.g., as imported into your REPL).
CLI available also.

## Install package

### PyPi

    pip install python-cdd-gae

### Master

    pip install -r https://raw.githubusercontent.com/offscale/cdd-python-gae/master/requirements.txt
    pip install https://api.github.com/repos/offscale/cdd-python-gae/zipball#egg=cdd

## Goal

Migrate from Google App Engine to cloud-independent runtime (e.g., vanilla CPython 3.11 with SQLite). 

## Relation to other projects

This was created independent of `cdd-python` project for two reasons:

  0. Unidirectional;
  1. Relevant to fewer people.

## SDK

### Approach

Traverse the AST for ndb and webapp2.

## Advantages

  - 

## Disadvantages

  - 

## Alternatives

  - 

## Minor other use-cases this facilitates

  - 

## CLI for this project

    $ python -m cdd_gae --help
    usage: python -m cdd_gae [-h] [--version]
                             {ndb2sqlalchemy,ndb2sqlalchemy_migrator,webapp2_to_fastapi}
                             ...
    
    Migration tooling from Google App Engine (webapp2, ndb) to python-cdd
    supported (FastAPI, SQLalchemy).
    
    positional arguments:
      {ndb2sqlalchemy,ndb2sqlalchemy_migrator,webapp2_to_fastapi}
        ndb2sqlalchemy      Parse NDB emit SQLalchemy
        ndb2sqlalchemy_migrator
                            Create migration scripts from NDB to SQLalchemy
        webapp2_to_fastapi  Parse WebApp2 emit FastAPI
    
    optional arguments:
      -h, --help            show this help message and exit
      --version             show program's version number and exit

### `ndb2sqlalchemy` (`webapp2_to_fastapi` takes same args)

    $ python -m cdd_gae ndb2sqlalchemy --help
    
    usage: python -m cdd_gae ndb2sqlalchemy [-h] -i INPUT_FILE -o OUTPUT_FILE
                                            [--dry-run]
    
    options:
      -h, --help            show this help message and exit
      -i INPUT_FILE, --input-file INPUT_FILE
                            Python file to parse NDB `class`es out of
      -o OUTPUT_FILE, --output-file OUTPUT_FILE
                            Empty file to generate SQLalchemy classes to
      --dry-run             Show what would be created; don't actually write to
                            the filesystem.

### `webapp2_to_fastapi` (`ndb2sqlalchemy` takes same args)

    $ python -m cdd_gae webapp2_to_fastapi --help
    
    usage: python -m cdd_gae webapp2_to_fastapi [-h] -i INPUT_FILE -o OUTPUT_FILE
                                                [--dry-run]
    
    options:
      -h, --help            show this help message and exit
      -i INPUT_FILE, --input-file INPUT_FILE
                            Python file to parse WebApp2 `class`es out of
      -o OUTPUT_FILE, --output-file OUTPUT_FILE
                            Empty file to generate FastAPI functions to
      --dry-run             Show what would be created; don't actually write to
                            the filesystem.

### `python -m cdd_gae ndb2sqlalchemy_migrator --help`

    $ ndb2sqlalchemy_migrator
    usage: python -m cdd_gae ndb2sqlalchemy_migrator [-h] --ndb-file NDB_FILE
                                                     --sqlalchemy-file
                                                     SQLALCHEMY_FILE
                                                     --ndb-mod-to-import
                                                     NDB_MOD_TO_IMPORT
                                                     --sqlalchemy-mod-to-import
                                                     SQLALCHEMY_MOD_TO_IMPORT -o
                                                     OUTPUT_FOLDER [--dry-run]
    
    optional arguments:
      -h, --help            show this help message and exit
      --ndb-file NDB_FILE   Python file containing the NDB `class`es
      --sqlalchemy-file SQLALCHEMY_FILE
                            Python file containing the NDB `class`es
      --ndb-mod-to-import NDB_MOD_TO_IMPORT
                            NDB module name that the entity will be imported from
      --sqlalchemy-mod-to-import SQLALCHEMY_MOD_TO_IMPORT
                            SQLalchemy module name that the entity will be
                            imported from
      -o OUTPUT_FOLDER, --output-folder OUTPUT_FOLDER
                            Empty folder to generate scripts that migrate from one
                            NDB class to one SQLalchemy class
      --dry-run             Show what would be created; don't actually write to
                            the filesystem.

---

## License

Licensed under either of

- Apache License, Version 2.0 ([LICENSE-APACHE](LICENSE-APACHE) or <https://www.apache.org/licenses/LICENSE-2.0>)
- MIT license ([LICENSE-MIT](LICENSE-MIT) or <https://opensource.org/licenses/MIT>)

at your option.

### Contribution

Unless you explicitly state otherwise, any contribution intentionally submitted
for inclusion in the work by you, as defined in the Apache-2.0 license, shall be
dual licensed as above, without any additional terms or conditions.
