# gazetteer.usnga

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

'''A package that describes U.S. National Geospacial-Intelligence Agency data
files. Note that this project is not endorsed by or affiliated with the US
NGA.'''

import copy
import re

from .fields import SmallIntField, IntegerField, DoubleField, DateField
from .fields import FixedTextField, TextField, FlagField
from .tables import GazetteerTable, GazetteerTableCSV, GazetteerTableDuplicate
from .indexes import GazetteerBTreeIndex, GazetteerForeignKey


Geonames = GazetteerTable(
    filename_regexp=r'Countries.txt',
    schema='usnga',
    table_name='geonames',
    fields=(SmallIntField('RC', nullable=False),  # Regional font Code
            IntegerField('UFI', nullable=False),  # Unique Feature Identifier
            IntegerField('UNI', nullable=False),  # Unique Name Identifier
            DoubleField('LAT', nullable=False),
            DoubleField('LONG', nullable=False),
            TextField('DMS_LAT', nullable=False),
            TextField('DMS_LONG', nullable=False),
            TextField('MGRS', nullable=False),  # Military Grid RefSystem
            TextField('JOG', nullable=False),  # Joint Operations Graphic
            FlagField('FC', nullable=False),  # Feature Class
            TextField('DSG', nullable=False),  # feature DeSiGnation code
            TextField('PC'),  # Populated place Class
            TextField('CC1', nullable=False),  # primary geopolitical code
            TextField('ADM1'),  # primary administrative div
            IntegerField('POP'),  # POPulation (not maintained)
            DoubleField('ELEV'),  # Elevation in m (not maintained)
            TextField('CC2'),  # secondary geopolitical code
            FixedTextField('NT', width=2, nullable=False),  # Name Type
            FixedTextField('LC', width=3),  # Language Code
            TextField('SHORT_FORM'),  # Short Form name
            TextField('GENERIC'),  # Descriptive part of full name (River etc)
            TextField('SORT_NAME_RO', nullable=False),  # Short Name Read Order
            TextField('FULL_NAME_RO', nullable=False),  # Full Name Read Order
            TextField('FULL_NAME_ND_RO', nullable=False),  # No diacritics
            TextField('SORT_NAME_RG', nullable=False),  # Short Name Rev Gen
            TextField('FULL_NAME_RG', nullable=False),  # Full Name Rev Generic
            TextField('FULL_NAME_ND_RG', nullable=False),  # Full Name Rev Gen
            TextField('NOTE'),
            DateField('MODIFY_DATE', nullable=False),
            TextField('DISPLAY', nullable=False),
            SmallIntField('NAME_RANK'),
            IntegerField('NAME_LINK'),  # Unique Name Id link
            TextField('TRANSL_CD'),  # Transliteration Method Code
            DateField('NM_MODIFY_DATE'),  # Name modification date
            DateField('F_EFCTV_DT'),  # Feature Effective Date
            DateField('F_TERM_DT')  # Feature Termination Date
            ),
    pk='UFI, UNI',
    sep='\t',
    encoding='UTF-8',
    datestyle='ISO'
    )


GeonamesDuplicates = GazetteerTableDuplicate(
    filename_regexp=r'Countries_disclaimer.txt',
    schema='usnga',
    table_name='geonames'
    )


GeonamesCountryFiles = copy.copy(Geonames)
GeonamesCountryFiles.filename_regexp = re.compile('[a-z]{2}.txt')

GeonamesCountryFilesDuplicates = GazetteerTableDuplicate(
    filename_regexp=r'[a-z]{2}_('
                    'administrative_a|hydrographic_h|'
                    'localities_l|populatedplaces_p|'
                    'transportation_r|spot_s|'
                    'hypsographic_t|undersea_u|'
                    'vegetation_v|disclaimer'
                    ').txt',
    schema='usnga',
    table_name='geonames'
    )


GeonamesFullNameNDROIndex = GazetteerBTreeIndex(
    name='geonames_full_name_nd_ro_idx',
    schema='usnga',
    table_name='geonames',
    columns='lower(full_name_nd_ro) text_pattern_ops'
    )


GeonamesCC1Index = GazetteerBTreeIndex(
    name='geonames_cc1_idx',
    schema='usnga',
    table_name='geonames',
    columns='cc1'
    )

GeonamesFKFC = GazetteerForeignKey(
    'geonamesFK_FC',
    'usnga', 'geonames', 'FC',
    'usnga', 'feature_class_codes', 'feature_class'
    )

GeonamesFKDSG = GazetteerForeignKey(
    'geonamesFK_DSG',
    'usnga', 'geonames', 'DSG',
    'usnga', 'feature_designation_codes', 'feature_designation_code'
    )

GeonamesFKNT = GazetteerForeignKey(
    'geonamesFK_NT',
    'usnga', 'geonames', 'NT',
    'usnga', 'name_type_codes', 'name_type_code'
    )

GeonamesFKTRANSL_CD = GazetteerForeignKey(
    'geonamesFK_TRANSL_CD',
    'usnga', 'geonames', 'TRANSL_CD',
    'usnga', 'transliteration_codes', 'transliteration_code'
    )


AdministrativeCodes = GazetteerTableCSV(
    filename_regexp=r'USNGA_Administrative_Codes.csv',
    schema='usnga',
    table_name='administrative_codes',
    fields=(TextField('CC1 ADM1', nullable=False),
            TextField('Administrative Division Name', nullable=False),
            TextField('Administrative Division Class', nullable=False)
            ),
    pk='cc1_adm1'
    )


CountryCodes = GazetteerTableCSV(
    filename_regexp=r'USNGA_Country_Codes.csv',
    schema='usnga',
    table_name='country_codes',
    fields=(TextField('Country Code', nullable=False),
            TextField('Country Name', nullable=False)
            ),
    pk='country_code'
    )

CC1ISO3166Xref = GazetteerTableCSV(
    filename_regexp=r'USNGA_CC1_ISO3166_xref.csv',
    schema='usnga',
    table_name='cc1_iso3166_xref',
    fields=(TextField('COUNTRY', nullable=False),
            TextField('FIPS 10'),
            FixedTextField('ISO 3166 digraph', width=2),
            FixedTextField('ISO 3166 trigraph', width=3),
            TextField('ISO 3166 numeric'),
            TextField('TLD'),
            TextField('IOC'),
            TextField('SOVEREIGNTY'),
            TextField('NOTES')
            ),
    pk='COUNTRY',
    null='*'
    )

CC1ISO3166XrefFIPS10Index = GazetteerBTreeIndex(
    name='cc1_iso3166_xref_fips_10_idx',
    schema='usnga',
    table_name='cc1_iso3166_xref',
    columns='fips_10'
    )

CC1ISO3166XrefISO3166Index = GazetteerBTreeIndex(
    name='cc1_iso3166_xref_iso3166_idx',
    schema='usnga',
    table_name='cc1_iso3166_xref',
    columns='iso_3166_digraph'
    )


FeatureClassCodes = GazetteerTableCSV(
    filename_regexp=r'USNGA_Feature_Class_Codes.csv',
    schema='usnga',
    table_name='feature_class_codes',
    fields=(TextField('Feature Class', nullable=False),
            TextField('Feature Class Description', nullable=False)
            ),
    pk='feature_class'
    )

FeatureDesignationCodes = GazetteerTableCSV(
    filename_regexp=r'USNGA_Feature_Designation_Codes.csv',
    schema='usnga',
    table_name='feature_designation_codes',
    fields=(TextField('Feature Designation Code', nullable=False),
            TextField('Feature Designation Name', nullable=False),
            TextField('Feature Designation Text', nullable=False),
            TextField('Collection Guidance', nullable=False),
            TextField('Feature Class', nullable=False)
            ),
    pk='feature_designation_code'
    )


NameTypeCodes = GazetteerTableCSV(
    filename_regexp=r'USNGA_Name_Type_Codes.csv',
    schema='usnga',
    table_name='name_type_codes',
    fields=(FixedTextField('Name Type Code', width=2, nullable=False),
            TextField('Name Type', nullable=False),
            TextField('Name Type Text', nullable=False)
            ),
    pk='name_type_code'
    )


TransliterationCodes = GazetteerTableCSV(
    filename_regexp=r'USNGA_Transliteration_Codes.csv',
    schema='usnga',
    table_name='transliteration_codes',
    fields=(TextField('Transliteration Code', nullable=False),
            TextField('Transliteration Name', nullable=False)
            ),
    pk='transliteration_code'
    )


tables = (
    Geonames,
    GeonamesDuplicates,
    GeonamesCountryFiles,
    GeonamesCountryFilesDuplicates,
    AdministrativeCodes,
    CountryCodes,
    CC1ISO3166Xref,
    FeatureClassCodes,
    FeatureDesignationCodes,
    NameTypeCodes,
    TransliterationCodes
    )

indexes = (
    GeonamesFullNameNDROIndex,
    GeonamesCC1Index,
    GeonamesFKFC,
    GeonamesFKDSG,
    GeonamesFKNT,
    GeonamesFKTRANSL_CD,
    CC1ISO3166XrefFIPS10Index,
    CC1ISO3166XrefISO3166Index
    )
