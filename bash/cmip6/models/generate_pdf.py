# -*- coding: utf-8 -*-

"""
.. module:: generate_pdf/__main__.py
   :license: GPL/CeCIL
   :platform: Unix, Windows
   :synopsis: Generates CMIP6 PDF documents.

.. moduleauthor:: Mark Conway-Greenslade <momipsl@ipsl.jussieu.fr>

"""
import argparse
import datetime as dt
import os

import latex
from tornado import template

import pyesdoc
import pyessv
from pyesdoc.ipython.model_topic import NotebookOutput



# Define command line argument parser.
_ARGS = argparse.ArgumentParser("Generates an institute's CMIP6 model PDF files.")
_ARGS.add_argument(
    "--institution-id",
    help="An institution identifier",
    dest="institution_id",
    type=str
    )

# Template cache.
_TEMPLATES_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "templates_pdf")
_TEMPLATES = template.Loader(_TEMPLATES_PATH)

# Set of test instiutes.
_TEST_INSTITUTES = {'test-institute-1', 'test-institute-2', 'test-institute-3'}

# MIP era.
_MIP_ERA = "cmip6"


def _main(institution_id):
    """Main entry point.

    """
    # Load template into memory.
    latex_template = _TEMPLATES.load("main.tornado")

    for source_id, topic_id, topic_label in _yield_config(institution_id):
        # if topic_id != 'ocean':
        #     continue

        pyessv.log('generating PDF --> {} : {} : {} : {}'.format(_MIP_ERA, institution_id, source_id, topic_id), app='SH')

        # Set documentation output wrapper.
        output = _get_output_wrapper(institution_id, source_id, topic_id)

        # Generate latex.
        as_latex = latex_template.generate(
            topic=output.specialization,
            topic_label=topic_label,
            DOC=output,
            now=dt.datetime.now(),
            _str=_str
            )

        # Ensure that PDf generation will process unicode characters.
        as_latex = as_latex.replace('&amp;', 'and')
        as_latex = as_latex.replace('&quot;', '"')

        # Generate pdf.
        as_pdf = latex.build_pdf(as_latex)

        # Write pdf.
        write_pdf(institution_id, source_id, topic_id, as_pdf)

        # break

    pyessv.log('PDF file generation complete ... ', app='SH')


def _yield_config(institution_id):
    """Returns job configuration information.

    """
    if institution_id in _TEST_INSTITUTES:
        for i in range(3):
            for j in pyessv.ESDOC.cmip6.get_model_topics():
                yield 'sandbox-{}'.format(i + 1), j.canonical_name, j.label
    else:
        for j in pyessv.WCRP.cmip6.get_institute_sources(institution_id):
            for k in pyessv.ESDOC.cmip6.get_model_topics(j):
                yield j.canonical_name, k.canonical_name, k.label


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


def write_pdf(institution_id, source_id, topic_id, pdf):
    """Get notebook output.

    """
    fname = '_'.join([_MIP_ERA, institution_id, source_id, topic_id])
    fname += '.pdf'

    path = os.path.join(os.getenv('ESDOC_HOME'), 'repos/institutional')
    path = os.path.join(path, institution_id)
    path = os.path.join(path, _MIP_ERA)
    path = os.path.join(path, 'models')
    path = os.path.join(path, source_id)
    path = os.path.join(path, 'pdf')
    if not os.path.isdir(path):
        os.makedirs(path)
    path = os.path.join(path, fname)

    with open(path, 'w') as fstream:
        fstream.write(str(pdf))


def _str(val):
    """Formats a string value.

    """
    if val is None:
        return ''
    elif not isinstance(val, (str, unicode)):
        return str(val)
    else:
        val = val.encode('utf').strip()
        if len(val) == 0:
            return ''

        val = '{}{}'.format(val[0].upper(), val[1:])

        # Ensures latex can emit.
        val = unicode(val, "utf-8", errors="ignore")
        val = val.encode('ascii', 'ignore')

    return val


# Main entry point.
if __name__ == '__main__':
    _args = _ARGS.parse_args()
    _main(_args.institution_id)
