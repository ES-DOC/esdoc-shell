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
DEFAULTS = None

# Model initialisation from CMIP5 settings filename.
_SETTINGS_FNAME = 'initialization_from_CMIP5.json'


def init(institution_id):
    """Initialises seedings from institutional seeding config files.

    :param str institution_id: ID of institution being processed.

    """
    # Open settings.
    settings = _get_settings(institution_id)

    # Set defaults.
    _set_defaults(institution_id, settings)


def _get_settings(institution_id):
    """Returns initialization from CMIP5 settings.

    """
    # Set path.
    fpath = os.getenv('ESDOC_HOME')
    fpath = os.path.join(fpath, 'repos')
    fpath = os.path.join(fpath, 'institutional')
    fpath = os.path.join(fpath, institution_id)
    fpath = os.path.join(fpath, 'cmip6')
    fpath = os.path.join(fpath, 'models')
    fpath = os.path.join(fpath, _SETTINGS_FNAME)

    # Read JSON.
    try:
        with open(fpath, 'r') as fstream:
            return json.loads(fstream.read())
    except IOError:
        raise ValueError('Institute initialization from CMIP5 settings not found: {}: {}'.format(institution_id, fpath))


def _set_defaults(institution_id, settings):
    """Caches model defaults.

    """
    # Reset.
    global DEFAULTS
    DEFAULTS = list()

    for source_id in settings:
        for realm_id in settings[source_id]:
            initializedFrom = settings[source_id][realm_id]['initializedFrom']
            if not initializedFrom or initializedFrom.split(':')[0] != 'cmip5':
                continue
            if len(initializedFrom.split(':')) == 3:
                cmip5_institute = initializedFrom.split(':')[-2]
                cmip5_model = initializedFrom.split(':')[-1]
            else:
                try:
                    cmip5_institute = mappings.INSTITUTE_MAPPINGS_REVERSED[institution_id]
                except KeyError:
                    cmip5_institute = institution_id
                cmip5_model = initializedFrom.split(':')[-1]

            DEFAULTS.append((cmip5_institute.lower(), cmip5_model.lower(), institution_id, source_id, realm_id))


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
