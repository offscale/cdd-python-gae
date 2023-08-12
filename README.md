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

  - Automatic conversion from NDB to SQLalchemy
  - Scripts to migrate the data

## Disadvantages

  - Doesn't handle the internal NDB functions

## Alternatives

  - Hand weave ;)

## Minor other use-cases this facilitates

  - One could build this into a self-service migration system
  - The intermediary layers are on BigQuery and Google Object Storage, both of which are useful in their own right

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

For the following scripts set these `export`s:
  - `DNS_NAME`
  - `GOOGLE_BUCKET_NAME`
  - `GOOGLE_CLOUD_PROJECT`
  - `GOOGLE_CLOUD_ZONE`
  - `GOOGLE_PROJECT_NAME`
  - `INSTANCE_NAME`

### Backup from NDB to Google Cloud Storage
```sh
set -euo pipefail

entities_processed=0

echo 'Exporting datastore to bucket: '"$GOOGLE_CLOUD_BUCKET"
for entity in kind0 kind1 kind2; do
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
printf '#!/usr/bin/env bash\n\nbq mk "%s"\n' 'CollectionName' > "$DIR"'/2_bucket_to_bq.bash'
gsutil ls "$GOOGLE_CLOUD_BUCKET"'/**/all_namespaces/kind_*' | python3 -c 'import sys, posixpath, fileinput; f=fileinput.input(encoding="utf-8"); d=dict(map(lambda e: (posixpath.basename(posixpath.dirname(e)), posixpath.dirname(e)), sorted(f))); f.close(); print("\n".join(map(lambda k: "( bq mk \"CollectionName.{k}\" && bq --location=US load --source_format=DATASTORE_BACKUP \"CollectionName.{k}\" \"{v}/all_namespaces_{k}.export_metadata\" ) &".format(k=k, v=d[k]), sorted(d.keys()))),sep="");' >> "$DIR"'/2_bucket_to_bq.bash'

printf 'printf '"'"'To see if any jobs are left run:%s%s%s%s\n' \
       '\nbq ls --jobs=true --format=json | jq ' "'\"'\"'" \
       'map(select(.status.state != "DONE"))' "'\"'\"'\n'" >> "$DIR"'/2_bucket_to_bq.bash'

# Then run `bash 2_bucket_to_bq.bash`
```

### Export from Google BigQuery to Apache Parquet files in Google Cloud Storage
```sh
#!/usr/bin/env bash

set -euo pipefail

declare -r DATE_ISO8601="$(date -u --iso-8601)"
declare -r DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

while [[ $(bq ls --jobs=true --format=json | jq 'map(select(.status.state != "DONE"))') != "[]" ]]; do
   echo 'Waiting for operations to finish (sleeping for 5 minutes then trying again)'
   sleep 5m
done

echo 'Generating script that exports bq to datastore bucket in parquet format: '"'""$DIR"'/4_bq_to_parquet.bash'"'"

printf '#!/usr/bin/env bash\n\n' > "$DIR"'/4_bq_to_parquet.bash'
for entity in kind0 kind1 kind2; do
  printf -v GOOGLE_CLOUD_BUCKET_PATH '%s/%s_0/%s/*' "$GOOGLE_CLOUD_BUCKET" "$DATE_ISO8601" "$entity"
  printf "bq extract --location='%s' --destination_format='PARQUET' 'CollectionName.kind_%s' '%s' &\n" \
         "$GOOGLE_CLOUD_REGION" "$entity" "$GOOGLE_CLOUD_BUCKET_PATH" >> "$DIR"'/4_bq_to_parquet.bash'
done

printf 'printf '"'"'To see if any jobs are left run:%s%s%s%s\n' \
       '\nbq ls --jobs=true --format=json | jq ' "'\"'\"'" \
       'map(select(.status.state != "DONE"))' "'\"'\"'\n'" >> "$DIR"'/4_bq_to_parquet.bash'

# Then run `bash 4_bq_to_parquet.bash`
```

### Create node in Google Cloud

```sh
gcloud compute instances create "$INSTANCE_NAME" --project="$GOOGLE_CLOUD_PROJECT" --zone="$GOOGLE_CLOUD_ZONE" --machine-type=e2-standard-32 --network-interface=network-tier=PREMIUM,stack-type=IPV4_ONLY,subnet=default --maintenance-policy=MIGRATE --provisioning-model=STANDARD --scopes=https://www.googleapis.com/auth/devstorage.read_only,https://www.googleapis.com/auth/logging.write,https://www.googleapis.com/auth/monitoring.write,https://www.googleapis.com/auth/servicecontrol,https://www.googleapis.com/auth/service.management.readonly,https://www.googleapis.com/auth/trace.append --tags=http-server,https-server --create-disk=auto-delete=yes,boot=yes,device-name=$INSTANCE_NAME,image=projects/debian-cloud/global/images/debian-11-bullseye-v20230629,mode=rw,size=10,type=projects/$GOOGLE_PROJECT_NAME/zones/$GOOGLE_ZONE_NAME/diskTypes/pd-balanced --create-disk=device-name=2_5_tb,mode=rw,name=disk-1,size=2500,type=projects/$GOOGLE_PROJECT_NAME/zones/$GOOGLE_CLOUD_ZONE/diskTypes/pd-balanced --no-shielded-secure-boot --shielded-vtpm --shielded-integrity-monitoring --labels=goog-ec-src=vm_add-gcloud --reservation-affinity=an
```

### Prepare instance

```sh
gcloud compute ssh "$INSTANCE_NAME" --command='sudo mkdir /data && sudo mkfs -t ext4 /dev/sdb && sudo mount "$_" "/data" && sudo chown -R $USER:$GROUP "$_" && sudo apt install -y python3-dev python3-venv libpq-dev moreutils git pwgen rsync gcc && python3 -m venv venv && . venv/bin/activate && python -m pip install -r https://raw.githubusercontent.com/offscale/cdd-python/master/requirements.txt && python -m pip install https://api.github.com/repos/offscale/cdd-python/zipball#egg=python-cdd && python -m pip install -r https://raw.githubusercontent.com/offscale/cdd-python-gae/master/requirements.txt && python -m pip install https://api.github.com/repos/offscale/cdd-python-gae/zipball#egg=python-cdd-gae && python -m pip install sqlalchemy==1.4.*'
```

### Download Parquet files

```sh
# PS: This last bucket location can be found above as the `export`: `GOOGLE_CLOUD_BUCKET_PATH`
$ gcloud compute ssh $INSTANCE_NAME --command="gcloud storage cp -R 'gs://""$GOOGLE_BUCKET_NAME"'/2023-07-24_0/*' '/data'"
```

### Install and serve PostgreSQL

```sh
gcloud compute ssh $INSTANCE_NAME --command='f="postgres-version-manager-go_Linux_x86_64.tar.gz"; curl -OL https://github.com/offscale/postgres-version-manager-go/releases/0.0.21/"$f" && tar xf "$f" && ./pvm-go --data-path /data/pg-data --username "$(pwgen -n1)" --password "$(pwgen -n1)" --database database_name_db --locale C.UTF-8 start && ./pvm-go stop && sudo adduser -gecos "" --disabled-password --quiet postgres && sudo chown -R $_:$_ /data/pg-data && sudo ./pvm-go -c ~/postgres-version-manager/pvm-config.json install-service systemd && sudo systemctl daemon-reload && sudo systemctl start postgresql'

# You might want to edit your "$($HOME/pvm-go get-path data)"'/pg_hba.conf' to enable connection to your db
# Or you can do:

$ export $($HOME/pvm-go env | xargs -L 1)

$ printf 'host\t'"$POSTGRES_DATABASE"'\t'"$POSTGRES_USERNAME"'\t0.0.0.0/0\tscram-sha-256\n' >> "$($HOME/pvm-go get-path data)"'/pg_hba.conf'

# You might also change your "$($HOME/pvm-go get-path data)"'/postgresql.conf' to enable connection to the correct address (or insecurely: listen_addresses = '*')

$ printf 'listen_addresses = '"'"'*'"'"'\n' >> "$($HOME/pvm-go get-path data)"'/postgresql.conf'

# Database connection string, take the output from that last command and replace "localhost" with:
$ declare -r IP_ADDR="$(gcloud compute instances describe "$INSTANCE_NAME" --flatten networkInterfaces[].accessConfigs[] --format 'csv[no-heading](networkInterfaces.accessConfigs.natIP)')"

# Go one step further and set a DNS name so it's easier, and so we can turn off/move the instance without worrying about a permanent IP, and for clustering
$ gcloud beta dns record-sets create "$DNS_NAME" --rrdatas="$IP_ADDR" --type=A --zone="$GOOGLE_ZONE"
```

### Create the tables

```sh
# `gcloud compute scp` over '5_gen_parquet_to_sqlalchemy.bash' then run:
$ gcloud compute ssh "$INSTANCE_NAME" --command='bash 5_gen_parquet_to_sqlalchemy.bash && export RDBMS_URI="$($HOME/pvm-go uri)" && ~/venv/bin/python -m parquet_to_postgres.create_tables'
````

### Import data from Parquet to PostgreSQL

```sh
$ fd -tf . '/data' -E 'exclude_tbl' -x bash -c 'python -m cdd_gae parquet2table --table-name "$(basename ${0%/*})" -i "$0"' {}
```

### Note connection string

```sh
$ gcloud compute ssh "$INSTANCE_NAME" --command='./pvm-go uri'
```

(replace `localhost` with the `$IP_ADDR` value or `$DNS_NAME` if you set that)

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
