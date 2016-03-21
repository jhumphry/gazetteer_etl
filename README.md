# Gazetteer_ETL

## Introduction

This project aims to simplify the use of gazetteer data files  by
making it easy to upload them to a PostgreSQL database. These files are mainly
provided in simple comma- or pipe-separated-value formats which are supported
by many existing tools. However this project also takes care of creating an
appropriate schema in the database, decompressing the `.zip` files and
automatically choosing the correct destination table.

A geographical database with worldwide coverage is available from
<http://www.geonames.org>, and tools exist to work with it. However it does
not contain all of the fields included in the data available from the
underlying sources. Currently, files from the following sources are supported
to some degree:

- usgnis: U.S. Board on Geographic Names - Domestic and Antarctic Names
<http://geonames.usgs.gov/domestic/download_data.htm>

- uscensus2010: U.S. Census Bureau 2010 Census Gazetteer Files
<http://www.census.gov/geo/maps-data/data/gazetteer2010.html>

This is an independent project and it is not associated with or endorsed by
the producers of the data sources listed above. It is available under the GPL
v2 or later, as described in the file `COPYING`.

> This program is distributed in the hope that it will be useful, but
> WITHOUT WITHOUT ANY WARRANTY; without even the implied warranty of
> MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General
> Public License for more details.

## Provided programs and package

### `gazetteer_schema.py`

This program can create or recreate the schemas in a database which can then
be used by `gazetteer_extract.py`. It can also truncate the tables to clear
out all existing data. The optional `TABLE` parameter can be used to act only
on the tables in one schema, or on one particular table, rather than acting on
all the tables it knows about.

    $ python3 gazetteer_schema.py --help
    usage: gazetteer_schema.py [-h] [--drop-existing] [--dry-run [LOG FILE]]
                               [--database DATABASE] [--user USER]
                               [--password PASSWORD] [--host HOST] [--port PORT]
                               ACTION [TABLE]

    Create or modify a PostgreSQL database schema for gazetteer data

    positional arguments:
      ACTION                Whether to "create", "truncate" or "list" tables
      TABLE                 The database schema or table to act on, or ALL

    optional arguments:
      -h, --help            show this help message and exit

    processing options:
      --drop-existing       Drop existing tables (and any data) before recreating

    database arguments:
      --dry-run [LOG FILE]  Dump commands to a file rather than executing them on
                            the database
      --database DATABASE   PostgreSQL database to use (default gazetteer)
      --user USER           PostgreSQL user for upload
      --password PASSWORD   PostgreSQL user password
      --host HOST           PostgreSQL host (if using TCP/IP)
      --port PORT           PostgreSQL port (if required)


### `gazetteer_extract.py`

This program uploads data from a file to the existing schema in the database.
The optional `TYPE` parameter can be used to over-ride the automatic
recognition of the destination table from the file name.

    $ python3 gazetteer_extract.py --help
    usage: gazetteer_extract.py [-h] [--dry-run [LOG FILE]] [--database DATABASE]
                                [--user USER] [--password PASSWORD] [--host HOST]
                                [--port PORT] [--no-sync-commit]
                                [--work-mem WORK_MEM]
                                [--maintenance-work-mem MAINTENANCE_WORK_MEM]
                                FILE [TYPE]

    Upload gazetteer data to a PostgreSQL database

    positional arguments:
      FILE                  The file to extract and upload data from
      TYPE                  Override recognition of the type of file

    optional arguments:
      -h, --help            show this help message and exit

    database arguments:
      --dry-run [LOG FILE]  Dump commands to a file rather than executing them on
                            the database
      --database DATABASE   PostgreSQL database to use (default gazetteer)
      --user USER           PostgreSQL user for upload
      --password PASSWORD   PostgreSQL user password
      --host HOST           PostgreSQL host (if using TCP/IP)
      --port PORT           PostgreSQL port (if required)
      --no-sync-commit      Disable synchronous commits
      --work-mem WORK_MEM   Size of working memory in MB
      --maintenance-work-mem MAINTENANCE_WORK_MEM
                            Size of maintenance working memory in MB

The `--no-sync-commit` option temporarily disables synchronous commits and so
can give a speed boost. The `--work-mem` and `--maintenance-work-mem` options
temporarily increase the amount of working memory that the PostgreSQL server
uses.

### `gazetteer`

This is an internal package that defines classes that are used by the above
programs.
