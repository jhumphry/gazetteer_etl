# gazetteer_schema.py

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

''' gazetteer_schema.py - This program connects to a database and creates or
recreates a schema that matches gazetteer data files provided by various
sources. Note that this program is not associated with or endorsed by any of
the supported sources.'''

import os
import sys
import argparse

import psycopg2

import gazetteer
import gazetteer.mockdb

# Parse command line arguments

parser = argparse.ArgumentParser(description='Create or modify a PostgreSQL '
                                 'database schema for gazetteer data')
parser.add_argument('action', metavar='ACTION',
                    choices=['create', 'truncate', 'list'],
                    help='Whether to "create", "truncate" or "list" tables')
parser.add_argument('table',
                    help='The database schema or table to act on, or ALL',
                    metavar='TABLE', nargs='?', default='ALL')

parser_po = parser.add_argument_group('processing options')
parser_po.add_argument('--drop-existing', help='Drop existing tables (and any '
                       'data) before recreating', action='store_true',
                       default=False)

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
args = parser.parse_args()

# List tables in each schema if requested

if args.action == 'list':
    print('Valid PostgreSQL table names are:')
    for i in gazetteer.gazetteer_schema:
        print('Schema {}:'.format(i))
        for j in gazetteer.gazetteer_schema[i]:
            print(' {0}.{1}'.format(i, j))
    sys.exit(0)

# Create database connection

if args.dry_run:
    connection = gazetteer.mockdb.Connection(args.dry_run)
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

# Create tables or truncate them

with connection.cursor() as cur:
    for i in gazetteer.gazetteer_schema:
        cur.execute('CREATE SCHEMA IF NOT EXISTS {};'.format(i))

    if args.table == 'ALL':
        tables = gazetteer.gazetteer_tables.keys()
    else:
        if args.table in gazetteer.gazetteer_schema:
            tables = [args.table + '.' + x
                      for x in gazetteer.gazetteer_schema[args.table]]
        elif args.table in gazetteer.gazetteer_tables:
            tables = [args.table, ]
        else:
            print('"{}" is not a recognised table name. Use the "list" action '
                  'to list valid table names'.format(args.table))
            sys.exit(1)

    for table in tables:
        if args.action == 'truncate':
            cur.execute('TRUNCATE TABLE {} CASCADE;'.format(table))
        elif args.action == 'create':
            if args.drop_existing:
                cur.execute('DROP TABLE IF EXISTS {} CASCADE;'
                            .format(table))
            cur.execute(gazetteer.gazetteer_tables[table].generate_sql_ddl())

    connection.commit()

# Update database statistics

connection.autocommit = True
with connection.cursor() as cur:
    cur.execute("ANALYZE;")
connection.close()
