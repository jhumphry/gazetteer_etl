# fields.py

'''Descriptions of the fields that can make up USGNIS data files, along with
information on their SQL equivalents'''

import abc


class USGNISField(metaclass=abc.ABCMeta):

    def __init__(self, field_name, sql_name='', nullable=True):
        self.field_name = field_name
        if sql_name == '':
            self.sql_name = field_name.lower()
        else:
            self.sql_name = sql_name
        self.nullable = nullable
        self.nullable_string = '' if nullable else ' NOT NULL'

    @abc.abstractmethod
    def generate_sql(self):
        '''Return the SQL describing a field of this sort, suitable for
        inclusion in a CREATE TABLE statement'''
        pass


class IntegerField(USGNISField):

    def generate_sql(self):
        return self.sql_name + ' INTEGER' + self.nullable_string


class DoubleField(USGNISField):

    def generate_sql(self):
        return self.sql_name + ' DOUBLE PRECISION' + self.nullable_string


class TextField(USGNISField):

    def generate_sql(self):
        return self.sql_name + ' TEXT' + self.nullable_string


class FixedTextField(USGNISField):

    def __init__(self, field_name, width, sql_name='', nullable=True):
        super().__init__(field_name, sql_name, nullable)
        self.width = width

    def generate_sql(self):
        return self.sql_name + ' CHARACTER({})'.format(self.width) +\
            self.nullable_string


class DateField(USGNISField):

    def generate_sql(self):
        return self.sql_name + ' DATE' + self.nullable_string
