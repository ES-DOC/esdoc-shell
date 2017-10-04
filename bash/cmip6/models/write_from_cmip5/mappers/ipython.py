# -*- coding: utf-8 -*-

"""
.. module:: mapper_ipython.py
   :license: GPL/CeCIL
   :platform: Unix, Windows
   :synopsis: Maps CMIP5 CIM (v1) model documents to lightweight IPython format.

.. moduleauthor:: Mark Conway-Greenslade <momipsl@ipsl.jussieu.fr>

"""
import collections

import pyesdoc

import mappings
import seedings
from convertor import convert_property_values



def map(data):
    """Maps a CMIP5 model component to a CMIP6 Ipython notebook output.

    :param tuple data: 2 member tuple: (model, component).

    :returns: CMIP6 IPython notebook output.
    :rtype: dict

    """
    # Unpack.
    m, c = data

    # Map.
    obj = collections.OrderedDict()
    obj['publicationState'] = 0
    obj['mipEra'] = 'cmip6'
    obj['institute'] = mappings.get_institute(m)
    obj['seedingSource'] = 'cmip5::{}'.format(m.short_name.lower())
    obj['sourceID'] = seedings.get_source_id(m, c)
    obj['topic'] = mappings.get_realm(c)
    obj['authors'] = []
    obj['contributors'] = []
    obj['content'] = _get_content(m, c)

    return obj


def _get_content(m, c):
    """Returns notebook content.

    """
    obj = collections.OrderedDict()
    for p, spec in mappings.get_component_properties(c):
        values = convert_property_values(p.values, spec)
        if values:
            obj[spec.id] = {
                'qcStatus': 0,
                'values': values
            }

    return obj

