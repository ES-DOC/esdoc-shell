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
    _log('Initialising CMIP6 model descriptions seeding config files:')
    for institution_id, obj in _get_data().items():
        fname = '{}.json'.format(institution_id)
        fpath = os.path.join(args.output_dir, fname)
        with open(fpath, 'w') as fstream:
            fstream.write(json.dumps(obj, indent=4))
        _log('... {} : initialised'.format(institution_id))


def _log(msg):
    """Log helper.

    """
    pyessv.log(msg, app='CMIP6')


def _get_data():
    """Gets data to be written to file system.

    """
    return collections.OrderedDict([(i, j) for i, j in _get_institutes().items() if j])


def _get_institutes():
    """Get map of institute to source identifier.

    """
    return collections.OrderedDict((i.canonical_name, _get_sources(i)) \
           for i in pyessv.load('wcrp:cmip6:institution-id'))


def _get_sources(institute):
    """Get map of source identifier to realm.

    """
    def _is_related(source):
        return institute.canonical_name in [i.lower() for i in source.data['institution_id']]

    return collections.OrderedDict([(i.canonical_name, _get_realms()) \
           for i in pyessv.load('wcrp:cmip6:source-id') if _is_related(i)])


def _get_realms():
    """Get map of realm to empty mapping.

    """
    return collections.OrderedDict((i.canonical_name, '') \
           for i in pyessv.load('wcrp:cmip6:realm'))


# Entry point.
_main(_ARGS.parse_args())
