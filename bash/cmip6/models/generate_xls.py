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
from pyesdoc.ipython.model_topic import NotebookOutput

# Changes
# 1. Hide speciality ID col.
# 2. citations & resp.party references



# Define command line argument parser.
_ARGS = argparse.ArgumentParser("Generates an institute's CMIP6 model XLS files.")
_ARGS.add_argument(
    "--institution-id",
    help="An institution identifier",
    dest="institution_id",
    type=str
    )

# MIP era.
_MIP_ERA = "cmip6"

# Set of test instiutes.
_TEST_INSTITUTES = {'test-institute-1', 'test-institute-2', 'test-institute-3'}



def _main(args):
    """Main entry point.

    """
    pyessv.log('XLS file generation starts ... ', app='SH')

    yielder = _yield_test_workbooks if args.institution_id in _TEST_INSTITUTES else _yield_institutional_workbooks
    for wb in yielder(args.institution_id):
        wb.write()

    pyessv.log('XLS file generation complete ... ', app='SH')


def _yield_test_workbooks(institution_id):
    """Returns set of spreadsheets to be generated.

    """
    for i in range(3):
        source_id = 'sandbox-{}'.format(i + 1)
        for j in pyessv.ESDOC.cmip6.get_model_topics():
            topic_id = j.canonical_name
            topic_label = j.label
            output = _get_output_wrapper(institution_id, source_id, topic_id)
            yield Workbook(institution_id, source_id, topic_id, topic_label, output)


def _yield_institutional_workbooks(institution_id):
    """Returns set of spreadsheets to be generated.

    """
    for i in pyessv.WCRP.cmip6.institution_id:
        if i.canonical_name != institution_id:
            continue
        for j in pyessv.WCRP.cmip6.get_institute_sources(i):
            source_id = j.canonical_name
            for k in pyessv.ESDOC.cmip6.get_model_topics(j):
                topic_id = k.canonical_name
                topic_label = k.label
                output = _get_output_wrapper(institution_id, source_id, topic_id)
                yield Workbook(institution_id, source_id, topic_id, topic_label, output)


def _get_output_wrapper(institution_id, source_id, topic_id):
    """Returns a model documentation output wrapper.

    """
    # Set path to output file.
    fpath = os.getenv('ESDOC_HOME')
    fpath = os.path.join(fpath, 'repos/institutional')
    fpath = os.path.join(fpath, institution_id)
    fpath = os.path.join(fpath, 'cmip6/models')
    fpath = os.path.join(fpath, source_id)
    fpath = os.path.join(fpath, 'json')
    fpath = os.path.join(fpath, 'cmip6_{}_{}_{}.json'.format(institution_id, source_id, topic_id))

    return NotebookOutput(_MIP_ERA, institution_id, source_id, topic_id, path=fpath)


class Workbook(object):
    """Wraps XLS workbook being generated.

    """
    def __init__(self, institution_id, source_id, topic_id, topic_label, doc):
        """Instance constructor.

        """
        self.institution_id = institution_id
        self.source_id = source_id
        self.topic_label = topic_label
        self.topic_id = topic_id
        self.doc = doc
        self.wb = None
        self.ws = None
        self.ws_row = 0
        self.set_topic(doc.specialization)


    def write(self):
        """Write workbook.

        """
        self.write_topic()
        self.write_frontis()
        for st in self.t.sub_topics:
            self.set_subtopic(st)
            self.write_subtopic()

            for ps in st.all_property_containers:
                self.set_propertyset(ps)
                self.write_propertyset()

                for p in ps.properties:
                    self.set_property(p)
                    self.write_property()
                    self.write_property_value()

        self.wb.close()


    def set_topic(self, t):
        """Set topic being processed.

        """
        self.t = t
        self.set_subtopic(None)


    def set_subtopic(self, st):
        """Set sub-topic being processed.

        """
        self.st = st
        self.st_idx = 0 if st is None else self.st_idx + 1
        self.st_id = '{}'.format(self.st_idx)
        self.set_propertyset(None)


    def set_propertyset(self, ps):
        """Set property set being processed.

        """
        self.ps = ps
        self.ps_idx = 0 if ps is None else self.ps_idx + 1
        self.ps_id = '{}.{}'.format(self.st_idx, self.ps_idx)
        self.set_property(None)


    def set_property(self, p):
        """Set property being processed.

        """
        self.p = p
        self.p_idx = 0 if p is None else self.p_idx + 1
        self.p_id = '{}.{}.{}'.format(self.st_idx, self.ps_idx, self.p_idx)
        self.p_values = [] if p is None else self.doc.get_values(p.id)


    def write_topic(self):
        """Write topic workbook.

        """
        path = os.path.join(os.getenv('ESDOC_HOME'), 'repos/institutional')
        path = os.path.join(path, self.institution_id)
        path = os.path.join(path, _MIP_ERA)
        path = os.path.join(path, 'models')
        path = os.path.join(path, self.source_id)
        if not os.path.isdir(path):
            os.makedirs(path)
        fname = '_'.join([_MIP_ERA, self.institution_id, self.source_id, self.topic_id])
        fname += '.xlsx'
        path = os.path.join(path, fname)

        pyessv.log('generating --> {}'.format(fname), app='SH')
        self.wb = xlsxwriter.Workbook(path)


    def write_frontis(self):
        """Writes front summary worksheet.

        """
        # Write worksheet.
        ws = self.wb.add_worksheet('Frontis')

        # Set columns.
        f0 = self.create_format()
        f0.set_bg_color('#337ab7')
        f0.set_font_color('#FFFFFF')
        ws.set_column('A:A', 35, f0)
        ws.set_column('B:B', 180, f0)
        ws.set_column('C:XFD', None, f0)

        # Set formats.
        f0 = self.create_format(26)
        f0.set_bold()
        f0.set_bg_color('#337ab7')
        f0.set_font_color('#FFFFFF')

        f1 = self.create_format(18)
        f1.set_bold()
        f1.set_bg_color('#337ab7')
        f1.set_font_color('#FFFFFF')

        f2 = self.create_format(18)
        f2.set_bg_color('#337ab7')
        f2.set_font_color('#FFFFFF')

        f3 = self.create_format(11)
        f3.set_bg_color('#337ab7')
        f3.set_font_color('#FFFFFF')
        f3.set_italic()

        f4 = self.create_format(14)
        f4.set_align('left')
        f4.set_bg_color('#CCCCCC')
        f4.set_font_color('#000000')

        ws_row = 0
        ws.write(ws_row, 0, 'ES-DOC CMIP6 Model Documentation', f0)

        ws_row += 2
        ws.write(ws_row, 0, 'MIP Era', f1)
        ws.write(ws_row, 1, 'CMIP6', f2)

        ws_row += 1
        ws.write(ws_row, 0, 'Institute', f1)
        ws.write(ws_row, 1, self.doc.institute.upper(), f2)

        ws_row += 1
        ws.write(ws_row, 0, 'Model', f1)
        ws.write(ws_row, 1, self.doc.source_id.upper(), f2)

        ws_row += 1
        ws.write(ws_row, 0, 'Topic', f1)
        ws.write(ws_row, 1, self.topic_label, f2)

        ws_row += 2
        ws.write(ws_row, 0, 'Sub-Topics', f1)
        for idx, st in enumerate(self.t.sub_topics):
            ws.write(ws_row + idx, 1, '{}. {}'.format(idx + 1, st.names(2)), f2)
        ws_row += len(self.t.sub_topics)

        ws_row += 2
        ws.write(ws_row, 0, 'Further Info', f1)
        ws.write(ws_row, 1, 'https://es-doc.org/{}'.format(self.doc.mip_era.lower()), f2)

        ws_row += 1
        ws.write(ws_row, 0, 'Specialization Version', f1)
        ws.write(ws_row, 1, self.t.change_history[-1][0], f2)


    def write_subtopic(self):
        """Write sub-topic worksheet.

        """
        # Set formats.
        f0 = self.create_format()
        f0.set_bg_color('#FFFFFF')

        f1 = self.create_format(24)
        f1.set_bg_color('#003366')
        f1.set_bold()
        f1.set_font_color('#FFFFFF')

        # Write worksheet.
        ws_title = '{}. {}'.format(self.st_idx, self.st.names(2))[0:31]
        self.ws = self.wb.add_worksheet(ws_title)
        self.ws_row = 0

        # Write columns.
        self.ws.set_column(0, 0, 13)
        self.ws.set_column(1, 1, 200)
        self.ws.set_column('C:C', None, None, {
            'hidden': 1,
            })
        self.ws.set_column('D:XFD', None, f0)


    def write_propertyset(self):
        """Write property set worksheet rows.

        """
        # Set formats.
        f0 = self.create_format(18)
        f0.set_bg_color('#003366')
        f0.set_bold()
        f0.set_font_color('#FFFFFF')

        f1 = self.create_format(14)
        f1.set_bold()
        f1.set_italic()

        # Write header.
        if self.ps_idx == 1:
            self.ws_row += 0
        else:
            self.ws_row += 3
        # print 111, self.ps_idx, self.ps_id
        # self.ws_row += (2 if self.ps == self.st.all_property_containers[0] else 3)
        self.ws.set_row(self.ws_row, 24)
        self.ws.write(self.ws_row, 0, self.ps_id, f0)
        self.ws.write(self.ws_row, 1, _get_property_set_label(self.ps), f0)

        # Write description.
        self.ws_row += 1
        self.ws.set_row(self.ws_row, 24)
        self.ws.write(self.ws_row, 1, self.ps.description, f1)


    def write_property(self):
        """Write property worksheet rows.

        """
        # Set formats.
        f0 = self.create_format(14)
        f0.set_bg_color('#337ab7')
        f0.set_bold()
        f0.set_font_color('#FFFFFF')

        f1 = self.create_format(11)

        f2 = self.create_format()
        f2.set_bold()

        f3 = self.create_format(10)
        f3.set_align('left')
        f3.set_italic()

        # Write header.
        self.ws_row += 2
        self.ws.set_row(self.ws_row, 24)
        self.ws.write(self.ws_row, 0, '{} {}'.format(self.p_id, '*' if self.p.is_required else ''), f0)
        self.ws.write(self.ws_row, 1, self.p.name_camel_case_spaced, f0)

        # Write details.
        self.ws_row += 1
        self.ws.set_row(self.ws_row, 24)
        self.ws.write(self.ws_row, 0, self.p.typeof_label, f1)
        self.ws.write(self.ws_row, 1, self.p.description, f2)
        self.ws.write(self.ws_row, 2, self.p.id, f2)

        # Write note: comma separated strings.
        if self.p.typeof == 'cs-str':
            self.ws_row += 1
            self.ws.set_row(self.ws_row, 24)
            self.ws.write(self.ws_row, 1, 'NOTE: Please enter a comma seperated list', f3)

        # Write note: long strings.
        if self.p.typeof == 'l-str':
            self.ws_row += 1
            self.ws.set_row(self.ws_row, 24)
            self.ws.write(self.ws_row, 1, 'NOTE: Double click to expand if text is too long for cell', f3)

        # Write note: X.N cardinality.
        if self.p.is_collection:
            self.ws_row += 1
            self.ws.set_row(self.ws_row, 24)
            self.ws.write(self.ws_row, 1, 'NOTE: Multiple entries are allowed, please insert a new row per entry.', f3)


    def write_property_value(self):
        """Writes a worksheet row per property value.

        """
        if self.p.typeof == 'bool':
            self.write_property_value_bool()

        elif self.p.typeof == 'float':
            self.write_property_value_float()

        elif self.p.typeof == 'int':
            self.write_property_value_int()

        elif self.p.typeof in {'str', 'cs-str', 'l-str'}:
            self.write_property_value_str()

        elif self.p.enum:
            self.write_property_value_enum()


    def write_property_value_bool(self):
        """Writes a property boolean value.

        """
        for val in self.p_values or ['']:
            self.write_property_values(val, {
                'validate': 'list',
                'source': ['TRUE', 'FALSE']
                })


    def write_property_value_enum(self):
        """Writes a property enum value.

        """
        choices = [c.value for c in self.p.enum.choices]
        if self.p.enum.is_open:
            choices.append('Other: document to the right')
        choices = [_str(i[0:255]) for i in choices]

        self.p_values = [_str(i) for i in self.p_values]
        for val in self.p_values or ['']:
            self.write_property_values(val, {
                'validate': 'list'
                }, choices=choices)


    def write_property_value_float(self):
        """Writes a property float value.

        """
        for val in self.p_values or ['']:
            self.write_property_values(val, {
                'validate': 'decimal',
                'criteria': 'between',
                'maximum': 1000000.0,
                'minimum': -1000000.0
                })


    def write_property_value_int(self):
        """Writes a property int value.

        """
        for val in self.p_values or ['']:
            self.write_property_values(val, {
                'validate': 'integer',
                'criteria': '>=',
                'value': 0
                })


    def write_property_value_str(self):
        """Writes a property str value.

        """
        for val in self.p_values or ['']:
            self.write_property_values(val, {
                'validate': 'any',
                })


    def write_property_values(self, val, validation_opts, choices=[]):
        """Writes property values to active worksheet.

        """
        f0 = self.create_format(14)
        f0.set_align('left')
        f0.set_bg_color('#CCCCCC')
        f0.set_font_color('#000000')
        f0.set_text_wrap()
        f0.set_align('top')

        self.ws_row += 1
        self.ws.set_row(self.ws_row, 178 if self.p.typeof == 'l-str' else 24)
        self.ws.write(self.ws_row, 1, val, f0)

        if choices:
            for idx, choice in enumerate(choices):
                self.ws.write(self.ws_row, idx + 26, choice)
            validation_opts['source'] = 'AA{0}:A{1}{0}'.format(self.ws_row + 1, chr(64 + len(choices)))

        self.ws.data_validation(self.ws_row, 1, self.ws_row, 1, validation_opts)


    def create_format(self, font_size=12):
        """Returns a cell formatter.

        """
        f = self.wb.add_format()
        f.set_align('vcenter')
        f.set_font_name('Helvetica Neue')
        f.set_font_size(font_size)

        return f


def _get_property_set_label(ps):
    """Returns label associated with a property set.

    """
    names = ps.names().split(' --> ')
    if len(names) == 3:
        return names[-1]
    elif len(names) == 4:
        return ps.names(2)
    else:
        return ps.names(2)


def _str(val):
    """Formats a string value.

    """
    if val is not None:
        val = str(val).strip()
        if len(val):
            val = '{}{}'.format(val[0].upper(), val[1:])

            return val

    return ''


# Main entry point.
if __name__ == '__main__':
    _main(_ARGS.parse_args())


# Constant value, Turbulent closure - TKE, Turbulent closure - KPP, Turbulent closure - Mellor-Yamada, Turbulent closure - Bulk Mixed Layer, Richardson number dependent - PP, Richardson number dependent - KT, Imbeded as isopycnic vertical coordinate, Other: document to the right