# -*- coding: utf-8 -*-

"""
.. module:: write_model_notebooks.py
   :license: GPL/CeCIL
   :platform: Unix, Windows
   :synopsis: Writes CMIP6 IPython model notebooks to file system.

.. moduleauthor:: Mark Conway-Greenslade <momipsl@ipsl.jussieu.fr>

"""
import argparse

import pyesdoc
import pyessv

import defaults
import mappings
import mapper


# All institute filter.
_ALL_INSTITUTES = 'all'

# Define command line options.
_ARGS = argparse.ArgumentParser("Maps CMIP5 model documents to CMIP6 IPython notebook output.")
_ARGS.add_argument(
    "--institute",
    help="CMIP5 institute identier (* for all).",
    dest="institute",
    type=str
    )
_ARGS = _ARGS.parse_args()


def _yield_model(institute):
    """Yields mappable CMIP5 model documents.

    """
    for m in pyesdoc.archive.yield_latest_documents("cmip5", "metafor-q", "cim-1-software-modelcomponent"):
        if institute == _ALL_INSTITUTES or institute == m.meta.institute.lower():
            yield m


def _yield_model_components(institute):
    """Yields mappable CMIP5 model components.

    """
    for m in _yield_model(institute):
        for c in m.sub_components:
            if defaults.get_source_id(m, c):
                yield (m, c)


def _yield_notebook_outputs(institute):
    """Yields CMIP6 notebook outputs.

    """
    for docs in _yield_model_components(institute):
        yield mapper.map(docs)


# Initialise sub-modules.
pyesdoc.archive.init()
mappings.init()
defaults.init()

# Process mapped documents.
pyessv.log('Processing archived model documentation:', app='CMIP6')
for nb_output in _yield_notebook_outputs(_ARGS.institute.lower()):
    nb_output.save()
    pyessv.log(nb_output.fpath, app='CMIP6')
