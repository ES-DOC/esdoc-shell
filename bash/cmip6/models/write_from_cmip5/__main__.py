# -*- coding: utf-8 -*-

"""
.. module:: write_model_notebooks.py
   :license: GPL/CeCIL
   :platform: Unix, Windows
   :synopsis: Writes CMIP6 IPython model notebooks to file system.

.. moduleauthor:: Mark Conway-Greenslade <momipsl@ipsl.jussieu.fr>

"""
import argparse
import os

import pyessv
from pyesdoc import archive


import mappings
import seedings
from mappers import get_mapper
from writers import get_writer



# Command line options.
_ARGS = argparse.ArgumentParser("Maps CMIP5 model documents for use in CMIP6.")
_ARGS.add_argument(
    "--encoding",
    help="Format to which mapped documents will be written.",
    dest="encoding",
    type=str,
    choices=['cim', 'ipython']
    )
_ARGS.add_argument(
    "--output",
    help="Path to a directory into which CIM v2 documents will be written.",
    dest="output_dir",
    type=str
    )
_ARGS.add_argument(
    "--seeding",
    help="Path within which are to be found seeding files.",
    dest="seeding_dir",
    type=str
    )
_ARGS = _ARGS.parse_args()

# Validate inputs.
if not os.path.isdir(_ARGS.output_dir):
    raise ValueError("Output directory is invalid")
if not os.path.isdir(_ARGS.seeding_dir):
    raise ValueError("Seeding directory is invalid")


def init():
    """Initialisation.

    """
    archive.init()
    mappings.init()
    seedings.init(_ARGS.seeding_dir)


def yield_model():
    """Yields mappable CMIP5 model documents.

    """
    for m in archive.yield_latest_documents("cmip5", "metafor-q", "cim-1-software-modelcomponent"):
        yield m


def yield_model_components():
    """Yields mappable CMIP5 model components.

    """
    for m in yield_model():
        for c in m.sub_components:
            if seedings.get_source_id(m, c):
                yield (m, c)


# Map of encodings to yielders.
_YIELDERS = {
    'cim': yield_model,
    'ipython': yield_model_components
}

# Initialise sub-packages.
init()

# Set mapper / writer / factory.
mapper = get_mapper(_ARGS.encoding)
writer = get_writer(_ARGS.encoding)
yielder = _YIELDERS[_ARGS.encoding]

# Process mapped documents.
pyessv.log('Processing archived model documentation:', app='CMIP6')
for documentation in yielder():
    writer.write(mapper.map(documentation), _ARGS.output_dir)
