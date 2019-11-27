# -*- coding: utf-8 -*-

"""
.. module:: generate_cim.py
   :license: GPL/CeCIL
   :platform: Unix, Windows
   :synopsis: Generates CMIP6 CIM documents from simplified JSON output.

.. moduleauthor:: Mark Conway-Greenslade <momipsl@ipsl.jussieu.fr>

"""
import argparse
import hashlib
import os
import shutil

import pyessv

import _utils as utils
from cmip6.utils import vocabs


# Define command line argument parser.
_ARGS = argparse.ArgumentParser("Synchronizes CMIP6 model CIM files between institutional repos & main archive.")
_ARGS.add_argument(
    "--institution-id",
    help="An institution identifier",
    dest="institution_id",
    type=str,
    default="all"
    )
_ARGS.add_argument(
    "--destination",
    help="Folder to which CIM documents will be copied.",
    dest="dest",
    type=str
    )

# MIP era.
_MIP_ERA = "cmip6"


def _main(args):
    """Main entry point.

    """
    institutes = vocabs.get_institutes(args.institution_id)
    for i in institutes:
        for s in vocabs.get_institute_sources(i):
            for src in _get_cim_files(i, s):
                fname = '{}.json'.format(hashlib.md5(src.split("/")[-1]).hexdigest())
                dest = os.path.join(args.dest, fname)
                shutil.copy(src, dest)


def _get_cim_files(i, s):
    """Returns CIM files to be copied to documentation archive.

    """
    folder = utils.get_folder_of_cmip6_source(i, s, 'cim')

    return [os.path.join(folder, i) for i in os.listdir(folder)]


# Main entry point.
if __name__ == '__main__':
    args = _ARGS.parse_args()
    if not os.path.exists(args.dest):
        raise ValueError("Destination folder is invalid")
    _main(args)
