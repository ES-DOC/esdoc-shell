# -*- coding: utf-8 -*-

"""
.. module:: generate_cim.py
   :license: GPL/CeCIL
   :platform: Unix, Windows
   :synopsis: Generates CMIP6 JSON documents from XLS files.

.. moduleauthor:: Mark Conway-Greenslade <momipsl@ipsl.jussieu.fr>

"""
import argparse
import collections
import json
import os

import openpyxl
import pyesdoc
import pyessv

from pyesdoc.ontologies.cim import v2 as cim

import _utils as utils



# Define command line argument parser.
_ARGS = argparse.ArgumentParser("Generates CMIP6 model JSON files.")
_ARGS.add_argument(
    "--institution-id",
    help="An institution identifier",
    dest="institution_id",
    type=str
    )

# MIP era.
_MIP_ERA = "cmip6"

# Name of file controlling publication.
_MODEL_PUBLICATION_FNAME = "model_publication.json"

# Set of valid publication states.
_PUBLICATION_STATUS_SET = {"off", "draft", "on"}


def _main(args):
    """Main entry point.

    """
    # Set institutes to be processed.
    institutes = pyessv.WCRP.cmip6.institution_id if args.institution_id == 'all' else \
                 [pyessv.WCRP.cmip6.institution_id[args.institution_id]]

    # Write a CIM file per CMIP6 institute | source combination.
    # i = institute | s = source | t = topic
    for i in institutes:
        try:
            settings = _get_publication_settings(i)
        except IOError:
            warning = '{} model_publications.json not found'
            warning = warning.format(i.canonical_name)
            pyessv.log_warning(warning)
            continue

        for s in pyessv.WCRP.cmip6.get_institute_sources(i):
            try:
                settings[s.canonical_name]
            except KeyError:
                warning = '{} :: {} publication settings not found'
                warning = warning.format(i.canonical_name, s.canonical_name)
                pyessv.log_warning(warning)
                continue

            for t in pyessv.ESDOC.cmip6.get_model_topics(s):
                setting = _get_setting(settings, i, s, t)
                if setting in (None, "off"):
                    continue

                try:
                    wb = _get_spreadsheet_path(i, s, t)
                except IOError:
                    warning = '{} :: {} :: {} spreadsheet not found'
                    warning = warning.format(i.canonical_name, s.canonical_name, t.canonical_name)
                    pyessv.log_warning(warning)
                    continue

                _write_json(i, s, t, wb)


def _get_publication_settings(i):
    """Returns an institute's model publication settings.

    """
    fpath = os.path.join(utils.get_folder_of_cmip6_institute(i),
                         _MODEL_PUBLICATION_FNAME)
    with open(fpath, 'r') as fstream:
        return json.loads(fstream.read())


def _get_setting(settings, i, s, t):
    """Returns a source topic publication status.

    """
    return 'on'
    try:
        return settings[s.canonical_name][t.canonical_name]['publish']
    except KeyError:
        warning = '{} :: {} :: {} topic setting either not found or invalid'
        warning = warning.format(i.canonical_name, s.canonical_name, t.canonical_name)
        pyessv.log_warning(warning)


def _get_spreadsheet_path(i, s, t):
    """Returns a model topic spreadsheet for processing.

    """
    fname = utils.get_file_of_cmip6(i, s, t, 'xlsx')
    path = utils.get_folder_of_cmip6_source(i, s)
    path = os.path.join(path, fname)
    if not os.path.exists:
        raise IOError()

    return openpyxl.load_workbook(path, read_only=True)


def _write_json(i, s, t, wb):
    """Writes a JSON file to file system.

    """
    # Initialise output.
    obj = collections.OrderedDict()
    obj['mipEra'] = _MIP_ERA
    obj['institute'] = i.canonical_name
    obj['seedingSource'] = None
    obj['sourceID'] = s.canonical_name
    obj['topic'] = t.canonical_name
    obj['content'] = collections.OrderedDict()

    # Process spreadsheet.
    for idx, ws in enumerate(wb):
        # Process citations/responsible parties.
        if idx == 1:
            print "TODO: process citations/responsible parties"
            continue

        # Extract specialization entries.
        elif idx > 1:
            _set_xls_content(obj, ws)

    # Persist output.
    fname = utils.get_file_of_cmip6(i, s, t, 'json')
    path = utils.get_folder_of_cmip6_source(i, s, 'json')
    path = os.path.join(path, fname)
    with open(path, 'w') as fstream:
        fstream.write(json.dumps(obj, indent=4))


def _set_xls_content(obj, ws):
    """Sets content for a particular specialization.

    """
    content = None
    for row in ws.iter_rows(min_row=1, max_col=3, max_row=ws.max_row):
        if row[1].value is None:
            if content is not None:
                if content[1]:
                    obj['content'][content[0]] = {'values': content[1]}
                content = None

        elif row[2].value is not None:
            content = (row[2].value, [])

        elif content is not None:
            if not _is_note(row[1]):
                content[1].append(row[1].value)


def _is_note(cell):
    """Returns flag indicating whether a cell represents a note tot he user or not.

    """
    try:
        return cell.value.startswith('NOTE: ')
    except AttributeError:
        return False


# Main entry point.
if __name__ == '__main__':
    _main(_ARGS.parse_args())
