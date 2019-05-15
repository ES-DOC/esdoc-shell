# -*- coding: utf-8 -*-

"""
.. module:: mappings.py
   :license: GPL/CeCIL
   :platform: Unix, Windows
   :synopsis: CMIP5 to CMIP6 vocab mapping utility functions.

.. moduleauthor:: Mark Conway-Greenslade <momipsl@ipsl.jussieu.fr>

"""
import collections
import csv
import glob
import os

import pyesdoc



# Map of CMIP5 institutes to CMIP6 institutes.
_INSTITUTE_MAPPINGS = {
    'csiro-bom': 'csiro-arccss-bom',
    'csiro-qccce': 'csiro',
    'ec-earth': 'ec-earth-consortium',
    'lasg-cess': 'thu'
    }
INSTITUTE_MAPPINGS_REVERSED = {v:k for k, v in _INSTITUTE_MAPPINGS.items()}

# Map of CMIP5 realms to CMIP6 realms.
REALM_MAPPINGS = {
    'aerosols': 'aerosol',
    'atmosphere': 'atmos',
    'atmosphericchemistry': 'atmoschem',
    'atmospheric chemistry': 'atmoschem',
    'landice': 'land',
    'land ice': 'landice',
    'landsurface': 'land',
    'land surface': 'land',
    'ocean': 'ocean',
    'ocean biogeo chemistry': 'ocnbgchem',
    'oceanbiogeochemistry': 'ocnbgchem',
    'seaice': 'seaice',
    'sea ice': 'seaice',
}

# Map of CMIP5 component properties to CMIP6 specializations.
_PROPERTY_MAPPINGS = collections.OrderedDict()

# Map of CMIP5 components to CMIP6 topics.
_TOPIC_MAPPINGS = collections.OrderedDict()

# Map of CMIP5 enum choices to CMIP6 enum choices.
ENUM_CHOICE_MAPPINGS = {k.lower(): v for k, v in {
    '3 extinction depths': '3 extinction depth',
    '3d mass/volume mixing ratio for aerosols': '3D mass/volume ratio for aerosols',
    'bc (black carbon / soot)': 'Black carbon / soot',
    'black carbon / soot': 'BC',
    'Convective momentum transport (CMT)': 'convective momentum transport',
    'Coupled with deep and shallow': ['coupled with deep', 'coupled with shallow'],
    'from atmosphericchemistry model': 'from Atmospheric Chemistry model',
    'Harmonic (second order)': 'Harmonic',
    'IR brightness and visible optical depth': ['IR brightness', 'visible optical depth'],
    'k-correlated': 'correlated-k',
    'Non-linear split-explicit': 'Non-linear semi-explicit',
    'Present-day': 'present day',
    'present day': 'fixed: present day',
    'Radiative effects of anvils': 'radiative effect of anvils',
    'Separated': 'separate diagnosis',
    'Spaceborne': 'space borne',
    'sts (supercooled ternary solution aerosol particule)': 'STS (supercooled ternary solution aerosol particule))',
    'TVD': 'Total Variance Dissipation (TVD)',
    'Time + space varying (Smagorinski)': 'Time + space varying (Smagorinsky)',
    'Turbulent closure (KPP)': 'Turbulent closure - KPP',
    'Turbulent closure (TKE)': 'Turbulent closure - TKE',
    'Use Ocean transport time step': 'use ocean model transport time step',
    'uses atmosphericchemistry time stepping': 'Uses atmospheric chemistry time stepping',
    'vapour/solid/liquid': ['water ice', 'water vapour', 'water liquid'],
    'via stratospheric aerosols optical thickness': 'stratospheric aerosols optical thickness',
    'Wide-band (Morcrette)': 'wide-band model',
    'Wide-band model (Fouquart)': 'wide-band model'
}.items()}


def init():
    """Initialises mappings from csv files.

    """
    dpath = os.path.dirname(__file__)
    dpath = os.path.join(dpath, 'csv-files')
    fpaths = glob.glob(os.path.join(dpath, "*.csv"))
    for fpath in fpaths:
        with open(fpath, 'rU') as fstream:
            data = [i for i in csv.reader(fstream) if i[0] != '']
        data = data[1:]
        if fpath.endswith('property-mappings.csv'):
            _init_property_mappings(data)
        else:
            _init_topic_mappings(data)


def _init_topic_mappings(data):
    """Initialises component mappings from a single csv file.

    """
    for mapping in [_ComponentMapping(i) for i in data]:
        if mapping.cmip6_id:
            _TOPIC_MAPPINGS[mapping.cmip5_id.lower()] = mapping.cmip6_id


def _init_property_mappings(data):
    """Initialises property mappings from a single csv file.

    """
    for mapping in [_PropertyMapping(i) for i in data]:
        if mapping.cmip6_id:
            try:
                spec = pyesdoc.get_property_specialization(mapping.cmip6_id)
            except KeyError:
                print 'CSV ERROR: ', mapping.cmip6_id
            else:
                _PROPERTY_MAPPINGS[mapping.cmip5_id.lower()] = spec


class _ComponentMapping(object):
    '''A mapping between a CMIP5 property and a CMIP6 specialization.

    '''
    def __init__(self, row):
        '''Instance constructor.

        '''
        self.cmip5_id = row[0]
        self.cmip6_id = row[1].lower()


class _PropertyMapping(object):
    '''A mapping between a CMIP5 property and a CMIP6 specialization.

    '''
    def __init__(self, row):
        '''Instance constructor.

        '''
        self.cmip5_component = row[0]
        self.cmip5_property = row[1]
        self.cmip5_property_type = 'Key' if len(row[0].split('>')) == 1 else 'Scientific'
        self.cmip6_id = row[2].lower()


    @property
    def cmip5_id(self):
        '''Returns a CMIP5 identifier.

        '''
        return '{} >> {} Properties > {}'.format(
            self.cmip5_component, self.cmip5_property_type, self.cmip5_property)


def get_cmip5_institute_id(m):
    """Maps a CIM v1 model component to a CMIP5 institute identifier.

    :param cim.v1.Model m: CMIP5 model document.

    :returns: CMIP6 institute identifier.
    :rtype: str

    """
    identifier = m.meta.institute.lower()

    return _INSTITUTE_MAPPINGS.get(identifier, identifier)


def get_cmip5_model_id(m):
    """Returns CMIP5 model identifier.

    :param cim.v1.Model m: CMIP5 model document.

    :returns: CMIP5 model identifier.
    :rtype: str

    """
    return m.short_name.lower()


def get_cmip5_component_id(c):
    """Returns CMIP5 component identifier.

    :param cim.v1.ModelComponent c: CMIP5 component.

    :returns: CMIP5 component identifier.
    :rtype: str

    """
    return c.type.lower()


def get_cmip6_component_identifier(c):
    """Maps a CIM v1 CMIP5 model component to a CMIP6 topic identifier.

    :param cim.v1.Component c: CMIP5 model component.

    :returns: A topic identifier.
    :rtype: str

    """
    identifier = c.ext.full_display_name[3:].lower()

    return _TOPIC_MAPPINGS[identifier]


def _get_cmip5_property_id(c, p):
    """Maps a CIM v1 CMIP5 model property to a CMIP5 property identifier.

    :param cim.v1.Component c: CMIP5 model component.
    :param cim.v1.ComponentProperty p: CMIP5 model component property.

    :returns: A property identifier.
    :rtype: str

    """
    identifier = p.ext.full_display_name[3:].lower()
    if len(c.ext.long_display_name.split(' > ')) == 1:
        identifier = identifier.replace('scientific properties', 'key properties')

    return identifier


def get_cmip5_component_properties(c):
    """Returns CMIP5 component properties that can be mapped to CMIP6 model properties.

    :param cim.v1.Component c: CMIP5 model component.

    :returns: A list of 2 member tuples: (cim.v1.ComponentProperty, cmip6_specialization)
    :rtype: list

    """
    def _is_mappable_property_value(val):
        """Returns a flag indicating whether a property value is mappable or not.

        """
        if val is None:
            return False

        try:
            val = str(val).strip().lower()
        except UnicodeEncodeError:
            pass

        return val not in {'', 'other', 'n/a'}

    result = []
    for c in [c] + c.ext.component_tree:
        for p in c.ext.displayable_scientific_properties:
            cmip5_property_id = _get_cmip5_property_id(c, p)
            try:
                cmip6_specialization = _PROPERTY_MAPPINGS[cmip5_property_id]
            except KeyError:
                pass
            else:
                p.values = [i for i in p.values if _is_mappable_property_value(i)]
                if p.values:
                    result.append((p, cmip6_specialization))

    return sorted(result, key=lambda i: i[0])
