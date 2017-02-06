# -*- coding: utf-8 -*-

"""
.. module:: xl.py
   :license: GPL/CeCIL
   :platform: Unix, Windows
   :synopsis: Wraps Excel spreadsheet access.

.. moduleauthor:: Mark Conway-Greenslade <momipsl@ipsl.jussieu.fr>

"""
import xlrd

import pyesdoc

from constants import *
from convertors import *
from xl_mappings import WS_MAPS



class Spreadsheet(object):
    """The spreadsheet from which CIM documents are to be extracted.

    """
    def __init__(self, worksheet_fpath, identifiers):
        """Instance constructor.

        """
        self.ids = identifiers
        self._spreadsheet = xlrd.open_workbook(worksheet_fpath)


    def _get_sheet(self, ws_name):
        """Returns pointer to a named worksheet.

        """
        return self._spreadsheet.sheet_by_name(ws_name)


    def _get_rows(self, ws_name):
        """Returns collection of rows within a named worksheet.

        """
        return enumerate(self._get_sheet(ws_name).get_rows())


    def _yield_rows(self, ws_name):
        """Yields rows within a named worksheet.

        """
        for idx, row in self._get_rows(ws_name):
            if idx >= WS_ROW_OFFSETS[ws_name] and \
               len(row[0].value):
                yield idx, row


    def _get_cell_value(self, row, col_idx, convertor):
        """Returns the (converted) value of a worksheet cell.

        """
        # Extract raw cell value.
        value = row[col_idx - 1].value

        # Nullify dead text.
        if isinstance(value, (unicode, str)):
            value = value.strip()
            if len(value) == 0:
                value = None
            elif value.upper() in {u"NONE", u"N/A"}:
                value = None

        # Convert if necessary.
        if convertor:
            try:
                return convertor(value)
            except TypeError:
                return convertor(value, lambda i: row[i - 1].value)

        return value


    def __getitem__(self, ws_name):
        """Returns a child table attribute.

        """
        doc_type, mappings = WS_MAPS[ws_name]

        return [self._get_document(self.ids[ws_name][str(idx)], doc_type, row, mappings)
                for idx, row in self._yield_rows(ws_name)]


    def _set_document_attribute(self, doc, row, mapping):
        """Asssigns a document attribute form a mapping.

        """
        # Unpack mapping info.
        try:
            attr, col_idx, convertor = mapping
        except ValueError:
            try:
                attr, col_idx = mapping
            except ValueError:
                print mapping
                raise ValueError()
            convertor = None

        # Convert cell value.
        if col_idx.find("-") == -1:
            attr_value = self._get_cell_value(row, convert_col_idx(col_idx), convertor)
        else:
            col_idx_from, col_idx_to = [convert_col_idx(i) for i in col_idx.split("-")]
            attr_value = [i for i in (self._get_cell_value(row, i, convertor)
                          for i in range(col_idx_from, col_idx_to + 1)) if i]

        # Set aattribute value.
        setattr(doc, attr, attr_value)


    def _get_document(self, doc_uid, doc_type, row, mappings):
        """Returns a CIM document from a spreadsheet row.

        """
        # Create document.
        doc = pyesdoc.create(doc_type,
                             project=DOC_PROJECT,
                             source=DOC_SOURCE,
                             version=1,
                             uid=doc_uid)

        # Assign document dates.
        try:
            doc.meta
        except AttributeError:
            pass
        else:
            doc.meta.create_date = DOC_CREATE_DATE
            doc.meta.update_date = DOC_UPDATE_DATE

        # Assign document author.
        try:
            doc.meta.author = DOC_AUTHOR_REFERENCE
        except AttributeError:
            pass

        # Set document attributes from mapped worksheet cells.
        for mapping in mappings:
            self._set_document_attribute(doc, row, mapping)

        return doc