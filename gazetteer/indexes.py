# gazetteer.indexes

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

'''Descriptions of indexes for the tables in Gazetteer data files, along with
information on generating appropriate SQL'''


class GazetteerBTreeIndex:
    '''This class defines basic btree indexes on a table'''

    def __init__(self, name, schema, table_name, columns,
                 unique=False, where=None, fillfactor=100):

        self.name = name
        self.schema = schema
        self.table_name = table_name
        self.full_table_name = schema + '.' + table_name
        if isinstance(columns, str):
            self.columns = (columns, )
        else:
            self.columns = columns
        self.unique = unique
        self.where = where
        self.fillfactor = fillfactor

    def generate_sql(self, drop_existing=False):
        '''Return the text of a SQL statement that will create the index. If
        specified, drop the existing index first.'''

        result = ''

        if drop_existing:
            result += self.generate_drop_sql()

        unique_text = 'UNIQUE' if self.unique else ''

        result += 'CREATE {0} INDEX IF NOT EXISTS {1} ON {2}.{3} '\
                  'USING btree\n    ('.format(unique_text,
                                              self.name,
                                              self.schema,
                                              self.table_name)

        for c in self.columns[:-1]:
            result += c + ',\n    '
        result += self.columns[-1] + '\n    )\n'

        result += 'WITH (fillfactor = {})'.format(self.fillfactor)

        if self.where is not None:
            result += '\n' + self.where

        result += ';\n\n'

        return result

    def generate_drop_sql(self):
        '''Return the text of a SQL statement that will drop the index.'''

        return 'DROP INDEX IF EXISTS {0}.{1} CASCADE;\n\n' \
               .format(self.schema, self.name)


class GazetteerForeignKey:
    '''This class defines foreign keys on a table'''

    def __init__(self, name, schema, table_name, columns,
                 foreign_schema, foreign_table_name, foreign_columns):

        self.name = name

        self.schema = schema
        self.table_name = table_name
        self.full_table_name = schema + '.' + table_name
        if isinstance(columns, str):
            self.columns = (columns, )
        else:
            self.columns = columns

        self.foreign_schema = foreign_schema
        self.foreign_table_name = foreign_table_name
        if isinstance(foreign_columns, str):
            self.foreign_columns = (foreign_columns, )
        else:
            self.foreign_columns = foreign_columns

    def generate_sql(self, drop_existing=False):
        '''Return the text of a SQL statement that will create the index. If
        specified, drop the existing index first.'''

        result = ''

        if drop_existing:
            result += self.generate_drop_sql()

        result += 'ALTER TABLE {0} ADD CONSTRAINT {1} FOREIGN KEY ('\
                  .format(self.full_table_name, self.name)

        for c in self.columns[:-1]:
            result += c + ',\n    '
        result += self.columns[-1] + ')\n'

        result += 'REFERENCES {0}.{1} ('\
                  .format(self.foreign_schema, self.foreign_table_name)

        for c in self.foreign_columns[:-1]:
            result += c + ',\n    '
        result += self.foreign_columns[-1] + ');\n'

        return result

    def generate_drop_sql(self):
        '''Return the text of a SQL statement that will drop the index.'''

        return 'ALTER TABLE {0} DROP CONSTRAINT IF EXISTS {1} CASCADE;\n\n' \
               .format(self.full_table_name, self.name)
