# -*- coding: utf-8 -*-

"""
.. module:: write_seeding_config.__main__.py
   :license: GPL/CeCIL
   :platform: Unix, Windows
   :synopsis: Initializes CMIP6 seeding configuration files.

.. moduleauthor:: Mark Conway-Greenslade <momipsl@ipsl.jussieu.fr>

"""
import collections
import json
import os

import pyessv



# Output directory.
_OUTPUT_DIR = os.getenv('ESDOC_HOME')
_OUTPUT_DIR = os.path.join(_OUTPUT_DIR, 'repos')
_OUTPUT_DIR = os.path.join(_OUTPUT_DIR, 'esdoc-docs')
_OUTPUT_DIR = os.path.join(_OUTPUT_DIR, 'cmip6')
_OUTPUT_DIR = os.path.join(_OUTPUT_DIR, 'models')
_OUTPUT_DIR = os.path.join(_OUTPUT_DIR, 'seeding')


def _main():
    """Main entry point.

    """
    _log('Initialising CMIP6 model descriptions seeding config files:')
    for institution_id, obj in _get_data().items():
        fname = '{}.json'.format(institution_id)
        fpath = os.path.join(_OUTPUT_DIR, fname)
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

    return collections.OrderedDict([(i.canonical_name, _get_realms(i)) \
           for i in pyessv.load('wcrp:cmip6:source-id') if _is_related(i)])


def _get_realms(source_id):
    """Get map of realm to empty mapping.

    """
    def _is_realized(realm):
        return source_id.data['model_component'][realm.raw_name]['description'] != 'none'

    return collections.OrderedDict((i.canonical_name, _get_realm(source_id, i)) \
           for i in pyessv.load('wcrp:cmip6:realm') if _is_realized(i))


def _get_realm(source_id, realm):
    """Maps a realm to a dictionary.

    """
    obj = collections.OrderedDict()
    obj['initializedFrom'] = ''
    obj['name'] = ''

    return obj


# Entry point.
_main()