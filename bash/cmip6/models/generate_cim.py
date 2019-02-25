# -*- coding: utf-8 -*-

"""
.. module:: generate_cim.py
   :license: GPL/CeCIL
   :platform: Unix, Windows
   :synopsis: Generates CMIP6 CIM documents from simplified JSON output.

.. moduleauthor:: Mark Conway-Greenslade <momipsl@ipsl.jussieu.fr>

"""
import argparse
import json
import os

import pyesdoc
import pyessv

from pyesdoc.ontologies.cim import v2 as cim

import _utils as utils



# Define command line argument parser.
_ARGS = argparse.ArgumentParser("Generates CMIP6 model CIM files.")
_ARGS.add_argument(
    "--institution-id",
    help="An institution identifier",
    dest="institution_id",
    type=str
    )

# MIP era.
_MIP_ERA = "cmip6"

# Set of properties injected by machinery.
_INJECTED_PROPERTIES = {'Name', 'Overview', 'Keywords'}


def _main(args):
    """Main entry point.

    """
    # Set institutes to be processed.
    institutes = pyessv.WCRP.cmip6.institution_id if args.institution_id == 'all' else \
                 [pyessv.WCRP.cmip6.institution_id[args.institution_id]]

    # Write a CIM file per CMIP6 institute | source combination.
    # i = institute | s = source
    for i in institutes:
        for s in pyessv.WCRP.cmip6.get_institute_sources(i):
            _sync_fs(i, s)


def _sync_fs(i, s):
    """Syncs an institute's model documentation upon the file system.
    This results in either an updated document or a deleted document.

    """
    # Get file path & content.
    path = _get_cim_fpath(i, s)
    content = _get_content(i, s)

    # Delete if content is null.
    if content is None:
        if os.path.exists(path):
            pyessv.log('deleting --> {}'.format(path.split('/')[-1]), app='SH')
            os.remove(path)

    # Write otherwise.
    else:
        pyessv.log('writing --> {}'.format(path.split('/')[-1]), app='SH')
        with open(path, 'w') as fstream:
            fstream.write(content)


def _get_content(i, s):
    """Generates a CIM document for a CMIP6 institute | source combination.

    """
    doc = _map_model(i, s, _get_data_accessors(i, s))
    if doc is None:
        return

    # Destructure injected properties.
    _destructure(doc)

    # Emit validation report.
    errors = pyesdoc.validate(doc)
    errors = [e for e in errors if
              e.endswith('values --> is an empty list') == False]
    if errors:
        print "INVALID CIM DOCUMENT:", s
        for err in errors:
            print err

    # Return JSON string.
    return pyesdoc.encode(doc)


def _get_data_accessors(i, s):
    """Returns a collection of model spreadsheet output accessors - one per spreadsheet.

    """
    accessors = [utils.ModelTopicOutput.create(_MIP_ERA, i, s, t) \
                 for t in pyessv.ESDOC.cmip6.get_model_topics(s)]

    return [a for a in accessors if a.content]


def _get_cim_fpath(i, s):
    """Returns file path of CIM document to be written to file system.

    """
    path = utils.get_folder_of_cmip6_source(i, s, 'cim')
    fname = utils.get_file_of_cmip6(i, s, None, 'json')

    return os.path.join(path, fname)


def _destructure_injected(container, doc, accessor):
    """Destructures properties injected by the machinery but which can be directly assigned to CIM type instances.

    """
    # Escape if the container was empty.
    if container is None:
        return

    # Set injected.
    injected = [i for i in container.properties if i.name in _INJECTED_PROPERTIES]

    # Assign to CIM type instance.
    for p in injected:
        if p.name == 'Name':
            doc.long_name = accessor.get_value(p.specialization_id)
        elif p.name == 'Overview':
            doc.description = accessor.get_value(p.specialization_id)
        elif p.name == 'Keywords':
            doc.keywords = accessor.get_comma_delimited_values(p.specialization_id)

    # Update container.
    container.properties = [i for i in container.properties if i not in injected]


def _destructure(model):
    """Destructures properties injected by the machinery but which can be directly assigned to CIM type instances.

    """
    if model.key_properties:
        for p in [i for i in model.key_properties.properties if i.values]:
            if p.name == 'Name':
                model.long_name = p.values[0]
            elif p.name == 'Overview':
                model.description = p.values[0]
            elif p.name == 'Keywords':
                model.keywords = [i.strip() for i in p.values[0].split(',')]


def _map_model(i, s, accessors):
    """Returns a mapped model CIM document.

    """
    m = pyesdoc.create(cim.Model, project='CMIP6', source='spreadsheet', version=1, institute=i.canonical_name)
    m.activity_properties = _map_model_activity_properties(accessors) or []
    m.canonical_id = s.canonical_name
    m.key_properties = _map_model_key_properties(accessors)
    m.model_type = 'GCM'
    m.name = s.canonical_name.upper()
    m.realms = _map_realms(accessors)

    return m if (m.activity_properties or m.key_properties or m.realms) else None


def _map_model_activity_properties(accessors):
    """Maps a specialization to model activity properties.

    """
    for accessor in accessors:
        if accessor.specialization.id.endswith('toplevel'):
            return _map_topics(accessor.specialization['process'], accessor)


def _map_model_key_properties(accessors):
    """Maps a specialization to model key properties.

    """
    for accessor in accessors:
        if accessor.specialization.id.endswith('toplevel'):
            return _map_topic(accessor.specialization['keyprops'], accessor)


def _map_realms(accessors):
    """Maps specializations to realms.

    """
    accessors = [i for i in accessors if not i.specialization.id.endswith('toplevel')]
    result = [_map_realm(i.specialization, i) for i in accessors]

    return [i for i in result if i is not None]


def _map_realm(specialization, accessor):
    """Maps a specialization to a realm.

    """
    r = pyesdoc.create(cim.Realm, project='CMIP6', source='spreadsheet', version=1)
    r.description = specialization.description or specialization.name_camel_case_spaced
    r.name = specialization.name_camel_case_spaced
    r.specialization_id = specialization.id
    r.key_properties = _map_topic(specialization['keyprops'], accessor)
    r.grid = _map_topic(specialization['grid'], accessor)
    r.processes = _map_topics(specialization['process'], accessor)

    return r if (r.key_properties or r.grid or r.processes) else None


def _map_topic(specialization, accessor):
    """Maps a specialization to a topic.

    """
    if specialization is None:
        return
    t = _instantiate(specialization, cim.Topic)
    t.properties = _map_properties(specialization.properties, accessor)
    t.property_sets = _map_property_sets(specialization.property_sets, accessor)
    t.sub_topics = _map_topics(specialization.sub_topics, accessor)

    return t if (t.properties or t.property_sets or t.sub_topics) else None


def _map_topics(specializations, accessor):
    """Maps specializations to topics.

    """
    result = [_map_topic(i, accessor) for i in specializations]

    return [i for i in result if i is not None]


def _map_properties(specializations, accessor):
    """Maps specializations to properties.

    """
    result = [_map_property(i, accessor) for i in specializations]

    return [i for i in result if i is not None]


def _map_property(specialization, accessor):
    """Maps a specialization to a property.

    """
    tp = _instantiate(specialization, cim.TopicProperty)
    tp.values = accessor.get_values(specialization.id)
    tp.values = [i for i in tp.values if i is not None]
    tp.values = [i if isinstance(i, (str, unicode)) else unicode(i) for i in tp.values]

    return tp
    return tp if tp.values else None


def _map_property_set(specialization, accessor):
    """Maps a specialization to a property set.

    """
    tps = _instantiate(specialization, cim.TopicPropertySet)
    tps.properties = [_map_property(i, accessor) for i in specialization.properties]
    tps.properties = [i for i in tps.properties if i is not None]

    return tps if tps.properties else None


def _map_property_sets(specializations, accessor):
    """Maps specializations to property sets.

    """
    result = [_map_property_set(i, accessor) for i in specializations]

    return [i for i in result if i is not None]


def _instantiate(specialization, cim_type):
    """Instantiates a CIM type instance.

    """
    instance = cim_type()
    instance.description = specialization.description or specialization.name_camel_case_spaced
    instance.name = specialization.name_camel_case_spaced
    instance.specialization_id = specialization.id

    return instance


# Main entry point.
if __name__ == '__main__':
    _main(_ARGS.parse_args())
