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

from _utils import ModelTopicDocumentation



# Define command line argument parser.
_ARGS = argparse.ArgumentParser("Generates CMIP6 model PDF files.")
_ARGS.add_argument(
    "--institution-id",
    help="An institution identifier",
    dest="institution_id",
    type=str
    )

# MIP era.
_MIP_ERA = "cmip6"

# Template cache.
_TEMPLATES_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "templates_pdf")
_TEMPLATES = template.Loader(_TEMPLATES_PATH)


def _main(args):
    """Main entry point.

    """
    # Set institutes to be processed.
    institutes = pyessv.WCRP.cmip6.institution_id if args.institution_id == 'all' else \
                 [pyessv.WCRP.cmip6.institution_id[args.institution_id]]

    # Load template into memory.
    template = _TEMPLATES.load("main.tornado")

    # Write a PDF file per CMIP6 institute | topic combination.
    # i = institute | j = source | k = topic
    for i in institutes:
        for j in pyessv.WCRP.cmip6.get_institute_sources(i):
            for k in pyessv.ESDOC.cmip6.get_model_topics(j):
                _write(template, i, j, k)


def _write(template, i, j, k):
    """Main entry point.

    """
    # Set documentation output wrapper.
    output = ModelTopicDocumentation.create(_MIP_ERA, i, j, k)

    # Generate latex.
    as_latex = template.generate(
        topic=output.specialization,
        topic_label=k.label,
        DOC=output,
        now=dt.datetime.now(),
        _str=_str
        )

    # Ensure that PDf generation will process unicode characters.
    as_latex = as_latex.replace('&amp;', 'and')
    as_latex = as_latex.replace('&quot;', '"')

    # Write pdf.
    _write_pdf(latex.build_pdf(as_latex), i, j, k)


def _write_pdf(content, i, j, k):
    """Get notebook output.

    """
    fpath = os.path.join(os.getenv('ESDOC_HOME'), 'repos/institutional')
    fpath = os.path.join(fpath, i.canonical_name)
    fpath = os.path.join(fpath, _MIP_ERA)
    fpath = os.path.join(fpath, 'models')
    fpath = os.path.join(fpath, j.canonical_name)
    fpath = os.path.join(fpath, 'pdf')
    if not os.path.isdir(fpath):
        os.makedirs(fpath)

    fname = '{}_{}_{}_{}.pdf'.format(
        _MIP_ERA, i.canonical_name, j.canonical_name, k.canonical_name
        )
    pyessv.log('generating --> {}'.format(fname), app='SH')

    with open(os.path.join(fpath, fname), 'w') as fstream:
        fstream.write(str(content))


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
    _main(_ARGS.parse_args())
