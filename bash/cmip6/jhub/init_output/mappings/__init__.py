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



# Set of CMIP5 institute to CMIP6 institute mappings.
INSTITUTE_MAPPINGS = {
    'lasg-cess': 'thu'
    }

# Map of CMIP5 component to CMIP6 realm mappings.
REALM_MAPPINGS = {
    'aerosols': 'aerosol',
    'atmosphere': 'atmos',
    'atmospheric chemistry': 'atmoschem',
    'land ice': 'landice',
    'land surface': 'land',
    'sea ice': 'seaice',
}

# Map of CMIP6 realm to CMIP5 component mappings.
COMPONENT_MAPPINGS = {j: i for i, j in REALM_MAPPINGS.items()}

# Set of source identifier mappings.
SOURCE_ID_MAPPINGS = {
    'ipsl': {
        'ipsl-cm5a-lr': 'ipsl-cm6a-lr'
    },
    'noaa-gfdl': {
        'gfdl-cm2p1': 'gfdl-am4',
        'gfdl-cm2p1': 'gfdl-cm4',
        'gfdl-cm2p1': 'gfdl-esm4'
    }
}

# Set of CMIP5 component property to CMIP6 specialization mappings.
PROPERTY_MAPPINGS = collections.OrderedDict()

# Map of CMIP5 enum choices to CMIP6 enum choices.
ENUM_CHOICE_MAPPINGS = {
    '3 extinction depths': '3 extinction depth',
    'Convective momentum transport (CMT)': 'convective momentum transport',
    'Coupled with deep and shallow': ['coupled with deep', 'coupled with shallow'],
    'Harmonic (second order)': 'Harmonic',
    'IR brightness and visible optical depth': ['IR brightness', 'visible optical depth'],
    'Non-linear split-explicit': 'Non-linear semi-explicit',
    'Present-day': 'present day',
    'Radiative effects of anvils': 'radiative effect of anvils',
    'Separated': 'separate diagnosis',
    'Spaceborne': 'space borne',
    'TVD': 'Total Variance Dissipation (TVD)',
    'Time + space varying (Smagorinski)': 'Time + space varying (Smagorinsky)',
    'Turbulent closure (KPP)': 'Turbulent closure - KPP',
    'Turbulent closure (TKE)': 'Turbulent closure - TKE',
    'Wide-band (Morcrette)': 'wide-band model',
    'Wide-band model (Fouquart)': 'wide-band model'
}
ENUM_CHOICE_MAPPINGS = {k.lower(): v for k, v in ENUM_CHOICE_MAPPINGS.items()}


def init():
    """Initialises mappings from csv files.

    """
    dpath = os.path.dirname(__file__)
    fpaths = glob.glob(os.path.join(dpath, "*.csv"))
    for fpath in fpaths:
        _init_mappings(fpath)


def _init_mappings(fpath):
    """Initialises mappings from a single csv file.

    """
    with open(fpath, 'rU') as fstream:
        data = [i for i in csv.reader(fstream) if i[0] != '']
        data = data[1:]
        for mapping in [_Mapping(i) for i in data]:
            if mapping.cmip6_id:
                try:
                    spec = pyesdoc.get_property_specialization(mapping.cmip6_id)
                except KeyError:
                    print 'CSV ERROR: ', mapping.cmip6_id
                else:
                    PROPERTY_MAPPINGS[mapping.cmip5_id.lower()] = spec


class _Mapping(object):
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


def get_institute(m):
    """Maps a CIM v1 model component to a CMIP6 institute identifier.

    :param cim.v1.Model m: CMIP5 model document.

    :returns: CMIP6 institute identifier.
    :rtype: str

    """
    identifier = m.meta.institute.lower()

    return INSTITUTE_MAPPINGS.get(identifier, identifier)


def get_realm(c):
    """Maps a CIM v1 model component to a CMIP6 realm identifier.

    :param cim.v1.Component c: CMIP5 model component.

    :returns: CMIP6 realm identifier.
    :rtype: str

    """
    identifier = c.ext.long_display_name.lower().split(' > ')[0]

    return REALM_MAPPINGS.get(identifier, identifier)


def get_source_id(m):
    """Maps a CIM v1 model component to a CMIP6 source identifier.

    :param cim.v1.Model m: CMIP5 model document.

    :returns: CMIP6 source identifier.
    :rtype: str

    """
    institute_id = get_institute(m)
    if institute_id is None or institute_id not in SOURCE_ID_MAPPINGS:
        return

    identifier = m.short_name.lower()

    return SOURCE_ID_MAPPINGS[institute_id].get(identifier, identifier)


def _get_property_id(c, p):
    """Maps a CIM v1 CMIP5 model property to a CMIP5 property identifier.

    :param cim.v1.Component c: CMIP5 model component.
    :param cim.v1.ComponentProperty p: CMIP5 model component property.

    :returns: A property identifier.
    :rtype: str

    """
    identifier = p.ext.full_display_name[3:].lower()
    if len(c.ext.long_display_name.split(' > ')) == 1:
        identifier = identifier.replace('scientific properties', 'key properties')
        # print identifier, identifier in PROPERTY_MAPPINGS

    return identifier


def get_component_properties(c):
    """Returns a collection of component properties that can be mapped to CMIP6 model properties.

    :param cim.v1.Component c: CMIP5 model component.

    :returns: A list of 2 member tuples: (specialization_id, cim.v1.ComponentProperty)
    :rtype: list

    """
    result = []
    for c in [c] + c.ext.component_tree:
        for p in c.ext.displayable_scientific_properties:
            p_id = _get_property_id(c, p)
            if p_id in PROPERTY_MAPPINGS:
                p.values = [i for i in p.values if _is_mappable_value(i)]
                if p.values:
                    result.append((p, PROPERTY_MAPPINGS[p_id]))

    return sorted(result, key=lambda i: i[0])


def _is_mappable_value(val):
    """Returns a flag indicating whether a property value is ammpable or not.

    """
    return val is not None and \
           str(val).strip().lower() not in {'', 'other'}
