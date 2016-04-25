# gazetteer.tables

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

'''Descriptions of the tables in Gazetteer data files, along with information
on generating appropriate SQL'''

import re


class GazetteerTable:
    '''This class defines both a file that can be read, and a database table
    that the data can be uploaded to.'''

    REQUIRES_TEXTIO = True

    def __init__(self, filename_regexp, schema, table_name,
                 fields, pk, sep='|', encoding=None, datestyle='MDY'):
        self.filename_regexp = re.compile(filename_regexp)
        self.schema = schema
        self.table_name = table_name
        self.full_table_name = schema + '.' + table_name
        self.fields = fields
        self.pk = pk
        self.sep = sep
        self.encoding = encoding
        self.datestyle = datestyle

    def match_name(self, filename):
        '''Return a Boolean that indicates if the filename matches the pattern
        for this table.'''

        return self.filename_regexp.fullmatch(filename)

    def check_header(self, file_object, print_debug=False):
        '''Return a Boolean value based on whether the provided header row
        matches the expectation in the code'''

        header = file_object.readline()

        columns = header.strip('\ufeff\n ').split(self.sep)
        if len(columns) != len(self.fields):
            if print_debug:
                print('Wrong number of columns: {} expected : {}'
                      .format(len(columns), len(self.fields)))
            return False

        for i in range(0, len(columns)):
            if self.fields[i].field_name != columns[i].strip('" '):
                if print_debug:
                    print('Unknown column name: {}'
                          .format(columns[i].strip('"')))
                return False

        return True

    def generate_sql_ddl(self):
        '''Return the SQL describing a table of this sort'''

        result = 'CREATE TABLE {} (\n'.format(self.full_table_name)
        for i in self.fields[:-1]:
            result += '    ' + i.generate_sql() + ',\n'

        result += '    ' + self.fields[-1].generate_sql()

        if self.pk != '':
            result += ', \n    PRIMARY KEY({})\n'.format(self.pk)
        else:
            result += '\n'

        result += ');\n'
        return result

    def copy_data(self, fileobj, cur):
        '''Copy data from the file object fileobj to the database using the
        cursor cur'''

        cur.execute('SET DATESTYLE=%s;', (self.datestyle, ))

        cur.copy_from(
            file=fileobj,
            table=self.full_table_name,
            sep=self.sep,
            null=''
            )


class GazetteerTableCSV(GazetteerTable):
    '''This is a child class of GazetteerTable that uses the CSV mode of
    PostgreSQL's copy command, for the few files that are provided as CSV.'''

    def __init__(self, filename_regexp, schema, table_name, fields, pk,
                 sep=',', escape='\\', quote='"', null=None, encoding=None,
                 datestyle='MDY', force_null=None):
        self.filename_regexp = re.compile(filename_regexp)
        self.schema = schema
        self.table_name = table_name
        self.full_table_name = schema + '.' + table_name
        self.fields = fields
        self.pk = pk
        self.sep = sep
        self.escape = escape
        self.quote = quote
        self.null = null
        self.encoding = encoding
        self.datestyle = datestyle
        self.force_null = force_null

    def copy_data(self, fileobj, cur):
        '''Copy data from the file object fileobj to the database using the
        cursor cur'''

        cur.execute('SET DATESTYLE=%s;', (self.datestyle, ))

        sql = '''COPY {} FROM STDIN WITH (FORMAT CSV, DELIMITER '{}', ''' \
              .format(self.full_table_name, self.sep)

        if self.null is not None:
            sql += '''NULL '{}', '''.format(self.null)

        if self.force_null is not None:
            sql += '''FORCE_NULL ({}), '''.format(self.force_null)

        sql += ''' ESCAPE '{}', QUOTE '{}');'''.format(self.escape, self.quote)

        cur.copy_expert(sql=sql, file=fileobj)


class GazetteerTableInserted(GazetteerTable):
    '''This functions like the GazetteerTable, except that data is manually
    split in Python and uploaded using a PREPAREd INSERT statement. This is
    slower but works around files with dodgy characters that confuse
    PostgreSQL.'''

    def copy_data(self, fileobj, cur):
        '''Copy data from the file object fileobj to the database using the
        cursor cur'''

        cur.execute('SET DATESTYLE=%s;', (self.datestyle, ))

        prepared_name = 'insert_' + self.table_name.replace('.', '_')
        num_fields = len(self.fields)

        sql_prepare_params = ",".join(["$"+str(x)
                                       for x in range(1, num_fields+1)])
        cur.execute('''PREPARE {0} AS INSERT INTO {1} VALUES ({2});'''
                    .format(prepared_name,
                            self.full_table_name,
                            sql_prepare_params))

        sql_insert_params = ",".join(["%s" for x in range(1, num_fields+1)])
        sql_insert = 'EXECUTE {0} ({1});'.format(prepared_name,
                                                 sql_insert_params)

        for line in fileobj:
            params = [(None if x.strip() == '' else x)
                      for x in line.split(self.sep)]
            cur.execute(sql_insert, params)


class GazetteerTableDuplicate(GazetteerTable):
    '''Some data sources provide their data as multiple overlapping files. Only
    one (the most comprehensive) should be uploaded and the others can be
    ignored unless the type is specifically set. This table type can be used
    to match on the filename, but not do anything with the file itself.'''

    REQUIRES_TEXTIO = False

    def __init__(self, filename_regexp, schema, table_name):
        self.filename_regexp = re.compile(filename_regexp)
        self.schema = schema
        self.table_name = table_name
        self.full_table_name = schema + '.' + table_name
        self.encoding = 'UTF-8'

    def check_header(self, file_object, print_debug=False):
        return True

    def generate_sql_ddl(self):
        return ''

    def copy_data(self, fileobj, cur):
        pass
