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


def _main(args):
    """Main entry point.

    """
    pyessv.log('XLS file generation starts ... ', app='SH')

    for source_id, topic_id, topic_label, doc in _yield_config(args.institution_id):
        wb = Workbook(args.institution_id, source_id, topic_id, topic_label, doc)
        wb.write()

    pyessv.log('XLS file generation complete ... ', app='SH')


def _yield_config(institution_id):
    """Returns set of notebooks to be generated.

    """
    for i in pyessv.WCRP.cmip6.institution_id:
        if i.canonical_name != institution_id:
            continue
        for j in pyessv.WCRP.cmip6.get_institute_sources(i):
            for k in pyessv.ESDOC.cmip6.get_model_topics(j):
                output = NotebookOutput.create(_MIP_ERA, i.canonical_name, j.canonical_name, k.canonical_name)
                yield j.canonical_name, k.canonical_name, k.label, output


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
        f0 = self.create_format(None)
        f0.set_bg_color('#337ab7')
        f0.set_font_color('#FFFFFF')

        f1 = self.create_format(None)
        f1.set_bg_color('white')
        f1.set_font_color('#FFFFFF')

        ws.set_column('A:A', 35, f0)
        ws.set_column('B:B', 55, f0)
        ws.set_column('C:E', None, f0)
        ws.set_column('F:ZZ', None, f1)
        for i in range(100):
            ws.set_row(i + 12 + len(self.t.sub_topics), None, f1)

        # Write header.
        f0 = self.create_format(26)
        f0.set_bold()
        f0.set_bg_color('#337ab7')
        f0.set_font_color('#FFFFFF')
        f0.set_underline()
        ws.write(0, 0, 'ES-DOC CMIP6 Model Documentation', f0)

        # Write summary.
        f1 = self.create_format(18)
        f1.set_bold()
        f1.set_bg_color('#337ab7')
        f1.set_font_color('#FFFFFF')

        f2 = self.create_format(18)
        f2.set_bg_color('#337ab7')
        f2.set_font_color('#FFFFFF')

        ws.write(2, 0, 'Institute', f1)
        ws.write(2, 1, self.doc.institute.upper(), f2)
        ws.write(3, 0, 'Model', f1)
        ws.write(3, 1, self.doc.source_id.upper(), f2)
        ws.write(4, 0, 'Topic', f1)
        ws.write(4, 1, self.topic_label, f2)

        ws.write(6, 0, 'Sub-Topics', f1)
        for idx, st in enumerate(self.t.sub_topics):
            ws.write(6 + idx, 1, '{}. {}'.format(idx + 1, st.names(2)), f2)

        ws.write(7 + len(self.t.sub_topics), 0, 'Specialization Version', f1)
        ws.write(7 + len(self.t.sub_topics), 1, self.t.change_history[-1][0], f2)
        ws.write(9 + len(self.t.sub_topics), 0, 'Further Info', f1)
        ws.write(9 + len(self.t.sub_topics), 1, 'https://es-doc.org/{}'.format(self.doc.mip_era.lower()), f2)
        ws.write(10 + len(self.t.sub_topics), 1, 'https://specializations.es-doc.org/{}'.format(self.doc.mip_era.lower()), f2)


    def write_subtopic(self):
        """Write sub-topic worksheet.

        """
        # Write worksheet.
        ws_title = '{}. {}'.format(self.st_idx, self.st.names(2))[0:31]
        self.ws = self.wb.add_worksheet(ws_title)

        # Set columns.
        self.ws.set_column(0, 0, 5.5)
        self.ws.set_column(1, 1, 120)
        self.ws.set_column(2, 4, 18)
        self.ws.set_column(5, 5, 85)

        # Write header.
        f0 = self.create_format(24)
        f0.set_bg_color('#337ab7')
        f0.set_bold()
        f0.set_font_color('#FFFFFF')

        self.ws_row = 0
        self.ws.set_row(self.ws_row, 36)
        self.ws.write(self.ws_row, 0, self.st_id, f0)
        self.ws.write(self.ws_row, 1, self.st.description, f0)
        self.ws.write(self.ws_row, 2, '', f0)
        self.ws.write(self.ws_row, 3, '', f0)
        self.ws.write(self.ws_row, 4, '', f0)
        self.ws.write(self.ws_row, 5, '', f0)


    def write_propertyset(self):
        """Write property set worksheet rows.

        """
        # Write header.
        f0 = self.create_format(18)
        f0.set_bg_color('#337ab7')
        f0.set_bold()
        f0.set_font_color('#FFFFFF')

        self.ws_row += (2 if self.ps == self.st.all_property_containers[0] else 3)
        self.ws.set_row(self.ws_row, 24)
        self.ws.write(self.ws_row, 0, self.ps_id, f0)
        self.ws.write(self.ws_row, 1, _get_property_set_label(self.ps), f0)
        self.ws.write(self.ws_row, 2, '', f0)
        self.ws.write(self.ws_row, 3, '', f0)
        self.ws.write(self.ws_row, 4, '', f0)
        self.ws.write(self.ws_row, 5, '', f0)

        # Write description.
        f0 = self.create_format(14)
        f0.set_bold()
        f0.set_italic()

        self.ws_row += 1
        self.ws.set_row(self.ws_row, 24)
        self.ws.write(self.ws_row, 1, self.ps.description, f0)


    def write_property(self):
        """Write property worksheet rows.

        """
        # Write header.
        f0 = self.create_format(14)
        f0.set_bg_color('#337ab7')
        f0.set_bold()
        f0.set_font_color('#FFFFFF')

        f1 = self.create_format(14)
        f1.set_align('center')
        f1.set_bg_color('#337ab7')
        f1.set_bold()
        f1.set_font_color('#FFFFFF')

        self.ws_row += 2
        self.ws.set_row(self.ws_row, 24)
        self.ws.write(self.ws_row, 1, '{} - {}'.format(self.p_id, self.p.name_camel_case_spaced), f0)
        self.ws.write(self.ws_row, 2, 'Is Required ?', f1)
        self.ws.write(self.ws_row, 3, 'Cardinality', f1)
        self.ws.write(self.ws_row, 4, 'Type', f1)
        self.ws.write(self.ws_row, 5, 'Specialization ID', f0)

        # Write details.
        f0 = self.create_format(12)
        f0.set_bold()

        f1 = self.create_format(12)
        f1.set_align('center')
        f1.set_bold()

        f2 = self.create_format(12)
        f2.set_bold()
        f2.set_italic()

        self.ws_row += 1
        self.ws.set_row(self.ws_row, 24)
        self.ws.write(self.ws_row, 1, self.p.description, f2)
        self.ws.write(self.ws_row, 2, self.p.is_required, f1)
        self.ws.write(self.ws_row, 3, self.p.cardinality, f1)
        self.ws.write(self.ws_row, 4, self.p.typeof_label, f1)
        self.ws.write(self.ws_row, 5, self.p.id, f0)


    def write_property_value(self):
        """Write property worksheet rows.

        """
        if self.p.typeof == 'bool':
            self.write_property_values({
                'validate': 'list',
                'source': ['TRUE', 'FALSE']
                })

        elif self.p.typeof == 'float':
            self.write_property_values({
                'validate': 'decimal',
                'criteria': 'between',
                'maximum': 1000000.0,
                'minimum': -1000000.0
                })

        elif self.p.typeof == 'int':
            self.write_property_values({
                'validate': 'integer',
                'criteria': '>=',
                'value': 0
                })

        elif self.p.typeof == 'str':
            self.write_property_values({
                'validate': 'any',
                })

        elif self.p.enum:
            options = [c.value for c in self.p.enum.choices]
            if self.p.enum.is_open:
                options.append('Other: document in the cell to the right')
            self.p_values = [_str(i) for i in self.p_values]
            self.write_property_values({
                'validate': 'list',
                'source': [_str(i[0:250]) for i in options]
                })


    def write_property_values(self, validation_opts):
        """Writes property values to active worksheet.

        """
        f0 = self.create_format(14)
        f0.set_align('left')
        f0.set_bg_color('#CCCCCC')
        f0.set_font_color('#000000')

        for val in self.p_values or ['']:
            self.ws_row += 1
            self.ws.set_row(self.ws_row, 24)
            self.ws.write(self.ws_row, 1, val, f0)
            self.ws.data_validation(self.ws_row, 1, self.ws_row, 1, validation_opts)


    def create_format(self, font_size):
        """Returns a cell formatter.

        """
        f = self.wb.add_format()
        f.set_align('vcenter')
        f.set_font_name('Helvetica Neue')
        if font_size is not None:
            f.set_font_size(font_size)

        return f


def _get_property_set_label(ps):
    """Returns label associated with a property set.

    """
    names = ps.names().split(' --> ')
    if len(names) == 3:
        return '{} --> Top Level Details'.format(names[-1])
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
