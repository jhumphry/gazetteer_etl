# gazetteer.usgnis

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

'''A package that describes US Geographical Names Information Service data
files that describe US domestic and Antarctic names. Note that this project is
not endorsed by or affiliated with the US Geological Survey.'''

import copy
import re

from .fields import IntegerField, DoubleField, TextField
from .fields import FixedTextField, DateField, FlagField
from .tables import GazetteerTable, GazetteerTableCSV, GazetteerTableInserted
from .indexes import GazetteerBTreeIndex, GazetteerForeignKey


Features = GazetteerTable(
    filename_regexp=r'NationalFile_([0-9]{8})\.txt',
    schema='usgnis',
    table_name='features',
    fields=(IntegerField('FEATURE_ID', nullable=False),
            TextField('FEATURE_NAME', nullable=False),
            TextField('FEATURE_CLASS', nullable=False),
            FixedTextField('STATE_ALPHA', width=3, nullable=False),
            IntegerField('STATE_NUMERIC', nullable=False),
            TextField('COUNTY_NAME'),
            IntegerField('COUNTY_NUMERIC'),
            TextField('PRIMARY_LAT_DMS',
                      sql_name='prim_lat_dms',
                      nullable=False),
            TextField('PRIM_LONG_DMS', nullable=False),
            DoubleField('PRIM_LAT_DEC', nullable=False),
            DoubleField('PRIM_LONG_DEC', nullable=False),
            TextField('SOURCE_LAT_DMS'),
            TextField('SOURCE_LONG_DMS'),
            DoubleField('SOURCE_LAT_DEC'),
            DoubleField('SOURCE_LONG_DEC'),
            IntegerField('ELEV_IN_M'),
            IntegerField('ELEV_IN_FT'),
            TextField('MAP_NAME', nullable=False),
            DateField('DATE_CREATED'),
            DateField('DATE_EDITED')
            ),
    pk='feature_id, state_numeric',
    datestyle='MDY'
    )

FeaturesNameIndex = GazetteerBTreeIndex(
    name='features_feature_name_pattern_idx',
    schema='usgnis',
    table_name='features',
    columns='feature_name text_pattern_ops'
    )

FeaturesStateIndex = GazetteerBTreeIndex(
    name='features_state_idx',
    schema='usgnis',
    table_name='features',
    columns='state_alpha'
    )

FeaturesFK1 = GazetteerForeignKey(
    'featuresFK1',
    'usgnis', 'features', 'feature_class',
    'usgnis', 'feature_class_code_definitions', 'class'
    )

AllStatesFeatures = copy.copy(Features)
AllStatesFeatures.filename_regexp = \
    re.compile(r'[A-Z]{2}_Features_([0-9]{8})\.txt')

FedCodes = GazetteerTable(
    filename_regexp=r'NationalFedCodes_([0-9]{8})\.txt',
    schema='usgnis',
    table_name='fed_codes',
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
    pk='feature_id, county_sequence',
    datestyle='MDY'
    )

FedCodesFK1 = GazetteerForeignKey(
    'fed_codesFK1',
    'usgnis', 'fed_codes', 'census_class_code',
    'usgnis', 'census_class_code_definitions', 'code'
    )

AllStatesFedCodes = copy.copy(FedCodes)
AllStatesFedCodes.filename_regexp = \
    re.compile(r'[A-Z]{2}_FedCodes_([0-9]{8})\.txt')

# The Feature_Description_History files currently have lines containing a
# variety of characters, including a '\|' sequence that PostgreSQL's COPY
# command incorrectly interprets as a literal '|' in the data. This data has
# to be processed with a slower, prepared INSERT-based routine.

FeatureDescriptionHistory = GazetteerTableInserted(
    filename_regexp=r'Feature_Description_History_([0-9]{8})\.txt',
    schema='usgnis',
    table_name='feature_description_history',
    fields=(IntegerField('FEATURE_ID', nullable=False),
            TextField('DESCRIPTION'),
            TextField('HISTORY')
            ),
    pk='feature_id'
    )

GovtUnits = GazetteerTable(
    filename_regexp=r'GOVT_UNITS_([0-9]{8})\.txt',
    schema='usgnis',
    table_name='govt_units',
    fields=(IntegerField('FEATURE_ID', nullable=False),
            TextField('UNIT_TYPE', nullable=False),
            IntegerField('COUNTY_NUMERIC'),
            TextField('COUNTY_NAME'),
            IntegerField('STATE_NUMERIC', nullable=False),
            FixedTextField('STATE_ALPHA', width=2, nullable=False),
            TextField('STATE_NAME', nullable=False),
            FixedTextField('COUNTRY_ALPHA', width=2, nullable=False),
            TextField('COUNTRY_NAME', nullable=False),
            TextField('FEATURE_NAME', nullable=False),
            ),
    pk='feature_id, unit_type'
    )

# Some AllNames files have null bytes in the text, so the slower insert routine
# is required.

AllNames = GazetteerTableInserted(
    filename_regexp=r'AllNames_([0-9]{8})\.txt',
    schema='usgnis',
    table_name='all_names',
    fields=(IntegerField('FEATURE_ID', nullable=False),
            TextField('FEATURE_NAME', nullable=False),
            FlagField('FEATURE_NAME_OFFICIAL'),
            TextField('CITATION', nullable=False),
            DateField('DATE_CREATED')
            ),
    pk='feature_id, feature_name',
    datestyle='MDY'
    )

AntarcticaFeatures = GazetteerTable(
    filename_regexp=r'ANTARCTICA_([0-9]{8})\.txt',
    schema='usgnis',
    table_name='antarctica',
    fields=(IntegerField('ANTARCTICA_FEATURE_ID', nullable=False),
            TextField('FEATURE_NAME', nullable=False),
            TextField('FEATURE_CLASS', nullable=False),
            TextField('PRIMARY_LATITUDE_DMS', nullable=False),
            TextField('PRIMARY_LONGITUDE_DMS', nullable=False),
            DoubleField('PRIMARY_LATITUDE_DEC', nullable=False),
            DoubleField('PRIMARY_LONGITUDE_DEC', nullable=False),
            IntegerField('ELEV_IN_M'),
            IntegerField('ELEV_IN_FT'),
            DateField('DECISION_YEAR'),
            TextField('DESCRIPTION'),
            DateField('DATE_CREATED'),
            DateField('DATE_EDITED')
            ),
    pk='antarctica_feature_id',
    datestyle='MDY'
    )

CensusClassCodeDefinitions = GazetteerTableCSV(
    filename_regexp=r'USGNIS_Census_Class_Code_Definitions.csv',
    schema='usgnis',
    table_name='census_class_code_definitions',
    fields=(FixedTextField('Code', width=2, nullable=False),
            TextField('Description', nullable=False),
            ),
    pk='code'
    )

FeatureClassCodeDefinitions = GazetteerTableCSV(
    filename_regexp=r'USGNIS_Feature_Class_Code_Definitions.csv',
    schema='usgnis',
    table_name='feature_class_code_definitions',
    fields=(TextField('Class', nullable=False),
            TextField('Description', nullable=False),
            ),
    pk='class'
    )


tables = (
    Features,
    AllStatesFeatures,
    FedCodes,
    AllStatesFedCodes,
    FeatureDescriptionHistory,
    GovtUnits,
    AllNames,
    AntarcticaFeatures,
    CensusClassCodeDefinitions,
    FeatureClassCodeDefinitions
    )

indexes = (
    FeaturesNameIndex,
    FeaturesStateIndex,
    FeaturesFK1,
    FedCodesFK1
    )
