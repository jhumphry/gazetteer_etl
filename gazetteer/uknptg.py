# gazetteer.uknptg

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

'''A package that describes Nation Public Transport Gazetteer data files. Note
that this project is not endorsed by or affiliated with the UK Department for
Transport. The files available from data.gov.uk do not actually match the
schema descriptions available from the DfT - it is possible that this may be
corrected at some future point.'''

from .fields import SmallIntField, IntegerField
from .fields import FixedTextField, TextField, FlagField, TimeStampField
from .tables import GazetteerTableCSV
from .indexes import GazetteerBTreeIndex, GazetteerForeignKey


class GazetteerTableCSV_NPTG(GazetteerTableCSV):
    '''Some of the NPTG files have data containing an extra dummy column that
    is not in the header and is always blank.'''

    def __init__(self, dummy_columns, **kwargs):
        self.dummy_columns = dummy_columns
        super().__init__(**kwargs)

    def check_header(self, header, print_debug=False):
        columns = header.strip('\ufeff\n ').split(self.sep)
        if len(columns) + self.dummy_columns != len(self.fields):
            if print_debug:
                print('Wrong number of columns: {} expected : {}'
                      .format(len(columns), len(self.fields)))
            return False

        for i in range(0, len(columns)):
            if self.fields[i].field_name != columns[i].strip('" '):
                if print_debug:
                    print('Unknown column name: {}'
                          .format(columns[i].strip('"')))
                return False

        return True


Localities = GazetteerTableCSV(
    filename_regexp='Localities.csv',
    schema='uknptg',
    table_name='localities',
    fields=(FixedTextField('NptgLocalityCode', width=8, nullable=False),
            TextField('LocalityName', nullable=False),
            FixedTextField('LocalityNameLang', width=2),
            TextField('ShortName'),
            FixedTextField('ShortNameLang', width=2),
            TextField('QualifierName'),
            FixedTextField('QualifierNameLang', width=2),
            TextField('QualifierLocalityRef'),
            TextField('QualifierDistrictRef'),
            SmallIntField('AdministrativeAreaCode', nullable=False),
            IntegerField('NptgDistrictCode', nullable=False),
            FixedTextField('SourceLocalityType', width=3, nullable=False),
            FlagField('GridType'),
            IntegerField('Easting', nullable=False),
            IntegerField('Northing', nullable=False),
            TimeStampField('CreationDateTime', nullable=False),
            TimeStampField('ModificationDateTime'),
            SmallIntField('RevisionNumber'),
            FixedTextField('Modification', width=3),
            FlagField('', sql_name='dummy')
            ),
    pk='nptglocalitycode',
    encoding='UTF-8',
    datestyle='ISO'
    )

LocalitiesNameIndex = GazetteerBTreeIndex(
    name='localities_pattern_idx',
    schema='uknptg',
    table_name='localities',
    columns='localityname text_pattern_ops'
    )

LocalitiesFK1 = GazetteerForeignKey(
    'localitiesFK1',
    'uknptg',
    'localities',
    'administrativeareacode',
    'uknptg',
    'admin_areas',
    'administrativeareacode'
    )

LocalityAlternativeNames = GazetteerTableCSV_NPTG(
    dummy_columns=1,
    filename_regexp='LocalityAlternativeNames.csv',
    schema='uknptg',
    table_name='localities_alternative_names',
    fields=(FixedTextField('NptgLocalityCode', width=8, nullable=False),
            FixedTextField('OldNptgLocalityCode', width=8, nullable=False),
            TextField('LocalityName', nullable=False),
            FixedTextField('LocalityNameLang', width=2),
            TextField('ShortName'),
            FixedTextField('ShortNameLang', width=2),
            TextField('QualifierName'),
            FixedTextField('QualifierNameLang', width=2),
            TextField('QualifierLocalityRef'),
            TextField('QualifierDistrictRef'),
            TimeStampField('CreationDateTime', nullable=False),
            TimeStampField('ModificationDateTime'),
            SmallIntField('RevisionNumber', nullable=False),
            FixedTextField('Modification', width=3),
            FlagField('', sql_name='dummy')
            ),
    pk='nptglocalitycode, oldnptglocalitycode',
    encoding='UTF-8',
    datestyle='ISO'
    )

LocalityAlternativeNamesFK1 = GazetteerForeignKey(
    'localities_alternative_namesFK1',
    'uknptg',
    'localities_alternative_names',
    'nptglocalitycode',
    'uknptg',
    'localities',
    'nptglocalitycode'
    )

LocalityAlternativeNamesFK2 = GazetteerForeignKey(
    'localities_alternative_namesFK2',
    'uknptg',
    'localities_alternative_names',
    'oldnptglocalitycode',
    'uknptg',
    'localities',
    'nptglocalitycode'
    )

AdjacentLocality = GazetteerTableCSV(
    filename_regexp='AdjacentLocality.csv',
    schema='uknptg',
    table_name='adjacent_localities',
    fields=(FixedTextField('NptgLocalityCode', width=8, nullable=False),
            FixedTextField('AdjacentNptgLocalityCode',
                           width=8, nullable=False),
            TimeStampField('CreationDateTime'),
            TimeStampField('ModificationDateTime'),
            SmallIntField('RevisionNumber', nullable=False),
            FixedTextField('Modification', width=3),
            ),
    pk='nptglocalitycode, adjacentnptglocalitycode',
    encoding='UTF-8',
    datestyle='ISO',
    force_null='creationdatetime , modificationdatetime'
    )

AdjacentLocalitiesFK1 = GazetteerForeignKey(
    'adjacent_localitiesFK1',
    'uknptg',
    'adjacent_localities',
    'nptglocalitycode',
    'uknptg',
    'localities',
    'nptglocalitycode'
    )

AdjacentLocalitiesFK2 = GazetteerForeignKey(
    'adjacent_localitiesFK2',
    'uknptg',
    'adjacent_localities',
    'adjacentnptglocalitycode',
    'uknptg',
    'localities',
    'nptglocalitycode'
    )

LocalityHierarchy = GazetteerTableCSV_NPTG(
    dummy_columns=1,
    filename_regexp='LocalityHierarchy.csv',
    schema='uknptg',
    table_name='localities_hierarchy',
    fields=(FixedTextField('ParentNptgLocalityCode', width=8, nullable=False),
            FixedTextField('ChildNptgLocalityCode', width=8, nullable=False),
            TimeStampField('CreationDateTime'),
            TimeStampField('ModificationDateTime'),
            SmallIntField('RevisionNumber', nullable=False),
            FixedTextField('Modification', width=3),
            FlagField('', sql_name='dummy')
            ),
    pk='parentnptglocalitycode, childnptglocalitycode',
    encoding='UTF-8',
    datestyle='ISO'
    )


LocalityHierarchyFK1 = GazetteerForeignKey(
    'localities_hierarchyFK1',
    'uknptg',
    'localities_hierarchy',
    'parentnptglocalitycode',
    'uknptg',
    'localities',
    'nptglocalitycode'
    )

LocalityHierarchyFK2 = GazetteerForeignKey(
    'localities_hierarchyFK2',
    'uknptg',
    'localities_hierarchy',
    'childnptglocalitycode',
    'uknptg',
    'localities',
    'nptglocalitycode'
    )


AdminAreas = GazetteerTableCSV(
    filename_regexp='AdminAreas.csv',
    schema='uknptg',
    table_name='admin_areas',
    fields=(SmallIntField('AdministrativeAreaCode', nullable=False),
            SmallIntField('AtcoAreaCode', nullable=False),
            TextField('AreaName', nullable=False),
            FixedTextField('AreaNameLang', width=2),
            TextField('ShortName'),
            FixedTextField('ShortNameLang', width=2),
            FixedTextField('Country', width=3, nullable=False),
            FixedTextField('RegionCode', width=2, nullable=False),
            SmallIntField('MaximumLengthForShortNames'),
            SmallIntField('National'),
            TextField('ContactEmail'),
            TextField('ContactTelephone'),
            TimeStampField('CreationDateTime', nullable=False),
            TimeStampField('ModificationDateTime'),
            SmallIntField('RevisionNumber'),
            FixedTextField('Modification', width=3)
            ),
    pk='administrativeareacode',
    encoding='UTF-8',
    datestyle='ISO',
    force_null='maximumlengthforshortnames'
    )


AdminAreasFK1 = GazetteerForeignKey(
    'admin_areasFK1',
    'uknptg',
    'admin_areas',
    'regioncode',
    'uknptg',
    'regions',
    'regioncode'
    )


Regions = GazetteerTableCSV(
    filename_regexp='Regions.csv',
    schema='uknptg',
    table_name='regions',
    fields=(FixedTextField('RegionCode', width=2, nullable=False),
            TextField('RegionName', nullable=False),
            FixedTextField('RegionNameLang', width=2),
            TimeStampField('CreationDateTime', nullable=False),
            SmallIntField('RevisionNumber'),
            TimeStampField('ModificationDateTime'),
            FixedTextField('Modification', width=3)
            ),
    pk='regioncode',
    encoding='UTF-8',
    datestyle='ISO'
    )


Districts = GazetteerTableCSV(
    filename_regexp='Districts.csv',
    schema='uknptg',
    table_name='districts',
    fields=(SmallIntField('DistrictCode', nullable=False),
            TextField('DistrictName', nullable=False),
            FixedTextField('DistrictLang', width=2),
            SmallIntField('AdministrativeAreaCode', nullable=False),
            TimeStampField('CreationDateTime', nullable=False),
            TimeStampField('ModificationDateTime'),
            SmallIntField('RevisionNumber'),
            FixedTextField('Modification', width=3)
            ),
    pk='districtcode',
    encoding='UTF-8',
    datestyle='ISO'
    )


DistrictsFK1 = GazetteerForeignKey(
    'districtsFK1',
    'uknptg',
    'districts',
    'administrativeareacode',
    'uknptg',
    'admin_areas',
    'administrativeareacode'
    )


PlusbusZones = GazetteerTableCSV(
    filename_regexp='PlusbusZones.csv',
    schema='uknptg',
    table_name='plusbus_zones',
    fields=(FixedTextField('PlusbusZoneCode', width=12, nullable=False),
            TextField('Name', nullable=False),
            FixedTextField('NameLang', width=2),
            FixedTextField('Country', width=8, nullable=False),
            TimeStampField('CreationDateTime', nullable=False),
            TimeStampField('ModificationDateTime'),
            SmallIntField('RevisionNumber'),
            FixedTextField('Modification', width=3)
            ),
    pk='plusbuszonecode',
    encoding='UTF-8',
    datestyle='ISO'
    )


PlusbusMapping = GazetteerTableCSV(
    filename_regexp='PlusbusMapping.csv',
    schema='uknptg',
    table_name='plusbus_mapping',
    fields=(FixedTextField('PlusbusZoneCode', width=12, nullable=False),
            SmallIntField('Sequence', nullable=False),
            FlagField('GridType'),
            IntegerField('Easting', nullable=False),
            IntegerField('Northing', nullable=False),
            TimeStampField('CreationDateTime', nullable=False),
            TimeStampField('ModificationDateTime'),
            SmallIntField('RevisionNumber'),
            FixedTextField('Modification', width=3)
            ),
    pk='plusbuszonecode, sequence',
    encoding='UTF-8',
    datestyle='ISO'
    )

PlusbusMappingFK1 = GazetteerForeignKey(
    'plusbus_mappingFK1',
    'uknptg',
    'plusbus_mapping',
    'plusbuszonecode',
    'uknptg',
    'plusbus_zones',
    'plusbuszonecode'
    )


tables = (
    Localities,
    LocalityAlternativeNames,
    AdjacentLocality,
    LocalityHierarchy,
    AdminAreas,
    Regions,
    Districts,
    PlusbusZones,
    PlusbusMapping,
    )

indexes = (
    LocalitiesNameIndex,
    LocalitiesFK1,
    LocalityAlternativeNamesFK1,
    LocalityAlternativeNamesFK2,
    AdjacentLocalitiesFK1,
    AdjacentLocalitiesFK2,
    LocalityHierarchyFK1,
    LocalityHierarchyFK2,
    AdminAreasFK1,
    DistrictsFK1,
    PlusbusMappingFK1
    )
