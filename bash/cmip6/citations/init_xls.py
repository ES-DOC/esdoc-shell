# -*- coding: utf-8 -*-

"""
.. module:: init_xls.py
   :license: GPL/CeCIL
   :platform: Unix, Windows
   :synopsis: Initialises CMIP6 citation spreadsheets.

.. moduleauthor:: Mark Conway-Greenslade <momipsl@ipsl.jussieu.fr>

"""
import argparse
import os
import shutil

import pyessv

import _utils as utils



# Define command line argument parser.
_ARGS = argparse.ArgumentParser("Initialises CMIP6 model citation spreadsheets.")
_ARGS.add_argument(
    "--institution-id",
    help="An institution identifier",
    dest="institution_id",
    type=str,
    default="all"
    )
_ARGS.add_argument(
    "--xls-template",
    help="Path to XLS template",
    dest="xls_template",
    type=str
    )

# MIP era.
_MIP_ERA = "cmip6"


def _main(args):
    """Main entry point.

    """
    # Defensive programming.
    if not os.path.exists(args.xls_template):
        raise ValueError("XLS template file does not exist")

    # Set institutes to be processed.
    institutes = pyessv.WCRP.cmip6.institution_id if args.institution_id in {'', 'all'} else \
                 [pyessv.WCRP.cmip6.institution_id[args.institution_id]]

    # Write one file per CMIP6 institute.
    for i in institutes:
        fname = '{}_{}_citations.xlsx'.format(_MIP_ERA, i.canonical_name)
        dest = utils.get_folder_of_cmip6_institute(i, folder='citations')
        if not os.path.isdir(dest):
            os.makedirs(dest)
        dest = os.path.join(dest, fname)
        shutil.copy(args.xls_template, dest)


# Main entry point.
if __name__ == '__main__':
    _main(_ARGS.parse_args())
