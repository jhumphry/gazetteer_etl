# gazetteer.fields

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

'''Descriptions of the fields that can make up gazetteer data files, along
with information on their SQL equivalents'''

import abc


class GazetteerField(metaclass=abc.ABCMeta):
    '''An abstract class that defines a field/column in a gazetteer data
    table.'''

    sql_type_name = 'NONE'

    def __init__(self, field_name, sql_name='', nullable=True):
        self.field_name = field_name
        if sql_name == '':
            self.sql_name = field_name.lower().replace(' ', '_')
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


class BigIntField(GazetteerField):
    '''A gazetteer field corresponding to the SQL type BIGINT.'''

    sql_type_name = 'BIGINT'


class IntegerField(GazetteerField):
    '''A gazetteer field corresponding to the SQL type INTEGER.'''

    sql_type_name = 'INTEGER'


class SmallIntField(GazetteerField):
    '''A gazetteer field corresponding to the SQL type SMALLINT.'''

    sql_type_name = 'SMALLINT'


class DoubleField(GazetteerField):
    '''A gazetteer field corresponding to the SQL type DOUBLE PRECISION.'''

    sql_type_name = 'DOUBLE PRECISION'


class TextField(GazetteerField):
    '''A gazetteer field corresponding to the SQL type TEXT.'''

    sql_type_name = 'TEXT'


class FixedTextField(GazetteerField):
    '''A gazetteer field corresponding to the SQL type CHARACTER VARYING()
     with a defined width.'''

    def __init__(self, field_name, width, sql_name='', nullable=True):
        super().__init__(field_name, sql_name, nullable)
        self.width = width

    def generate_sql(self):
        if self.nullable:
            return self.sql_name + ' CHARACTER VARYING({})'.format(self.width)
        else:
            return self.sql_name + ' CHARACTER VARYING({})'.format(self.width)\
             + ' NOT NULL'


class DateField(GazetteerField):
    '''A gazetteer field corresponding to the SQL type DATE.'''

    sql_type_name = 'DATE'


class TimeStampField(GazetteerField):
    '''A gazetteer field corresponding to the SQL type TIMESTAMP.'''

    sql_type_name = 'TIMESTAMP'


class FlagField(GazetteerField):
    '''This is intended for gazetteer single character fields that are
    sometimes used as a form of Boolean or basic enumeration type. It may be
    more efficient to switch these to the "char" type (with the quotations)
    which is an internal PostgreSQL type which has a fixed width and only
    takes up one byte.'''

    sql_type_name = 'CHARACTER VARYING(1)'
