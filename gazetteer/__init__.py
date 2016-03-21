# gazetteer

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

'''A package that describes gazetteer data files and the associated schema for
upload into a database.'''

import gazetteer.usgnis
import gazetteer.uscensus2010

gazetteer_schema = {}
gazetteer_tables = {}
gazetteer_files = []


def register_tables(tables):
    '''Register a sequence of GazetteerTable objects'''

    # There can be more than one supported file for a given SQL table.
    # Therefore the gazetteer_files dict is comprehensive, but gazetteer_tables
    # only records the first table to provide the information for a SQL table.

    for i in tables:

        if i.schema not in gazetteer_schema:
            gazetteer_schema[i.schema] = set()
        gazetteer_schema[i.schema].add(i.table_name)

        gazetteer_files.append(i)

        if i.full_table_name not in gazetteer_tables:
            gazetteer_tables[i.full_table_name] = i


def find_table(file_name):
    '''Given a file name, return the GazetteerTable or GazetteerTableCSV that
    it is likely to relate to, or None if it does not appear to be related to
    any of them.'''

    for i in gazetteer_files:
        if i.match_name(file_name)[0]:
            return i
    return None

# Actually register the tables defined in each module

register_tables(usgnis.tables)
register_tables(uscensus2010.tables)
