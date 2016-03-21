# usgnis

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

'''A package that describes USGNIS data files available from
http://geonames.usgs.gov/domestic/download_data.htm and the associated schema
for upload into a database. Note that this package is not associated with or
endorsed by the U.S. Geological Survey.'''

import copy
import re

from .fields import IntegerField, DoubleField, TextField
from .fields import FixedTextField, DateField, FlagField
from .tables import USGNISTable, USGNISTableCSV, USGNISTableInserted


NationalFile = USGNISTable(
    filename_regexp='NationalFile_([0-9]{8})\.txt',
    table_name='usgnis.national_file',
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
    pk='feature_id, state_numeric'
    )

AllStatesFeatures = copy.copy(NationalFile)
AllStatesFeatures.filename_regexp = \
    re.compile('[A-Z]{2}_Features_([0-9]{8})\.txt')

NationalFedCodes = USGNISTable(
    filename_regexp='NationalFedCodes_([0-9]{8})\.txt',
    table_name='usgnis.national_fed_codes',
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

AllStatesFedCodes = copy.copy(NationalFedCodes)
AllStatesFedCodes.filename_regexp = \
    re.compile('[A-Z]{2}_FedCodes_([0-9]{8})\.txt')

# The Feature_Description_History files currently have lines containing a
# variety of characters, including a '\|' sequence that PostgreSQL's COPY
# command incorrectly interprets as a literal '|' in the data. This data has
# to be processed with a slower, prepared INSERT-based routine.

FeatureDescriptionHistory = USGNISTableInserted(
    filename_regexp='Feature_Description_History_([0-9]{8})\.txt',
    table_name='usgnis.feature_description_history',
    fields=(IntegerField('FEATURE_ID', nullable=False),
            TextField('DESCRIPTION'),
            TextField('HISTORY')
            ),
    pk='feature_id'
    )

GovtUnits = USGNISTable(
    filename_regexp='GOVT_UNITS_([0-9]{8})\.txt',
    table_name='usgnis.govt_units',
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

AllNames = USGNISTableInserted(
    filename_regexp='AllNames_([0-9]{8})\.txt',
    table_name='usgnis.all_names',
    fields=(IntegerField('FEATURE_ID', nullable=False),
            TextField('FEATURE_NAME', nullable=False),
            FlagField('FEATURE_NAME_OFFICIAL'),
            TextField('CITATION', nullable=False),
            DateField('DATE_CREATED')
            ),
    pk='feature_id, feature_name'
    )

AntarcticaFeatures = USGNISTable(
    filename_regexp='ANTARCTICA_([0-9]{8})\.txt',
    table_name='usgnis.antarctica',
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
    pk='antarctica_feature_id'
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
    fields=(TextField('Class', nullable=False),
            TextField('Description', nullable=False),
            ),
    pk='class'
    )

USGNIS_Tables = {
    'national_file': NationalFile,
    'national_fed_codes': NationalFedCodes,
    'feature_description_history': FeatureDescriptionHistory,
    'govt_units': GovtUnits,
    'all_names': AllNames,
    'antarctica': AntarcticaFeatures,
    'census_class_code_definitions': CensusClassCodeDefinitions,
    'feature_class_code_definitions': FeatureClassCodeDefinitions
    }

USGNIS_Files = USGNIS_Tables.copy()
USGNIS_Files['allstate_features'] = AllStatesFeatures
USGNIS_Files['allstate_fed_codes'] = AllStatesFedCodes


def find_table(file_name):
    '''Given a file name, return the USGNISTable or USGNITSTableCSV that it
    is likely to relate to, or None if it does not appear to be related to any
    of them.'''

    for i in USGNIS_Files:
        if USGNIS_Files[i].match_name(file_name)[0]:
            return USGNIS_Files[i]
    return None
