# -*- coding: utf-8 -*-

"""
.. module:: generate_config.py
   :license: GPL/CeCIL
   :platform: Unix, Windows
   :synopsis: Generates CMIP5 CIM (v1) model documents to CMIP6 CIM (v2) mapping config file.

.. moduleauthor:: Mark Conway-Greenslade <momipsl@ipsl.jussieu.fr>

"""
import argparse
import collections
import json
import os

import pyessv



# Define command line options.
_ARGS = argparse.ArgumentParser("Writes CMIP6 model seeding config files.")
_ARGS.add_argument(
    "--output",
    help="Path to directory into which seeding config files will be written.",
    dest="output_dir",
    type=str
    )


def _main(args):
    """Main entry point.

    """
    pyessv.log('Initialising CMIP6 model descriptions seeding config files:', app='CMIP6')

    data = _map_institutes()
    for institution_id, obj in data.items():
        fname = '{}.json'.format(institution_id)
        fpath = os.path.join(args.output_dir, fname)
        with open(fpath, 'w') as fstream:
            fstream.write(json.dumps(obj, indent=4))
        pyessv.log('... {} : initialised'.format(institution_id), app='CMIP6')


def _map_institutes():
    """Maps institutes collection to a dictionary.

    """
    obj = collections.OrderedDict()
    for institute in pyessv.load('wcrp:cmip6:institution-id'):
        obj[institute.canonical_name] = _map_institute(institute)

    return collections.OrderedDict([(i, j) for i, j in obj.items() if j])


def _map_institute(institute):
    """Maps an institute to a dictionary.

    """
    def _is_related(source):
        return institute.canonical_name in [i.lower() for i in source.data['institution_id']]

    obj = collections.OrderedDict()
    for source_id in pyessv.load('wcrp:cmip6:source-id'):
        if not _is_related(source_id):
            continue
        obj[source_id.canonical_name] = _map_source_id(source_id)

    return obj


def _map_source_id(source_id):
    """Maps a source identifier to a dictionary.

    """
    obj = collections.OrderedDict()
    for realm in pyessv.load('wcrp:cmip6:realm'):
        if source_id.raw_data['modelComponent'][realm.raw_name]['description'] != 'none':
            obj[realm.canonical_name] = _map_realm(source_id, realm)

    return obj


def _map_realm(source_id, realm):
    """Maps a realm to a dictionary.

    """
    obj = collections.OrderedDict()
    obj['initializedFrom'] = ''
    obj['name'] = ''

    return obj


def _get_realms():
    """Get map of realm to empty mapping.

    """
    return collections.OrderedDict((i.canonical_name, '') \
           for i in pyessv.load('wcrp:cmip6:realm'))


# Entry point.
_main(_ARGS.parse_args())
