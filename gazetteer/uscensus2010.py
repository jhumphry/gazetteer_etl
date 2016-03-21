# gazetteer.uscensus2010

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
files that describe the results of the 2010 US Census. Note that this project
is not endorsed by or affiliated with the US Census Bureau.'''

from .fields import BigIntField, IntegerField, DoubleField
from .fields import TextField, FixedTextField, FlagField
from .tables import GazetteerTable


Counties = GazetteerTable(
    filename_regexp='Gaz_counties_national.txt',
    schema='uscensus2010',
    table_name='counties',
    fields=(FixedTextField('USPS', width=2, nullable=False),
            BigIntField('GEOID', nullable=False),
            IntegerField('ANSICODE', nullable=False),
            TextField('NAME', nullable=False),
            IntegerField('POP10', nullable=False),
            IntegerField('HU10', nullable=False),
            DoubleField('ALAND', nullable=False),
            DoubleField('AWATER', nullable=False),
            DoubleField('ALAND_SQMI', nullable=False),
            DoubleField('AWATER_SQMI', nullable=False),
            DoubleField('INTPTLAT', nullable=False),
            DoubleField('INTPTLONG', nullable=False)
            ),
    pk='geoid',
    sep='\t',
    encoding='ISO-8859-1'
    )


CountiesSubdivisions = GazetteerTable(
    filename_regexp='Gaz_cousubs_national.txt',
    schema='uscensus2010',
    table_name='counties_subdivisions',
    fields=(FixedTextField('USPS', width=2, nullable=False),
            BigIntField('GEOID', nullable=False),
            IntegerField('ANSICODE', nullable=False),
            TextField('NAME', nullable=False),
            FlagField('FUNCSTAT10', nullable=False),
            IntegerField('POP10', nullable=False),
            IntegerField('HU10', nullable=False),
            DoubleField('ALAND', nullable=False),
            DoubleField('AWATER', nullable=False),
            DoubleField('ALAND_SQMI', nullable=False),
            DoubleField('AWATER_SQMI', nullable=False),
            DoubleField('INTPTLAT', nullable=False),
            DoubleField('INTPTLONG', nullable=False)
            ),
    pk='geoid',
    sep='\t',
    encoding='ISO-8859-1'
    )


Places = GazetteerTable(
    filename_regexp='Gaz_places_national.txt',
    schema='uscensus2010',
    table_name='places',
    fields=(FixedTextField('USPS', width=2, nullable=False),
            BigIntField('GEOID', nullable=False),
            IntegerField('ANSICODE', nullable=False),
            TextField('NAME', nullable=False),
            FixedTextField('LSAD', width=2, nullable=False),
            FlagField('FUNCSTAT', nullable=False),
            IntegerField('POP10', nullable=False),
            IntegerField('HU10', nullable=False),
            DoubleField('ALAND', nullable=False),
            DoubleField('AWATER', nullable=False),
            DoubleField('ALAND_SQMI', nullable=False),
            DoubleField('AWATER_SQMI', nullable=False),
            DoubleField('INTPTLAT', nullable=False),
            DoubleField('INTPTLONG', nullable=False)
            ),
    pk='geoid',
    sep='\t',
    encoding='ISO-8859-1'
    )


tables = (
    Counties,
    CountiesSubdivisions,
    Places
    )
