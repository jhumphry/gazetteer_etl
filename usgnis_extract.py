# usgnis_extract.py

# Copyright 2016, James Humphry

#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#

''' usgnis_schema.py - This program connects to a database and creates or
recreates a schema that matches the data files provided by USGNIS.'''

import os
import sys
import argparse
import zipfile
import contextlib

import psycopg2

import usgnis
import usgnis.mockdb

parser = argparse.ArgumentParser(description='Upload USGNIS data to a '
                                 'PostgreSQL database')
parser.add_argument('file', metavar='FILE',
                    help='The file to extract and upload data from')
parser.add_argument('type', help='Override recognition of the type of file',
                    metavar='TYPE', nargs='?', default='DEFAULT')

parser_db = parser.add_argument_group('database arguments')
parser_db.add_argument('--dry-run', help='Dump commands to a file rather than '
                                         'executing them on the database',
                       nargs='?', metavar='LOG FILE', default=None,
                       type=argparse.FileType('x'))
parser_db.add_argument('--database',
                       help='PostgreSQL database to use (default usgnis)',
                       action='store', default='usgnis')
parser_db.add_argument('--user', help='PostgreSQL user for upload',
                       action='store',
                       default=os.environ.get('USER', 'postgres'))
parser_db.add_argument('--password', help='PostgreSQL user password',
                       action='store', default='')
parser_db.add_argument('--host', help='PostgreSQL host (if using TCP/IP)',
                       action='store', default=None)
parser_db.add_argument('--port', help='PostgreSQL port (if required)',
                       action='store', type=int, default=5432)
parser_db.add_argument("--no-sync-commit", help="Disable synchronous commits",
                       action="store_true", default=False)
parser_db.add_argument("--work-mem", help="Size of working memory in MB ",
                       action="store", type=int, default=0)
parser_db.add_argument("--maintenance-work-mem",
                       help="Size of maintenance working memory in MB",
                       action="store", type=int, default=0)
args = parser.parse_args()

if args.dry_run:
    connection = usgnis.mockdb.Connection(args.dry_run)
else:
    if args.host:
        connection = psycopg2.connect(database=args.database,
                                      user=args.user,
                                      password=args.password,
                                      host=args.host,
                                      port=args.post)
    else:
        connection = psycopg2.connect(database=args.database,
                                      user=args.user,
                                      password=args.password)

file_ext = os.path.splitext(args.file)[1]

if file_ext == '.txt' or file_ext == '.csv':
    table = usgnis.find_table(os.path.split(args.file)[-1])

    if table is None:
        print('Cannot identify file type')
        sys.exit(1)
    else:
        print('Uploading data to {}.'.format(table.table_name))

    with open(args.file, 'r') as fp, \
            connection.cursor() as cur:

        if not table.check_header(fp.readline()):
            print('File {} does not have the correct header'.format(args.file))
            sys.exit(1)

        if args.no_sync_commit:
            cur.execute("SET SESSION synchronous_commit=off;")

        if args.work_mem != 0:
            cur.execute("SET SESSION work_mem=%s;", (args.work_mem*1024,))

        if args.maintenance_work_mem != 0:
            cur.execute("SET SESSION maintenance_work_mem=%s;",
                        (args.maintenance_work_mem*1024,))

        table.copy_data(fp, cur)
        connection.commit()

connection.autocommit = True
with connection.cursor() as cur:
    cur.execute("VACUUM ANALYZE;")
connection.close()
