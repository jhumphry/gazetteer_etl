# usgnis.fields

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

'''Descriptions of the fields that can make up USGNIS data files, along with
information on their SQL equivalents'''


class USGNISField:

    def __init__(self, field_name, sql_name='', nullable=True):
        self.field_name = field_name
        if sql_name == '':
            self.sql_name = field_name.lower()
        else:
            self.sql_name = sql_name
        self.nullable = nullable

    def generate_sql(self):
        '''Return the SQL describing a field of this sort, suitable for
        inclusion in a CREATE TABLE statement'''
        if self.nullable:
            return self.sql_name + ' ' + self.sql_type_name
        else:
            return self.sql_name + ' ' + self.sql_type_name + ' NOT NULL'


class IntegerField(USGNISField):

    sql_type_name = 'INTEGER'


class DoubleField(USGNISField):

    sql_type_name = 'DOUBLE PRECISION'


class TextField(USGNISField):

    sql_type_name = 'TEXT'


class FixedTextField(USGNISField):

    def __init__(self, field_name, width, sql_name='', nullable=True):
        super().__init__(field_name, sql_name, nullable)
        self.width = width

    def generate_sql(self):
        if self.nullable:
            return self.sql_name + ' CHARACTER({})'.format(self.width)
        else:
            return self.sql_name + ' CHARACTER({})'.format(self.width) +\
             ' NOT NULL'


class DateField(USGNISField):

    sql_type_name = 'DATE'


class FlagField(USGNISField):
    '''This is intended for single character fields that are sometimes used as
    a form of Boolean or basic enumeration type. It may be more efficient to
    switch these to the "char" type (with the quotations) which is an internal
    PostgreSQL type which has a fixed width and only takes up one byte.'''

    sql_type_name = 'CHARACTER VARYING(1)'
