# -*- coding: utf-8 -*-

"""
.. module:: mapper.py
   :license: GPL/CeCIL
   :platform: Unix, Windows
   :synopsis: Maps CMIP5 CIM (v1) model documents to lightweight IPython format.

.. moduleauthor:: Mark Conway-Greenslade <momipsl@ipsl.jussieu.fr>

"""
import os

import convertor
import defaults
import mappings
from _utils import ModelTopicOutput


class MappingInfo(object):
    """Encapsulates information to be mapped.

    """
    def __init__(self, cmip5_model_id, cmip5_component, cmip6_institution_id, cmip6_source_id, cmip6_topic):
        """Ctor.

        """
        self.cmip5_model_id = cmip5_model_id
        self.cmip5_component = cmip5_component
        self.cmip6_institution_id = cmip6_institution_id
        self.cmip6_source_id = cmip6_source_id
        self.cmip6_topic = cmip6_topic


def map(mapping_info):
    """Maps a CMIP5 model component to a CMIP6 simplified output.

    :param MappingInfo mapping_info: Information to be mapped.

    :returns: CMIP6 simplified model document output.
    :rtype: dict

    """
    # Deconstruct mapping information.
    cmip5_model_id = mapping_info.cmip5_model_id
    cmip5_component = mapping_info.cmip5_component
    cmip6_institution_id = mapping_info.cmip6_institution_id
    cmip6_source_id = mapping_info.cmip6_source_id
    cmip6_topic = mapping_info.cmip6_topic

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
    if not os.path.isdir(fpath):
        os.makedirs(fpath)
    fpath = os.path.join(fpath, 'cmip6_{}_{}_{}.json'.format(institution_id, source_id, topic_id))

    # Remove previous ?.
    if os.path.exists(fpath):
        os.remove(fpath)

    # Set output wrapper.
    return ModelTopicOutput('cmip6', institution_id, source_id, topic_id, path=fpath)


def _set_injected_properties(cmip6_topic, c, doc):
    """Maps properties injected by tooling chain.

    Note: c = cmip5_component

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
    for c in [i for i in c.ext.component_tree
              if i.description and len(i.description.strip()) > 0]:
        # Get mapped CMIP6 identifier.
        try:
            mapped_identifier = mappings.get_cmip6_component_identifier(c)
        except KeyError:
            continue

        # Skip sub-processes
        if len(mapped_identifier.split('.')) > 3:
            continue

        # Sub-topic overview.
        if c.description and len(c.description.strip()) > 0:
            spec_id = '{}.overview'.format(mapped_identifier)
            doc.set_id(spec_id)
            doc.set_value(c.description, str)

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
