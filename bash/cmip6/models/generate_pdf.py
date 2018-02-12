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

# MIP era.
_MIP_ERA = "cmip6"


def _main(args):
    """Main entry point.

    """
    for source_id, topic_id, topic_label, doc in _yield_config(args.institution_id):
        # Generate latex.
        as_latex = _TEMPLATES.load("main.tornado").generate(
            topic=doc.specialization,
            topic_label=topic_label,
            DOC=doc,
            escape=lambda s: s.strip().replace('"', "'"),
            now=dt.datetime.now(),
            _str=_str
            )

        # Generate pdf.
        as_pdf = latex.build_pdf(as_latex)

        # Write pdf.
        write_pdf(args.institution_id, source_id, topic_id, as_pdf)

    pyessv.log('PDF file generation complete ... ', app='SH')


def _yield_config(institution_id):
    """Returns set of notebooks to be generated.

    """
    pyessv.log('loading config ... ', app='SH')
    for i in pyessv.WCRP.cmip6.institution_id:
        if i.canonical_name != institution_id:
            continue
        for j in pyessv.WCRP.cmip6.get_institute_sources(i):
            for k in pyessv.ESDOC.cmip6.get_model_topics(j):
                output = NotebookOutput.create(_MIP_ERA, i.canonical_name, j.canonical_name, k.canonical_name)
                yield j.canonical_name, k.canonical_name, k.label, output


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
    if not os.path.isdir(path):
        os.makedirs(path)
    path = os.path.join(path, fname)

    pyessv.log('generating --> {}'.format(fname), app='SH')
    with open(path, 'w') as fstream:
        fstream.write(str(pdf))


def _str(val):
    """Formats a string value.

    """
    if val is not None:
        val = str(val).strip()
        if len(val):
            val = '{}{}'.format(val[0].upper(), val[1:])
            val = val.replace('&', 'and')
            val = val.replace('?', '\?')
            val = val.replace('\\', 'xxx')
            val = val.replace('"', '')

            return val

    return ''


# Main entry point.
if __name__ == '__main__':
    _main(_ARGS.parse_args())
