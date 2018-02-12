# -*- coding: utf-8 -*-

"""
.. module:: mapper_ipython.py
   :license: GPL/CeCIL
   :platform: Unix, Windows
   :synopsis: Maps CMIP5 CIM (v1) model documents to lightweight IPython format.

.. moduleauthor:: Mark Conway-Greenslade <momipsl@ipsl.jussieu.fr>

"""
from pyesdoc.ipython.model_topic import NotebookOutput

import convertor
import defaults
import mappings

from sh.utils import get_archive_output_fpath



def map(data):
    """Maps a CMIP5 model component to a CMIP6 Ipython notebook output.

    :param tuple data: 2 member tuple: (model, component).

    :returns: CMIP6 IPython notebook output.
    :rtype: dict

    """
    # Unpack.
    m, c = data
    institution_id = mappings.get_institute(m)
    source_id = defaults.get_source_id(m, c)
    realm = mappings.get_realm(c)
    path = get_archive_output_fpath(institution_id, source_id, realm)

    # Set notebook output.
    doc = NotebookOutput('cmip6', institution_id, source_id, realm, path=path, auto_save=False)
    doc.seeding_source = doc.seeding_source or 'cmip5:{}'.format(m.short_name.lower())

    # Set notebook content.
    for p, spec in mappings.get_component_properties(c):
        vals = convertor.convert_property_values(p.values, spec)
        doc.set_id(spec.id)
        for val in vals:
            try:
                doc.set_value(val)
            except ValueError:
                pass
        doc.sort_values()

    return doc
