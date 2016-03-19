# tables.py

'''Descriptions of the tables in USGNIS data files, along with information on
generating appropriate SQL'''

import datetime
import re

from .fields import *


class USGNISTable:

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

    def check_header(self, header):
        '''Return a Boolean value based on whether the provided header row
        matches the expectation in the code'''

        columns = header.strip('\ufeff\n ').split(self.sep)
        if len(columns) != len(self.fields):
            return False

        for i in range(0, len(columns)):
            if self.fields[i].field_name != columns[i].strip('"'):
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

    def __init__(self, filename_regexp, table_name, fields, pk, sep=','):
        self.filename_regexp = re.compile(filename_regexp)
        self.table_name = table_name
        self.fields = fields
        self.pk = pk
        self.sep = sep

    def copy_data(self, fileobj, cur):
        '''Copy data from the file object fileobj to the database using the
        cursor cur'''

        sql = 'COPY {} FROM STDIN WITH (FORMAT CSV)'.format(self.table_name)
        cur.copy_expert(sql=sql, file=fileobj)
