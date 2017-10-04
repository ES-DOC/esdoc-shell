# -*- coding: utf-8 -*-

"""
.. module:: mappings.py
   :license: GPL/CeCIL
   :platform: Unix, Windows
   :synopsis: CMIP5 to CMIP6 vocab mapping utility functions.

.. moduleauthor:: Mark Conway-Greenslade <momipsl@ipsl.jussieu.fr>

"""
import collections
import json
import os

import pyessv

import mappings



# Nested map of institutes to source identifiers to realms.
_SEEDINGS = collections.defaultdict(lambda: collections.defaultdict(dict))


def init(seeding_dir):
    """Initialises seedings from institutional seeding config files.

    :param str seeding_dir: Directory within which seedings are found.

    """
    # Load seedings from institutional configuration files.
    for institute_id in [i.canonical_name for i in pyessv.load('wcrp:cmip6:institution-id')]:
        # ... set file path.
        fname = '{}.json'.format(institute_id)
        fpath = os.path.join(seeding_dir, fname)
        if not os.path.isfile(fpath):
            continue

        # ... open file.
        with open(fpath, 'r') as fstream:
            obj = json.loads(fstream.read())

        # ... set seedings.
        for source_id, seedings in obj.items():
            for realm, cmip5_model in [(i, j.split(':')[1]) for i, j in seedings.items() if j and j.startswith('cmip5')]:
                cmip5_component = mappings.COMPONENT_MAPPINGS.get(realm, realm)
                _SEEDINGS[institute_id][cmip5_model][cmip5_component] = source_id


def get_source_id(m, c):
    """Returns a CMIP6 source identifier.

    :param str cmip5_model: CMIP5 model identifier.
    :param str cmip5_component: CMIP5 component identifier.

    :returns: A CMIP6 source identifier if found, else none.
    :rtype: str | None

    """
    institute_id = mappings.get_institute(m)
    cmip5_model = m.short_name.lower()
    cmip5_component = c.short_name.lower()
    try:
        return _SEEDINGS[institute_id][cmip5_model][cmip5_component]
    except KeyError:
        pass
