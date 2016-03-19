# fields.py

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
