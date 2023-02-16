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

### `python -m cdd_gae gen parquet2table`

    $ python -m cdd_gae parquet2table --help
    usage: python -m cdd_gae parquet2table [-h] -i FILENAME
                                           [--database-uri DATABASE_URI]
                                           [--table-name TABLE_NAME] [--dry-run]
    
    options:
      -h, --help            show this help message and exit
      -i FILENAME, --input-file FILENAME
                            Parquet file
      --database-uri DATABASE_URI
                            Database connection string. Defaults to `RDBMS_URI` in
                            your env vars.
      --table-name TABLE_NAME
                            Table name to use, else use penultimate underscore
                            surrounding word form filename basename
      --dry-run             Show what would be created; don't actually write to
                            the filesystem.

---

## Data migration

The most efficient way seems to be:

  0. Backup from NDB to Google Cloud Storage
  1. Import from Google Cloud Storage to Google BigQuery
  2. Export from Google BigQuery to Apache Parquet files in Google Cloud Storage
  3. Download and parse the Parquet files, then insert into SQL

(for the following scripts set `GOOGLE_CLOUD_PROJECT`, `GOOGLE_CLOUD_BUCKET`, `NAMESPACE`, `GOOGLE_LOCATION`)

### Backup from NDB to Google Cloud Storage
```sh
set -euo pipefail

entities_processed=0

echo 'Exporting datastore to bucket: '"$GOOGLE_CLOUD_BUCKET"
for entity in kind0 kind1; do
  gcloud datastore export "$GOOGLE_CLOUD_BUCKET" --project "$GOOGLE_CLOUD_PROJECT" --kinds "$entity" --async
  entities_processed=$((entities_processed + 1))
  if [ "$entities_processed" -eq 18 ]; then
    # Overcome quota issues
    echo 'Sleeping for 2 minutes to overcome quota issues'
    sleep 2m
    entities_processed=0
  fi
done

printf 'Tip: To see operations that are still being processed, run:\n%s\n' \
       'gcloud datastore operations list --format=json | jq '"'"'map(select(.metadata.common.state == "PROCESSING"))'"'"
```

### Import from Google Cloud Storage to Google BigQuery
```sh
#!/usr/bin/env bash

set -euo pipefail

declare -r DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

while [[ $(gcloud datastore operations list --format=json | jq -re 'map(select(.metadata.common.state == "PROCESSING"))') != "[]" ]]; do
   echo 'Waiting for operations to finish (sleeping for 5 minutes then trying again)'
   sleep 5m
done

echo 'Generating script that imports datastore bucket to bq to: '"'""$DIR"'/2_bucket_to_bq.bash'"'"
printf '#!/usr/bin/env bash\n\nbq mk "%s"\n' 'DatasetNameHere' > "$DIR"'/2_bucket_to_bq.bash'
gsutil ls "$GOOGLE_CLOUD_BUCKET"'/**/all_namespaces/kind_*' | python3 -c 'import sys, posixpath, fileinput; f=fileinput.input(encoding="utf-8"); d=dict(map(lambda e: (posixpath.basename(posixpath.dirname(e)), posixpath.dirname(e)), sorted(f))); f.close(); print("\n".join(map(lambda k: "( bq mk \"Playable.{k}\" && bq --location=US load --source_format=DATASTORE_BACKUP \"DatasetNameHere.{k}\" \"{v}/all_namespaces_{k}.export_metadata\" ) &".format(k=k, v=d[k]), sorted(d.keys()))),sep="");' >> "$DIR"'/2_bucket_to_bq.bash'

printf "To see if any jobs are left run:\nbq ls --jobs=true --format=json | jq 'map(select(.status.state != "'"DONE"))'"'"'\n' >> "$DIR"'/2_bucket_to_bq.bash'

# Then run `bash 2_bucket_to_bq.bash`
```

### Export from Google BigQuery to Apache Parquet files in Google Cloud Storage
```sh
#!/usr/bin/env bash

set -euo pipefail

declare -r GOOGLE_CLOUD_REGION="${GOOGLE_CLOUD_REGION:-US}"
declare -r DATE_ISO8601="$(date -u --iso-8601)"
declare -r DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

while [[ $(bq ls --jobs=true --format=json | jq 'map(select(.status.state != "DONE"))') != "[]" ]]; do
   echo 'Waiting for operations to finish (sleeping for 5 minutes then trying again)'
   sleep 5m
done

echo 'Generating script that exports bq to datastore bucket in parquet format: '"'""$DIR"'/4_bq_to_parquet.bash'"'"

printf '#!/usr/bin/env bash\n\n' > "$DIR"'/4_bq_to_parquet.bash'
for entity in kind0 kind1; do
  printf -v GOOGLE_CLOUD_BUCKET_PATH '%s/%s_0/%s/*' "$GOOGLE_CLOUD_BUCKET" "$DATE_ISO8601" "$entity"
  printf "bq extract --location='%s' --destination_format='PARQUET' 'DatasetNameHere.kind_%s' '%s' &\n" \
         "$GOOGLE_CLOUD_REGION" "$entity" "$GOOGLE_CLOUD_BUCKET_PATH" >> "$DIR"'/4_bq_to_parquet.bash'
done

printf 'printf '"'"'To see if any jobs are left run:%s'"'"'%s'"'"'\n' \
       '\nbq ls --jobs=true --format=json | jq ' \
       'map(select(.status.state != "DONE"))' >> "$DIR"'/4_bq_to_parquet.bash'

# Then run `bash 4_bq_to_parquet.bash`
```

###  Download and parse the Parquet files, then insert into SQL
Download from Google Cloud Bucket to `/data`:
```sh
gcloud storage cp -R 'gs://'"$GOOGLE_BUCKET_NAME"'/folder/*' '/data'
```

Use this script to create SQLalchemy files from Parquet files:
```bash
#!/usr/bin/env bash

set -euo pipefail

if ! command -v sponge &>/dev/null; then
  >&2 printf 'sponge not found, you need to:\nsudo apt install moreutils\n'
  exit 2
fi

declare -r module_dir='parquet_to_postgres'
mkdir -p "$module_dir"
declare -r main_py="$module_dir"'/__main__.py'
printf '%s\n' \
	  'from os import environ' \
	  'from sqlalchemy import create_engine' '' '' \
	  'if __name__ == "__main__":' \
	  '     ' \
	  '    print("Creating tables")' \
	  '    metadata.create_all(engine)' > "$main_py"
printf '%s\n' \
	  'from sqlalchemy import MetaData' '' \
	  'metadata = MetaData()' \
	  '__all__ = ["metadata"]' > "$module_dir"'/__init__.py'

declare -a extra_imports=()

while read -r parquet_file; do
  IFS='_'; read -r _ _ table_name _ _ _ <<< "${parquet_file//+(*\/|.*)}"
  if [ -z "$table_name" ]; then
	parent_dir="${parquet_file%/*}"
	table_name="${parent_dir##*/}"
  fi
  py_file="$module_dir"'/'"$table_name"'.py'
  python -m cdd_gae gen --parse 'parquet' --emit 'sqlalchemy_table' -i "$parquet_file" -o "$py_file" --name "$table_name"
  echo -e 'from . import metadata' | cat - "$py_file" | sponge "$py_file"
  printf -v table_import 'from %s.%s import config_tbl as %s' "$module_dir" "$table_name" "$table_name"
  extra_imports+=("$table_import")
done< <(find /data -type f -name '000000000000')

extra_imports+=('from . import metadata')

( IFS=$'\n'; echo -e "${extra_imports[*]}" ) | cat - "$main_py" | sponge "$main_py"

# create_tables script
create_tables_py="$module_dir"'/create_tables.py'
printf '%s\n' \
	  'from os import environ' \
	  'from sqlalchemy import create_engine' '' '' \
	  'if __name__ == "__main__":' \
	  '    engine = create_engine(environ["RDBMS_URI"])' \
	  '    print("Creating tables")' \
	  '    metadata.create_all(engine)' > "$create_tables_py"
( IFS=$'\n'; echo -e "${extra_imports[*]}" ) | cat - "$create_tables_py" | sponge "$create_tables_py"

printf 'To create tables, run:\npython -m %s.create_tables\n' "$module_dir"
```

Then run `python -m "$module_dir".create_tables` to execute the `CREATE TABLE`s.

Finally, to batch insert into your tables concurrently; replace `RDBMS_URI` with your database connection string:
```sh
export RDBMS_URI='postgresql://username:password@host/database'
for parquet_file in 2023-01-18_0_kind0_000000000000 2023-01-18_0_kind1_000000000000; do
  python -m cdd_gae parquet2table -i "$parquet_file" &
done
# Or with the concurrent `fd`
# fd -tf . '/data' -E 'exclude_tbl' -x python -m cdd_gae parquet2table -i
# Or with explicit table_name from parent folder's basename:
# fd -tf . '/data' -E 'exclude_tbl' -x bash -c 'python -m cdd_gae parquet2table --table-name "$(basename ${0%/*})" -i "$0"' {}
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
