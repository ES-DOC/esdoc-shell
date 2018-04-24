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



# 5 member tuple: (cmip5-insititute, cmip5-model, cmip6-insititute, cmip6-source-id, cmip6-realm-id).
DEFAULTS = list()

# Model initialisation configuration filename.
_FILENAME = 'model-initialization.json'


def init(institution_id):
    """Initialises seedings from institutional seeding config files.

    :param str institution_id: ID of institution being processed.

    """
    # Open config file.
    fpath = _get_filepath(institution_id)
    try:
        with open(fpath, 'r') as fstream:
            obj = json.loads(fstream.read())
    except IOError:
        raise ValueError('Institute model defaults not found: {}: {}'.format(institution_id, fpath))

    # Set defaults.
    _set_defaults(institution_id, obj)


def _get_filepath(institution_id):
    """Returns path to an institite's model initialisation configuration file.

    """
    fpath = os.getenv('ESDOC_HOME')
    fpath = os.path.join(fpath, 'repos')
    fpath = os.path.join(fpath, 'institutional')
    fpath = os.path.join(fpath, institution_id)
    fpath = os.path.join(fpath, 'cmip6')
    fpath = os.path.join(fpath, 'models')
    fpath = os.path.join(fpath, _FILENAME)

    return fpath


def _set_defaults(institution_id, obj):
    """Caches model defaults.

    """
    for source_id in obj:
        for realm_id in obj[source_id]:
            initializedFrom = obj[source_id][realm_id]['initializedFrom']
            if not initializedFrom or initializedFrom.split(':')[0] != 'cmip5':
                break
            if len(initializedFrom.split(':')) == 3:
                cmip5_institute = initializedFrom.split(':')[-2]
                cmip5_model = initializedFrom.split(':')[-1]
            else:
                try:
                    cmip5_institute = mappings.INSTITUTE_MAPPINGS_REVERSED[institution_id]
                except KeyError:
                    cmip5_institute = institution_id
                cmip5_model = initializedFrom.split(':')[-1]

            DEFAULTS.append((cmip5_institute, cmip5_model, institution_id, source_id, realm_id))


def get_cmip5_institute_id():
    """Returns a CMIP5 institute identifier.

    """
    return _DEFAULTS.keys()[0]


def get_source_id(m, c):
    """Returns a CMIP6 source identifier.

    :param str m: CMIP5 model identifier.
    :param str c: CMIP5 component identifier.

    :returns: A CMIP6 source identifier if found, else none.
    :rtype: str | None

    """
    cmip5_institute = mappings.get_institute(m)
    cmip5_model = m.short_name.lower()
    cmip5_component = c.short_name.lower()
    try:
        return _DEFAULTS[cmip5_institute][cmip5_model][cmip5_component]
    except KeyError:
        pass
