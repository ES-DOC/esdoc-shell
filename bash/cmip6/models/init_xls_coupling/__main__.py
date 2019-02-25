# -*- coding: utf-8 -*-

"""
.. module:: generate_xls/__main__.py
   :license: GPL/CeCIL
   :platform: Unix, Windows
   :synopsis: Generates CMIP6 PDF documents.

.. moduleauthor:: Mark Conway-Greenslade <momipsl@ipsl.jussieu.fr>

"""
import argparse
import datetime as dt
import os

import xlsxwriter

import pyesdoc
import pyessv
from init_workbook import init as init_workbook
from write_couplings import write as write_couplings
from write_example import write as write_example
from write_frontis import write as write_frontis


# Define command line argument parser.
_ARGS = argparse.ArgumentParser("Generates CMIP6 model coupling XLS files.")
_ARGS.add_argument(
    "--institution-id",
    help="An institution identifier",
    dest="institution_id",
    type=str
    )

# MIP era.
_MIP_ERA = "cmip6"

# Generator version.
_VERSION = '1.0.0'


def _main(args):
    """Main entry point.

    """
    # Set institutes to be processed.
    institutes = pyessv.WCRP.cmip6.institution_id if args.institution_id == 'all' else \
                 [pyessv.WCRP.cmip6.institution_id[args.institution_id]]

    # Write an XLS file per CMIP6 institute | topic combination.
    # i = institute | s = source
    for i in institutes:
        for s in pyessv.WCRP.cmip6.get_institute_sources(i):
            ctx = ProcessingContext(i, s)
            ctx.write()


class ProcessingContext(object):
    """Wraps XLS workbook being generated.

    """
    def __init__(self, i, s):
        """Instance constructor.

        """
        self.institution_id = i.canonical_name
        self.realms = pyessv.WCRP.cmip6.get_source_realms(s)
        self.source_id = s.canonical_name
        self.wb = None
        self.ws = None
        self.ws_row = 0
        self.MIP_ERA = _MIP_ERA
        self.VERSION = _VERSION


    def write(self):
        """Write workbook.

        """
        for func in (
            init_workbook,
            write_frontis,
            write_example,
            write_couplings,
            ):
            func(self)

        self.wb.close()


    def create_format(self, font_size=12):
        """Returns a cell formatter.

        """
        f = self.wb.add_format()
        f.set_align('vcenter')
        f.set_font_name('Helvetica Neue')
        f.set_font_size(font_size)

        return f


# Entry point.
_main(_ARGS.parse_args())
