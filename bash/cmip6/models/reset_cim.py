# -*- coding: utf-8 -*-

"""
.. module:: init_citation_xls.py
   :license: GPL/CeCIL
   :platform: Unix, Windows
   :synopsis: Initialises CMIP6 model citation spreadsheets.

.. moduleauthor:: Mark Conway-Greenslade <momipsl@ipsl.jussieu.fr>

"""
import argparse
import os
import shutil

import pyessv

import _utils as utils
from cmip6.utils import vocabs



# Define command line argument parser.
_ARGS = argparse.ArgumentParser("Resets CMIP6 model CIM files.")
_ARGS.add_argument(
    "--institution-id",
    help="An institution identifier",
    dest="institution_id",
    type=str,
    default="all"
    )

def _main(args):
    """Main entry point.

    """
    institutes = vocabs.get_institutes(args.institution_id)
    for i in institutes:
        for s in vocabs.get_institute_sources(i):
            folder = utils.get_folder_of_cmip6_source(i, s, 'cim')
            shutil.rmtree(folder)
            os.makedirs(folder)


# Main entry point.
if __name__ == '__main__':
    _main(_ARGS.parse_args())
