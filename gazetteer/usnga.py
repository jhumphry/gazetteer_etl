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

from .fields import SmallIntField, IntegerField, DoubleField, DateField
from .fields import FixedTextField, TextField, FlagField
from .tables import GazetteerTable
from .indexes import GazetteerBTreeIndex


Geonames = GazetteerTable(
    filename_regexp='geonames_([0-9]{8}).txt',
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

GeonamesFullNameROIndex = GazetteerBTreeIndex(
    name='geonames_full_name_ro_idx',
    schema='usnga',
    table_name='geonames',
    columns='full_name_ro text_pattern_ops'
    )

tables = (
    Geonames,
    )

indexes = (
    GeonamesFullNameROIndex,
    )
