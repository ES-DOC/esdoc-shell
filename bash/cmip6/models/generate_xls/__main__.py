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
from _utils import ModelTopicOutput
from cmip6.utils import vocabs
from write_citations_and_parties import write as write_citations_and_parties
from write_frontis import write as write_frontis
from write_property_value import write as write_property_value
from write_property import write as write_property
from write_propertyset import write as write_propertyset
from write_subtopic import write as write_subtopic
from write_topic import write as write_topic



# Define command line argument parser.
_ARGS = argparse.ArgumentParser("Generates CMIP6 model XLS files.")
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
    institutes = vocabs.get_institutes(args.institution_id)
    for i in institutes:
        for s in vocabs.get_institute_sources(i):
            for t in pyessv.ESDOC.cmip6.get_model_topics(s):
                xl = Spreadsheet(i, s, t)
                xl.write()


class Spreadsheet(object):
    """Wraps XLS workbook being generated.

    """
    def __init__(self, i, s, t):
        """Instance constructor.

        """
        self.doc = ModelTopicOutput.create(_MIP_ERA, i, s, t)
        self.institution_id = i.canonical_name
        self.t = self.doc.specialization
        self.topic_label = t.label
        self.topic_id = t.canonical_name
        self.p = None
        self.ps = None
        self.p_values = []
        self.source_id = s.canonical_name
        self.st = None
        self.wb = None
        self.ws = None
        self.ws_row = 0
        self.MIP_ERA = _MIP_ERA
        self.VERSION = _VERSION


    def write(self):
        """Write workbook.

        """
        self.set_identifiers()

        write_topic(self)
        write_frontis(self)
        write_citations_and_parties(self)

        for st in self.t.sub_topics:
            self.st = st
            self.ps = None
            self.p = None
            self.p_values = []
            write_subtopic(self)

            for ps in st.all_property_containers:
                self.ps = ps
                self.p = None
                self.p_values = []
                write_propertyset(self)

                for p in ps.properties:
                    self.p = p
                    self.p_values = [] if p is None else self.doc.get_values(p.id)
                    write_property(self)
                    write_property_value(self)

        self.wb.close()


    def set_identifiers(self):
        """Initialises property & property set identifiers.

        """
        idx1 = 0
        for pc in self.t.all_property_containers:
            level = len(pc.id.split('.'))
            if level == 3:
                idx1 += 1
                idx2 = 1
                idx3 = 1
            elif level == 4:
                idx2 += 1
                idx3 = 1
            elif level == 5:
                idx3 += 1
            pc.idx = '{}.{}.{}'.format(idx1, idx2, idx3)
            for idx, p in enumerate(pc.properties):
                p.idx = '{}.{}'.format(pc.idx, idx + 1)


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
