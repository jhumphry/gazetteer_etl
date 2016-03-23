# gazetteer.ukapc

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

'''A package that describes UK Antarctic Place-names Committee data files.
Note that this project is not endorsed by or affiliated with the UK Antarctic
Place-names Committee.'''

from .fields import SmallIntField, IntegerField, DoubleField, DateField
from .fields import TextField, FlagField, TimeStampField
from .tables import GazetteerTableCSV, GazetteerTableIndex


BAT = GazetteerTableCSV(
    filename_regexp='apip_bat_gazetteer.csv',
    schema='ukapc',
    table_name='bat',
    fields=(TextField('FID', nullable=False),
            TimeStampField('updated', nullable=False),
            TextField('placename', nullable=False),
            TextField('previousname'),
            DoubleField('lon', nullable=False),
            DoubleField('lat', nullable=False),
            DateField('acceptdate'),
            TextField('description'),
            IntegerField('parent'),
            SmallIntField('level', nullable=False),
            TextField('geom'),
            IntegerField('cga_id'),
            FlagField('featuretype', nullable=False),
            IntegerField('derived'),
            IntegerField('id', nullable=False)
            ),
    pk='id',
    encoding='UTF-8',
    datestyle='DMY',
    indexes=(GazetteerTableIndex(name='bat_placename_pattern_idx',
                                 unique=False,
                                 method='btree',
                                 columns='placename text_pattern_ops'),
             )
    )


tables = (
    BAT,
    )
