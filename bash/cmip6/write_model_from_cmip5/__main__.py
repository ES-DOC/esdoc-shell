# -*- coding: utf-8 -*-

"""
.. module:: write_model_notebooks.py
   :license: GPL/CeCIL
   :platform: Unix, Windows
   :synopsis: Writes CMIP6 IPython model notebooks to file system.

.. moduleauthor:: Mark Conway-Greenslade <momipsl@ipsl.jussieu.fr>

"""
import argparse
import collections
import datetime as dt
import json
import os

from tornado import template

import pyesdoc
from pyesdoc.ontologies import cim

import mapper



# Command line options.
_ARGS = argparse.ArgumentParser("Writes CMIP5 model documents in CIM v2 format.")
_ARGS.add_argument(
    "--output",
    help="Path to a directory into which notebooks will be written.",
    dest="output_dir",
    type=str
    )
_ARGS = _ARGS.parse_args()

_FPATH = "/Users/macg/dev/esdoc/repos/esdoc-archive/esdoc/cmip5/Metafor CMIP5 Questionnaire/cim.2.json"


# Map of CMIP5 to CMIP6 role codes.
_ROLE_CODES = {
    "pi": "Principal Investigator",
    "funder": "sponsor",
    "contact": "point of contact",
    "centre": "custodian"
}


# Validate inputs.
if not os.path.isdir(_ARGS.output_dir):
    raise ValueError("Output directory does not exist")

# Initialise.
pyesdoc.archive.init()
mapper.init()

for i in pyesdoc.archive.yield_latest_documents("cmip5", "metafor-q", "cim-1-software-modelcomponent"):
    with open(_FPATH, "w") as fstream:
        fstream.write(pyesdoc.encode(mapper.map_model(i)))
    break
