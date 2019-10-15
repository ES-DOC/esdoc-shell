# -*- coding: utf-8 -*-

"""
.. module:: model_topic.py
   :license: GPL/CeCIL
   :platform: Unix, Windows
   :synopsis: Model topic notebook data wrapper.

.. moduleauthor:: Mark Conway-Greenslade <momipsl@ipsl.jussieu.fr>


"""
import os

import pyessv


# Home directory.
ESDOC_HOME = os.getenv('ESDOC_HOME')


def get_folder(parts):
    """Returns path to an institute's mip-era repository.

    """
    path = os.path.join(ESDOC_HOME, 'repos')
    path = os.path.join(path, 'institutional')

    for part in parts:
        if part is None:
            continue
        try:
            part.canonical_name
        except AttributeError:
            path = os.path.join(path, part)
        else:
            path = os.path.join(path, part.canonical_name)

    if not os.path.isdir(path):
        os.makedirs(path)

    return path


def get_citations_folder(i):
    """Returns path to an institute's citations directory.

    """
    return get_folder((i, 'cmip6', 'citations'))


def get_citations_spreadsheet(i):
    """Returns path to an institute's citations xls file.

    """
    fname = 'cmip6_{}_citations.xlsx'.format(i.canonical_name)
    path = get_citations_folder(i)

    return os.path.join(path, fname)


def get_citations_json(i):
    """Returns path to an institute's citations json file.

    """
    fname = 'cmip6_{}_citations.json'.format(i.canonical_name)
    path = get_citations_folder(i)
    path = os.path.join(path, 'json')

    return os.path.join(path, fname)


def get_institutes(institution_id):
    """Returns set of institutes to be processed.

    """
    return pyessv.WCRP.cmip6.institution_id if institution_id == 'all' else \
           [pyessv.WCRP.cmip6.institution_id[institution_id]]


def get_parties_folder(i):
    """Returns path to an institute's responsible parties directory.

    """
    return get_folder((i, 'cmip6', 'responsible_parties'))


def get_parties_spreadsheet(i):
    """Returns path to an institute's responsible parties xls file.

    """
    fname = 'cmip6_{}_responsible_parties.xlsx'.format(i.canonical_name)
    path = get_parties_folder(i)

    return os.path.join(path, fname)


def get_parties_json(i):
    """Returns path to an institute's responsible parties json file.

    """
    fname = 'cmip6_{}_responsible_parties.json'.format(i.canonical_name)
    path = get_parties_folder(i)
    path = os.path.join(path, 'json')

    return os.path.join(path, fname)
