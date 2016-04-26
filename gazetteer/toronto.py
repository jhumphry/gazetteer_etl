# gazetteer.toronto

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

'''A package that describes Toronto Address Point WGS84 files. Note that this
project is not endorsed by or affiliated with the City of Toronto.'''

from .fields import SmallIntField, IntegerField, DoubleField
from .fields import TextField, FlagField
from .tables import dbfread_available, GazetteerTableDBF
from .tables import GazetteerTableInserted, GazetteerTableDuplicate


class TorontoFeatureCodesCSV(GazetteerTableInserted):
    '''A special version of GazetteerTableInserted to cope with the
    non-standard header on the feature codes descriptions file.'''

    def check_header(self, file_object, print_debug=False):
        header = file_object.readline()
        if header != 'ADDRESS FEATURE CODES\n':
            return False
        return True


AddressPoint = GazetteerTableDBF(
    filename_regexp=r'ADDRESS_POINT_WGS84.dbf',
    schema='toronto',
    table_name='address_point',
    fields=(IntegerField('GEO_ID', nullable=False),
            IntegerField('LINK', nullable=False),
            TextField('MAINT_STAG', nullable=False),
            TextField('ADDRESS', nullable=False),
            TextField('LFNAME', nullable=False),
            SmallIntField('LONUM', nullable=False),
            TextField('LONUMSUF'),
            SmallIntField('HINUM', nullable=False),
            TextField('HINUMSUF'),
            FlagField('ARC_SIDE', nullable=False),
            DoubleField('DISTANCE', nullable=False),
            IntegerField('FCODE', nullable=False),
            TextField('FCODE_DES', nullable=False),
            TextField('CLASS', nullable=False),
            TextField('NAME'),
            DoubleField('X', nullable=False),
            DoubleField('Y', nullable=False),
            DoubleField('LONGITUDE', nullable=False),
            DoubleField('LATITUDE', nullable=False),
            IntegerField('OBJECTID', nullable=False),
            TextField('MUN_NAME', nullable=False),
            TextField('WARD_NAME', nullable=False)
            ),
    pk='geo_id',
    encoding='UTF-8'
    )

AddressFeatureCodes = TorontoFeatureCodesCSV(
    filename_regexp=r'readme_address_points_Jan2013.txt',
    schema='toronto',
    table_name='feature_codes',
    fields=(IntegerField('fcode', nullable=False),
            TextField('description', nullable=False)
            ),
    pk='fcode',
    sep='\t',
    encoding='cp1252'
    )

AddressPointDiscards = GazetteerTableDuplicate(
    filename_regexp=r'ADDRESS_POINT_WGS84('
                    r'.prj|_readme.txt|.shp|'
                    r'.shp.xml|.shx)',
    schema='usnga',
    table_name='other'
    )

if dbfread_available:
    tables = (
        AddressPoint,
        AddressFeatureCodes,
        AddressPointDiscards
        )

    indexes = tuple()

else:
    tables = tuple()
    indexes = tuple()
