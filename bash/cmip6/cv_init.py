    # -*- coding: utf-8 -*-

"""
.. module:: write_cv.py.py
   :license: GPL/CeCIL
   :platform: Unix, Windows
   :synopsis: Maps raw WCRP CMIP6 vocab files to normalized pyesdoc CV format and writes to esdoc-cv repo.

.. moduleauthor:: Mark Conway-Greenslade <momipsl@ipsl.jussieu.fr>

"""
import argparse
import datetime as dt
import json
import os

import arrow

import pyesdoc
from pyesdoc import cv



# Define command line options.
_ARGS = argparse.ArgumentParser("Maps raw WCRP CMIP6 vocab files to normalized pyesdoc CV format and writes to esdoc-cv repo.")
_ARGS.add_argument(
    "--source",
    help="Path from which raw WCRP CMIP6 vocab files will be read.",
    dest="source",
    type=str
    )
_ARGS.add_argument(
    "--dest",
    help="Path to which vocab files will be written.",
    dest="dest",
    type=str
    )

# CV authority = WCRP.
_CV_AUTHORITY = pyesdoc.cv.create_authority(
    name=u"WCRP",
    description=u"World Climate Research Program",
    url=u"https://www.wcrp-climate.org/wgcm-overview"
    )

# CV scope = CMIP6.
_CV_SCOPE = pyesdoc.cv.create_scope(
    authority=_CV_AUTHORITY,
    name=u"CMIP6",
    description=u"Controlled Vocabularies (CVs) for use in CMIP6",
    url=u"https://github.com/WCRP-CMIP/CMIP6_CVs"
    )

# Ensure we use fixed creation date.
_CREATE_DATE = arrow.get("2016-12-14 12:00:00.000000+0000").datetime


def _main(args):
    """Main entry point.

    """
    if not os.path.isdir(args.dest):
        raise ValueError("Archive directory does not exist")
    if not os.path.isdir(args.source):
        raise ValueError("Archive directory does not exist")

    # Create CV collections.
    for typeof, term_data_factory in {
        ('activity_id', None),
        ('experiment_id', lambda obj, name: obj[name]),
        ('institution_id', lambda obj, name: {'postal_address': obj[name]}),
        ('realm', None),
        ('source_id', lambda obj, name: obj[name]),
        ('source_type', None)
    }:
        _create_collection(args.source, typeof, term_data_factory)

    # Write CV to destination directory.
    cv.write_authority(args.dest, _CV_AUTHORITY)


def _create_collection(source, collection_type, data_factory):
    """Creates a pyesdoc formatted CV collection from a WCRP CMIP6 CV file.

    """
    # Create collection.
    collection = pyesdoc.cv.create_collection(
        scope=_CV_SCOPE,
        name=unicode(collection_type).replace("_", "-"),
        description=u"WCRP CMIP6 CV collection: ".format(collection_type.replace("_", "-"))
        )
    collection.create_date = _CREATE_DATE

    # Create terms.
    obj = _get_input_data(source, collection_type)
    for name in obj:
        term_data = None
        if data_factory is not None:
            term_data = data_factory(obj, name)
        term = pyesdoc.cv.create_term(collection=collection, name=name, data=term_data)
        term.create_date = _CREATE_DATE


def _get_input_data(source, collection_type):
    """Returns WCRP CV input data.

    """
    fpath = os.path.join(source, "CMIP6_{}.json".format(collection_type))
    with open(fpath, 'r') as fstream:
        return json.loads(fstream.read())[collection_type]


# Entry point.
if __name__ == '__main__':
    _main(_ARGS.parse_args())
