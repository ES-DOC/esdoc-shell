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



# Define command line argument parser.
_ARGS = argparse.ArgumentParser("Initializes a CMIP6 model output JSON file.")
_ARGS.add_argument(
    "--institution-id",
    help="An institution identifier",
    dest="institution_id",
    type=str
    )


def _main(args):
    """Main entry point.

    """
    # Initialise sub-modules.
    pyessv.log('Initializing sub-modules ...', app='JHUB')
    pyesdoc.archive.init()
    mappings.init()
    defaults.init(args.institution_id)

    # Process mapped documents.
    pyessv.log('Processing archived CMIP5 model documentation ...', app='JHUB')
    for nb_output in _yield_notebook_outputs(args.institution_id):
        nb_output.save()
        pyessv.log(nb_output.fpath, app='JHUB')


def _yield_notebook_outputs(institution_id):
    """Yields CMIP6 notebook outputs.

    """
    for docs in _yield_model_components(institution_id):
        yield mapper.map(docs)


def _yield_model_components(institution_id):
    """Yields mappable CMIP5 model components.

        """
    for m in _yield_model(institution_id):
        for c in m.sub_components:
            if defaults.get_source_id(m, c):
                yield (m, c)


def _yield_model(institution_id):
    """Yields mappable CMIP5 model documents.

    """
    for m in pyesdoc.archive.yield_latest_documents("cmip5", "metafor-q", "cim-1-software-modelcomponent"):
        if mappings.get_institute(m) == institution_id:
            yield m


_main(_ARGS.parse_args())
