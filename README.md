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

Note: Parquet files are supported as it takes too long to run NDB queries to batch acquire / batch insert into SQL.

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
    usage: python -m cdd_gae [-h] [--version] {gen,ndb2sqlalchemy_migrator} ...
    
    Migration tooling from Google App Engine (webapp2, ndb) to python-cdd
    supported (FastAPI, SQLalchemy).
    
    positional arguments:
      {gen,ndb2sqlalchemy_migrator}
        gen                 Go from cdd_gae supported parse type to cdd supported
                            emit type
        ndb2sqlalchemy_migrator
                            Create migration scripts from NDB to SQLalchemy
    
    options:
      -h, --help            show this help message and exit
      --version             show program's version number and exit

### `python -m cdd_gae gen`

    $ python -m cdd_gae gen --help
    usage: python -m cdd_gae gen [-h] [--parse {ndb,parquet,webapp2}] --emit
                                 {argparse,class,function,json_schema,pydantic,sqlalchemy,sqlalchemy_table}
                                 -i INPUT_FILE -o OUTPUT_FILE [--name NAME]
                                 [--dry-run]
    
    options:
      -h, --help            show this help message and exit
      --parse {ndb,parquet,webapp2}
                            What type the input is.
      --emit {argparse,class,function,json_schema,pydantic,sqlalchemy,sqlalchemy_table}
                            What type to generate.
      -i INPUT_FILE, --input-file INPUT_FILE
                            Python file to parse NDB `class`es out of
      -o OUTPUT_FILE, --output-file OUTPUT_FILE
                            Empty file to generate SQLalchemy classes to
      --name NAME           Name of function/class to emit, defaults to inferring
                            from filename
      --dry-run             Show what would be created; don't actually write to
                            the filesystem.

### `python -m cdd_gae ndb2sqlalchemy_migrator`

    $ python -m cdd_gae ndb2sqlalchemy_migrator --help
    usage: python -m cdd_gae ndb2sqlalchemy_migrator [-h] --ndb-file NDB_FILE
                                                     --sqlalchemy-file
                                                     SQLALCHEMY_FILE
                                                     --ndb-mod-to-import
                                                     NDB_MOD_TO_IMPORT
                                                     --sqlalchemy-mod-to-import
                                                     SQLALCHEMY_MOD_TO_IMPORT -o
                                                     OUTPUT_FOLDER [--dry-run]
    
    options:
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

## Data migration

The most efficient way seems to be:

  0. Backup from NDB to Google Cloud Storage
  1. Import from Google Cloud Storage to Google BigQuery
  2. Export from Google BigQuery to Apache Parquet files in Google Cloud Storage
  3. Download and parse the Parquet files, then insert into SQL

(for the following scripts set `GOOGLE_PROJECT_ID`, `GOOGLE_BUCKET_NAME`, `NAMESPACE`, `GOOGLE_LOCATION`)

### Backup from NDB to Google Cloud Storage
```sh
for entity in kind0 kind1; do
  gcloud datastore export 'gs://'"$GOOGLE_BUCKET_NAME" --project "$GOOGLE_PROJECT_ID" --kinds "$entity" --async &
done
```

### Import from Google Cloud Storage to Google BigQuery
```sh
printf 'bq mk "%s"\n' "$NAMESPACE" > migrate.bash
gsutil ls 'gs://'"$GOOGLE_BUCKET_NAME"'/**/all_namespaces/kind_*' | python3 -c 'import sys, posixpath, fileinput; f=fileinput.input(encoding="utf-8"); d=dict(map(lambda e: (posixpath.basename(posixpath.dirname(e)), posixpath.dirname(e)), sorted(f))); f.close(); print("\n".join(map(lambda k: "( bq mk \"'"$NAMESPACE"'.{k}\" && bq --location='"$GOOGLE_LOCATION"' load --source_format=DATASTORE_BACKUP \"'"$NAMESPACE"'.{k}\" \"{v}/all_namespaces_{k}.export_metadata\" ) &".format(k=k, v=d[k]), sorted(d.keys()))),sep="");' >> migrate.bash
# Then run `bash migrate.bash`
```

### Export from Google BigQuery to Apache Parquet files in Google Cloud Storage
```sh
for entity in kind0 kind1; do
  bq extract --location="$GOOGLE_LOCATION" --destination_format='PARQUET' "$NAMESPACE"'.kind_'"$entity" 'gs://'"$GOOGLE_BUCKET_NAME"'/'"$entity"'/*' &
done
```

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
