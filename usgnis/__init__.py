# usgnis

'''Descriptions of USGNIS data files'''

from .fields import *
from .tables import *

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

USGNIS_Files = (
    NationalFedCodes,
    CensusClassCodeDefinitions,
    FeatureClassCodeDefinitions
    )