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



# Define command line argument parser.
_ARGS = argparse.ArgumentParser("Resets CMIP6 model JSON files.")
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
    # Set institutes to be processed.
    institutes = pyessv.WCRP.cmip6.institution_id if args.institution_id == 'all' else \
                 [pyessv.WCRP.cmip6.institution_id[args.institution_id]]

    # Reset JSON folder for each CMIP6 institute | source combination.
    # i = institute | s = source
    for i in institutes:
        for s in pyessv.WCRP.cmip6.get_institute_sources(i):
            folder = utils.get_folder_of_cmip6_source(i, s, 'json')
            shutil.rmtree(folder)
            os.makedirs(folder)


# Main entry point.
if __name__ == '__main__':
    _main(_ARGS.parse_args())
