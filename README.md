# USGNIS_ETL

## Introduction

This project aims to simplify the use of the data files provided by the U.S.
Geological Survey at <http://geonames.usgs.gov/domestic/download_data.htm> by
making it easy to upload them to a PostgreSQL database. These files are mainly
provided in simple comma- or pipe-separated-value formats which are supported
by many existing tools. However this project also takes care of creating an
appropriate schema in the database, decompressing the `.zip` files and
automatically choosing the correct destination table.

A geographical database with worldwide coverage is available from
<http://www.geonames.org>, and tools exist to work with it. However it does
not contain all of the fields included in the USGS data. If you are sure you
are only interested in the US, and you either need some of these fields or you
need to be able to prove the official provenance of the data, this project may
still be useful.

This is an independent project and it is not associated with or endorsed by
the U.S. Geological Survey. It is available under the GPL v2 or later, as
described in the file `COPYING`.

> This program is distributed in the hope that it will be useful, but
> WITHOUT WITHOUT ANY WARRANTY; without even the implied warranty of
> MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General
> Public License for more details.

## Provided programs and package

### `usgnis_schema.py`

This program can create or recreate a schema `usgnis` in a database which can
then be used by `usgnis_extract.py`. It can also truncate the tables to clear
out all existing data. The optional `TABLE` parameter indicates which table
to operate on. By default, actions are applied to all tables.

    $ python3 usgnis_schema.py --help
    usage: usgnis_schema.py [-h] [--drop-existing] [--dry-run [LOG FILE]]
                            [--database DATABASE] [--user USER]
                            [--password PASSWORD] [--host HOST] [--port PORT]
                            ACTION [TABLE]

    Create or modify a PostgreSQL database schema for USGNIS data

    positional arguments:
      ACTION                Whether to "create", "truncate" or "list" tables
      TABLE                 The database table to act on, or ALL

    optional arguments:
      -h, --help            show this help message and exit

    processing options:
      --drop-existing       Drop existing tables (and any data) before recreating

    database arguments:
      --dry-run [LOG FILE]  Dump commands to a file rather than executing them on
                            the database
      --database DATABASE   PostgreSQL database to use (default usgnis)
      --user USER           PostgreSQL user for upload
      --password PASSWORD   PostgreSQL user password
      --host HOST           PostgreSQL host (if using TCP/IP)
      --port PORT           PostgreSQL port (if required)

### `usgnis_extract.py`

This program uploads data from a file to the existing `usgnis` schema in the
database. The optional `TYPE` parameter can be used to over-ride the automatic
recognition of the destination table from the file name.

    $ python3 usgnis_extract.py --help
    usage: usgnis_extract.py [-h] [--dry-run [LOG FILE]] [--database DATABASE]
                             [--user USER] [--password PASSWORD] [--host HOST]
                             [--port PORT] [--no-sync-commit]
                             [--work-mem WORK_MEM]
                             [--maintenance-work-mem MAINTENANCE_WORK_MEM]
                             FILE [TYPE]

    Upload USGNIS data to a PostgreSQL database

    positional arguments:
      FILE                  The file to extract and upload data from
      TYPE                  Override recognition of the type of file

    optional arguments:
      -h, --help            show this help message and exit

    database arguments:
      --dry-run [LOG FILE]  Dump commands to a file rather than executing them on
                            the database
      --database DATABASE   PostgreSQL database to use (default usgnis)
      --user USER           PostgreSQL user for upload
      --password PASSWORD   PostgreSQL user password
      --host HOST           PostgreSQL host (if using TCP/IP)
      --port PORT           PostgreSQL port (if required)
      --no-sync-commit      Disable synchronous commits
      --work-mem WORK_MEM   Size of working memory in MB
      --maintenance-work-mem MAINTENANCE_WORK_MEM
                            Size of maintenance working memory in MB

The `--no-sync-commit` option temporarily disables synchronous
commits and so can give a speed boost. The `--work-mem` and
`--maintenance-work-mem` options temporarily increase the amount of working
memory that the PostgreSQL server uses.

### `usgnis`

This is an internal package that defines classes that are used by the above
programs.