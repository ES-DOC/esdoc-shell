# -*- coding: utf-8 -*-

"""
.. module:: mapper_ipython.py
   :license: GPL/CeCIL
   :platform: Unix, Windows
   :synopsis: Maps CMIP5 CIM (v1) model documents to lightweight IPython format.

.. moduleauthor:: Mark Conway-Greenslade <momipsl@ipsl.jussieu.fr>

"""
import os

import pyesdoc
from pyesdoc.ipython.model_topic import NotebookOutput

import mappings
import defaults
from convertor import convert_property_values



def map(data):
    """Maps a CMIP5 model component to a CMIP6 Ipython notebook output.

    :param tuple data: 2 member tuple: (model, component).

    :returns: CMIP6 IPython notebook output.
    :rtype: dict

    """
    # Unpack.
    m, c = data

    # Set notebook output.
    doc = NotebookOutput(
        'cmip6',
        mappings.get_institute(m),
        defaults.get_source_id(m, c),
        mappings.get_realm(c),
        output_dir=os.path.join(os.getenv('ESDOC_HOME'), 'repos/esdoc-jupyterhub'),
        auto_save=False)
    doc.seeding_source = doc.seeding_source or 'cmip5:{}'.format(m.short_name.lower())

    # Set notebook content.
    for p, spec in mappings.get_component_properties(c):
        vals = convert_property_values(p.values, spec)
        doc.set_id(spec.id)
        for val in vals:
            try:
                doc.set_value(val)
            except ValueError:
                pass
        doc.sort_values()

    return doc
