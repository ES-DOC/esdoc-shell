# -*- coding: utf-8 -*-

"""
.. module:: defaults.py
   :license: GPL/CeCIL
   :platform: Unix, Windows
   :synopsis: CMIP6 default model configuration information.

.. moduleauthor:: Mark Conway-Greenslade <momipsl@ipsl.jussieu.fr>

"""
import collections
import json
import os

import pyessv

import mappings



# Nested map of institutes to source identifiers to realms.
_DEFAULTS = collections.defaultdict(dict)

# Name of file contiaing model defaults.
_FILENAME = 'model-defaults.json'


def init(institution_id):
    """Initialises seedings from institutional seeding config files.

    :param str institution_id: ID of institution being processed.

    """
    # Open model-defaults.json.
    fpath = _get_filepath(institution_id)
    try:
        with open(fpath, 'r') as fstream:
            obj = json.loads(fstream.read())
    except IOError:
        raise ValueError('Institute model defaults not found: {}'.format(institution_id))

    # Set defaults.
    _set_defaults(obj)


def _get_filepath(institution_id):
    """Returns path to an institite's model-defaults.json file.

    """
    fpath = os.getenv('ESDOC_HOME')
    fpath = os.path.join(fpath, 'repos')
    fpath = os.path.join(fpath, 'institutional')
    fpath = os.path.join(fpath, institution_id)
    fpath = os.path.join(fpath, 'cmip6')
    fpath = os.path.join(fpath, 'models')
    fpath = os.path.join(fpath, _FILENAME)

    return fpath


def _set_defaults(obj):
    """Caches model defaults.

    """
    for source_id in obj:
        for realm in obj[source_id]:
            initializedFrom = obj[source_id][realm]['initializedFrom']
            if initializedFrom and initializedFrom.split(':')[0] == 'cmip5':
                cmip5_model = initializedFrom.split(':')[-1]
                cmip5_component = mappings.COMPONENT_MAPPINGS.get(realm, realm)
                _DEFAULTS[cmip5_model][cmip5_component] = source_id


def get_source_id(m, c):
    """Returns a CMIP6 source identifier.

    :param str m: CMIP5 model identifier.
    :param str c: CMIP5 component identifier.

    :returns: A CMIP6 source identifier if found, else none.
    :rtype: str | None

    """
    cmip5_model = m.short_name.lower()
    cmip5_component = c.short_name.lower()
    try:
        return _DEFAULTS[cmip5_model][cmip5_component]
    except KeyError:
        pass
