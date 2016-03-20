# usgnis

'''Descriptions of USGNIS data files'''

from .fields import IntegerField, DoubleField, TextField
from .fields import FixedTextField, DateField
from .tables import USGNISTable, USGNISTableCSV


NationalFile = USGNISTable(
    filename_regexp='NationalFile_([0-9]{8})\.txt',
    table_name='usgnis.nationalfile',
    fields=(IntegerField('FEATURE_ID', nullable=False),
            TextField('FEATURE_NAME', nullable=False),
            TextField('FEATURE_CLASS', nullable=False),
            FixedTextField('STATE_ALPHA', width=2, nullable=False),
            IntegerField('STATE_NUMERIC', nullable=False),
            TextField('COUNTY_NAME', nullable=False),
            IntegerField('COUNTY_NUMERIC', nullable=False),
            TextField('PRIMARY_LAT_DMS', nullable=False),
            TextField('PRIMARY_LONG_DMS', nullable=False),
            DoubleField('PRIM_LAT_DEC', nullable=False),
            DoubleField('PRIM_LONG_DEC', nullable=False),
            TextField('SOURCE_LAT_DMS'),
            TextField('SOURCE_LONG_DMS'),
            DoubleField('SOURCE_LAT_DEC'),
            DoubleField('SOURCE_LONG_DEC'),
            IntegerField('ELEV_IN_M', nullable=False),
            IntegerField('ELEV_IN_FT', nullable=False),
            TextField('MAP_NAME', nullable=False),
            DateField('DATE_CREATED'),
            DateField('DATE_EDITED')
            ),
    pk='feature_id'
    )

NationalFedCodes = USGNISTable(
    filename_regexp='NationalFedCodes_([0-9]{8})\.txt',
    table_name='usgnis.nationalfedcodes',
    fields=(IntegerField('FEATURE_ID', nullable=False),
            TextField('FEATURE_NAME', nullable=False),
            TextField('FEATURE_CLASS', nullable=False),
            TextField('CENSUS_CODE'),
            FixedTextField('CENSUS_CLASS_CODE', width=2),
            TextField('GSA_CODE'),
            TextField('OPM_CODE'),
            IntegerField('STATE_NUMERIC', nullable=False),
            FixedTextField('STATE_ALPHA', width=2, nullable=False),
            IntegerField('COUNTY_SEQUENCE', nullable=False),
            IntegerField('COUNTY_NUMERIC', nullable=False),
            TextField('COUNTY_NAME', nullable=False),
            DoubleField('PRIMARY_LATITUDE', nullable=False),
            DoubleField('PRIMARY_LONGITUDE', nullable=False),
            DateField('DATE_CREATED'),
            DateField('DATE_EDITED')
            ),
    pk='feature_id, county_sequence'
    )

CensusClassCodeDefinitions = USGNISTableCSV(
    filename_regexp='Census_Class_Code_Definitions.csv',
    table_name='usgnis.census_class_code_definitions',
    fields=(FixedTextField('Code', width=2, nullable=False),
            TextField('Description', nullable=False),
            ),
    pk='code'
    )

FeatureClassCodeDefinitions = USGNISTableCSV(
    filename_regexp='Feature_Class_Code_Definitions.csv',
    table_name='usgnis.feature_class_code_definitions',
    fields=(FixedTextField('Class', width=2, nullable=False),
            TextField('Description', nullable=False),
            ),
    pk='class'
    )

USGNIS_Files = {
    'nationalfile': NationalFile,
    'nationalfedcodes': NationalFedCodes,
    'census_class_code_definitions': CensusClassCodeDefinitions,
    'feature_class_code_definitions': FeatureClassCodeDefinitions
    }
