# usgnis.tables

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

'''Descriptions of the tables in USGNIS data files, along with information on
generating appropriate SQL'''

import datetime
import re


class USGNISTable:
    '''This class defines both a file provided by USGNIS that can be read, and
    a database table that the data can be uploaded to.'''

    def __init__(self, filename_regexp, table_name, fields, pk, sep='|'):
        self.filename_regexp = re.compile(filename_regexp)
        self.table_name = table_name
        self.fields = fields
        self.pk = pk
        self.sep = sep

    def match_name(self, filename):
        '''Return a tuple with two elements. The first is a Boolean that
        indicates if the filename matches the pattern for this table and the
        second gives the date of the file, or is None'''

        matched = self.filename_regexp.match(filename)
        if matched:
            date_text = matched.groups()
            if len(date_text) == 1:
                file_date = datetime.date(year=int(date_text[0][0:4]),
                                          month=int(date_text[0][4:6]),
                                          day=int(date_text[0][6:8]))
            else:
                file_date = None
            return (True, file_date)
        else:
            return (False, None)

    def check_header(self, header, print_debug=False):
        '''Return a Boolean value based on whether the provided header row
        matches the expectation in the code'''

        columns = header.strip('\ufeff\n ').split(self.sep)
        if len(columns) != len(self.fields):
            if print_debug:
                print('Wrong number of columns: {} expected : {}'
                      .format(len(columns), len(self.fields)))
            return False

        for i in range(0, len(columns)):
            if self.fields[i].field_name != columns[i].strip('"'):
                if print_debug:
                    print('Unknown column name: {}'
                          .format(columns[i].strip('"')))
                return False

        return True

    def generate_sql_ddl(self):
        '''Return the SQL describing a table of this sort'''

        result = 'CREATE TABLE {} (\n'.format(self.table_name)
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

        cur.copy_from(
            file=fileobj,
            table=self.table_name,
            sep=self.sep,
            null=''
            )


class USGNISTableCSV(USGNISTable):
    '''This is a child class of USGNISTable that uses the CSV mode of
    PostgreSQL's copy command, for the few files that are provided as CSV.'''

    def __init__(self, filename_regexp, table_name, fields, pk, sep=',',
                 escape='\\', quote='"'):
        self.filename_regexp = re.compile(filename_regexp)
        self.table_name = table_name
        self.fields = fields
        self.pk = pk
        self.sep = sep
        self.escape = escape
        self.quote = quote

    def copy_data(self, fileobj, cur):
        '''Copy data from the file object fileobj to the database using the
        cursor cur'''

        sql = 'COPY {} FROM STDIN WITH ' \
              '''(FORMAT CSV, DELIMITER '{}', ESCAPE '{}', QUOTE '{}' )''' \
              .format(self.table_name, self.sep, self.escape, self.quote)
        cur.copy_expert(sql=sql, file=fileobj)


class USGNISTableInserted(USGNISTable):
    '''This functions like the USGNISTable, except that data is manually split
    in Python and uploaded using a PREPAREd INSERT statement. This is slower
    but works around files with dodgy characters that confuse PostgreSQL.'''

    def copy_data(self, fileobj, cur):
        '''Copy data from the file object fileobj to the database using the
        cursor cur'''

        prepared_name = 'insert_' + self.table_name.replace('.', '_')
        num_fields = len(self.fields)

        sql_prepare_params = ",".join(["$"+str(x)
                                       for x in range(1, num_fields+1)])
        cur.execute('''PREPARE {0} AS INSERT INTO {1} VALUES ({2});'''
                    .format(prepared_name,
                            self.table_name,
                            sql_prepare_params))

        sql_insert_params = ",".join(["%s" for x in range(1, num_fields+1)])
        sql_insert = 'EXECUTE {0} ({1});'.format(prepared_name,
                                                 sql_insert_params)

        for line in fileobj:
            params = [(None if x.strip() == '' else x)
                      for x in line.split(self.sep)]
            cur.execute(sql_insert, params)
