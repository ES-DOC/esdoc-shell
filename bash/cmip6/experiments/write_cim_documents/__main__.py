# -*- coding: utf-8 -*-

"""
.. module:: write_experiments.py
   :license: GPL/CeCIL
   :platform: Unix, Windows
   :synopsis: Writes CMIP6 experiments to file system.

.. moduleauthor:: Mark Conway-Greenslade <momipsl@ipsl.jussieu.fr>

"""
import argparse
import os

import pyesdoc

from cv import validate_vocabularies
from convertors import UNCONVERTED_NAMES
from document_identifiers import DocumentIdentifiers
from document_set import DocumentSet
from xl import Spreadsheet
from xl_mappings import WS_EXPERIMENT
from xl_mappings import WS_PROJECT



# Define command line options.
_ARGS = argparse.ArgumentParser("Extracts CIM v2 documents from CMIP6 experiment spreadsheet.")
_ARGS.add_argument(
    "--io-dir",
    help="Path to a directory into which documents will be written.",
    dest="io_dir",
    type=str
    )
_ARGS.add_argument(
    "--spreadsheet",
    help="Path to the CMIP6 experiments worksheet.",
    dest="spreadsheet_filepath",
    type=str
    )
_ARGS.add_argument(
    "--identifiers",
    help="Path to set of CMIP6 experiments document identifiers.",
    dest="identifiers",
    type=str
    )
_ARGS = _ARGS.parse_args()


# Validate command line options.
if not os.path.isfile(_ARGS.spreadsheet_filepath):
    raise ValueError("Spreadsheet file does not exist")
if not os.path.isdir(_ARGS.io_dir):
    raise ValueError("Archive directory does not exist: {}".format(_ARGS.io_dir))

# Initialise pyesdoc.
pyesdoc.drq.initialize()

# Create document identifier mappings.
identifiers = DocumentIdentifiers(_ARGS.identifiers)

# Open spreadsheet accessor.
xl = Spreadsheet(_ARGS.spreadsheet_filepath, identifiers)

# Create document set.
docs = DocumentSet(xl)

# Filter out ignoreable documents.
docs.ignore_documents()

# Set intra-document mesh.
docs.set_document_connections()

# Emit set of unconverted names.
for collection_type, names in UNCONVERTED_NAMES.items():
    print "------------------------------------------------------"
    print "INVALID CELL REFERENCES: {} ".format(collection_type)
    print sorted(list(names))
    print "------------------------------------------------------"

# Create intra-document links.
docs.set_document_links()

# Write documents to file system.
docs.write(_ARGS.io_dir)

# Write vocab validation report.
validate_vocabularies(docs[WS_PROJECT], docs[WS_EXPERIMENT])
