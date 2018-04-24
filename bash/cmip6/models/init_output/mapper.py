# -*- coding: utf-8 -*-

"""
.. module:: mapper_ipython.py
   :license: GPL/CeCIL
   :platform: Unix, Windows
   :synopsis: Maps CMIP5 CIM (v1) model documents to lightweight IPython format.

.. moduleauthor:: Mark Conway-Greenslade <momipsl@ipsl.jussieu.fr>

"""
import os

from pyesdoc.ipython.model_topic import NotebookOutput

import convertor
import defaults
import mappings

from sh.utils import get_archive_output_fpath



def map(cmip5_model_id, cmip5_component, cmip6_institution_id, cmip6_source_id, cmip6_topic):
    """Maps a CMIP5 model component to a CMIP6 Ipython notebook output.

    :param str cmip5_model_id: CMIP5 model identifier.
    :param cim.v1.ModelComponent cmip5_component: CMIP5 model component.
    :param str cmip6_institution_id: CMIP6 institution identifier.
    :param str cmip6_source_id: CMIP6 source identifier.
    :param str cmip6_topic: CMIP6 model documentation topic.

    :returns: CMIP6 IPython notebook output.
    :rtype: dict

    """
    # Set output document to be seeded.
    doc = _get_document(cmip6_institution_id, cmip6_source_id, cmip6_topic)

    # Set seeding source.
    doc.seeding_source = 'cmip5:{}'.format(cmip5_model_id)

    # Set injected properties.
    _set_injected_properties(cmip6_topic, cmip5_component, doc)

    # Set specialized properties.
    if cmip6_topic != 'toplevel':
        _set_specialized_properties(cmip5_component, doc)

    # Sort values.
    doc.sort_values()

    return doc


def _get_document(institution_id, source_id, topic_id):
    """Returns output document.

    """
    # Set path to output file.
    fpath = os.getenv('ESDOC_HOME')
    fpath = os.path.join(fpath, 'repos/institutional')
    fpath = os.path.join(fpath, institution_id)
    fpath = os.path.join(fpath, 'cmip6/models')
    fpath = os.path.join(fpath, source_id)
    fpath = os.path.join(fpath, 'json')
    fpath = os.path.join(fpath, 'cmip6_{}_{}_{}.json'.format(institution_id, source_id, topic_id))

    # Ensure directory exists.
    if not os.path.isdir(os.path.dirname(fpath)):
        os.makedirs(os.path.dirname(fpath))

    # Remove previous.
    if os.path.exists(fpath):
        os.remove(fpath)

    # Set output wrapper.
    return NotebookOutput('cmip6', institution_id, source_id, topic_id, path=fpath, auto_save=False)


def _set_injected_properties(cmip6_topic, c, doc):
    """Maps properties injected by tooling chain.

    """
    # Topic overview.
    if c.description and len(c.description.strip()) > 0:
        spec_id = 'cmip6.{}.key_properties.overview'.format(cmip6_topic)
        doc.set_id(spec_id)
        doc.set_value(c.description)

    # Topic name.
    if c.long_name and len(c.long_name.strip()) > 0:
        spec_id = 'cmip6.{}.key_properties.name'.format(cmip6_topic)
        doc.set_id(spec_id)
        doc.set_value(c.long_name)

    # Escape if dealing with toplevel topic.
    if cmip6_topic == 'toplevel':
        return

    # Sub-topics.
    for c in [i for i in c.ext.component_tree if i.description and len(i.description.strip()) > 0]:
        # Get mapped CMIP6 identifier.
        try:
            mapped_identifier = mappings.get_cmip6_component_identifier(c)
        except KeyError:
            continue

        # Sub-topic overview.
        if c.description and len(c.description.strip()) > 0:
            spec_id = '{}.overview'.format(mapped_identifier)
            doc.set_id(spec_id)
            doc.set_value(str(c.description))

        # Sub-topic name (level 1 sub-topics only).
        if mapped_identifier.split('.') == 3:
            if c.long_name and len(c.long_name.strip()) > 0:
                spec_id = '{}.name'.format(mapped_identifier)
                doc.set_id(spec_id)
                doc.set_value(str(c.long_name))


def _set_specialized_properties(c, doc):
    """Maps properties defined within specializations.

    """
    for p, spec in mappings.get_cmip5_component_properties(c):
        vals = convertor.convert_property_values(p.values, spec)
        doc.set_id(spec.id)
        for val in vals:
            try:
                doc.set_value(val)
            except ValueError:
                pass
