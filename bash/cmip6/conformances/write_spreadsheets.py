# -*- coding: utf-8 -*-

"""
.. module:: write_spreadsheets.py
   :license: GPL/CeCIL
   :platform: Unix, Windows
   :synopsis: Emits blank CMIP6 conformance spreadsheets.

.. moduleauthor:: Mark Conway-Greenslade <momipsl@ipsl.jussieu.fr>

"""
import argparse
import collections
import glob
import json
import os

from openpyxl import Workbook

import pyesdoc
import pyesdoc.ontologies.cim.v2 as cim



# Define command line options.
_ARGS = argparse.ArgumentParser("Generates config files of CMIP6 experiements.")
_ARGS.add_argument(
    "--input",
    help="Path to a directory from which cim documents will be read.",
    dest="input_dir",
    type=str
    )
_ARGS.add_argument(
    "--output",
    help="Path to a directory into which configuration documents will be written.",
    dest="output_dir",
    type=str
    )

# Documents cached by uid.
_DOC_CACHE_1 = {}

# Documents cached by type / canonical name.
_DOC_CACHE_2 = collections.defaultdict(dict)

# Viewer url.
_VIEWER_URL = "https://documentation.es-doc.org/cmip6/{}/{}?client=esdoc"

# Maps of requirement type to type keys.
_REQUIREMENT_TYPE_KEYS = {
    cim.ForcingConstraint: "forcing-constraint",
    cim.TemporalConstraint: "temporal-constraint",
    cim.EnsembleRequirement: "ensemble",
    cim.MultiEnsemble: "multi-ensemble"
}

_MIP_EXP_MAP = collections.defaultdict(set)
_REQ_EXP_MAP = collections.defaultdict(set)
_REQ_MIP_MAP = collections.defaultdict(set)
_REQ_SCOPE_MAP = collections.defaultdict(set)
_REQ_GROUPS = set()


def _get_requirement(r_ref):
    """Returns a cached requirement.

    """
    try:
        r_ref = r_ref.meta
    except AttributeError as err:
        pass
    r = _DOC_CACHE_1[r_ref.id]
    r.meta.type = r_ref.type

    return r


def _main(args):
    """Main entry point.

    """
    if not os.path.isdir(args.input_dir):
        raise ValueError("Input directory does not exist")
    if not os.path.isdir(args.output_dir):
        raise ValueError("Output directory does not exist")

    # Step 1: cache documents.
    _load_cache(args.input_dir)

    # Step 2: Build relevant maps.
    for mip in _DOC_CACHE_2[cim.Project].values():
        for exp_ref in mip.required_experiments:
            exp = _DOC_CACHE_2[cim.NumericalExperiment][exp_ref.canonical_name]
            _MIP_EXP_MAP[mip].add(exp)
            for req_ref in exp.requirements:
                req = _get_requirement(req_ref)
                assert req == _DOC_CACHE_2[type(req)][req.name]
                if isinstance(req, cim.NumericalRequirement):
                    if len(req.additional_requirements):
                        _REQ_GROUPS.add(req)
                _REQ_MIP_MAP[exp].add(req)
                _REQ_EXP_MAP[exp].add(req)
                _REQ_SCOPE_MAP[req.scope].add(req)

    # Step 3: Build spreadsheets.
    pass


def _yield_documents(input_dir, type_key):
    """Yields set of document for further processing.

    """
    for fpath in glob.iglob("{}/{}*.*".format(input_dir, type_key)):
        yield pyesdoc.read(fpath)


def _load_cache(input_dir):
    """Caches set of documents for later processing.

    """
    for doc_type in {
        cim.EnsembleRequirement,
        cim.ForcingConstraint,
        cim.MultiEnsemble,
        cim.NumericalExperiment,
        cim.NumericalRequirement,
        cim.Project,
        cim.TemporalConstraint
    }:
        for doc in _yield_documents(input_dir, doc_type.type_key):
            _DOC_CACHE_1[doc.meta.id] = doc
            _DOC_CACHE_2[doc_type][doc.canonical_name] = doc


# Entry point.
if __name__ == '__main__':
    _main(_ARGS.parse_args())