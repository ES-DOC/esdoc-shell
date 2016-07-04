# -*- coding: utf-8 -*-

"""
.. module:: run_publish_cmip6_documents.py
   :license: GPL/CeCIL
   :platform: Unix, Windows
   :synopsis: Publishes CMIP6 documents from the CMIP6 experiment spreadsheet.

.. moduleauthor:: Mark Conway-Greenslade <momipsl@ipsl.jussieu.fr>

"""
import argparse
import glob
import json
import os
from collections import OrderedDict

import pyesdoc
import pyesdoc.ontologies.cim as cim



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

# Cache of documents.
_DOC_CACHE = {}

# Cache of experiment definitions to be written to file system.
_OUTPUT = {}


def _yield_documents(input_dir, doc_type):
    """Yields set of document for further processing.

    """
    for fpath in glob.iglob("{}/{}*.*".format(input_dir, doc_type)):
        yield pyesdoc.read(fpath)


def _get_requirement(r_ref):
    r = _DOC_CACHE[r_ref.id]
    r.meta.type = r_ref.type

    return r


def _yield_experiments(input_dir):
    """Yields set of experiments to be written to file system.

    """
    for e in _yield_documents(input_dir, "cim.2.designing.NumericalExperiment"):
        e.requirements = [_get_requirement(rr) for rr in e.requirements]

        yield e, json.dumps(_map_experiment(e), indent=4)


def _map_requirement(r):
    """Returns a requirement document mapped to a dictionary.

    """
    def get_requirement_type():
        """Returns a shortened requirement type description.

        """
        if len(r.meta.type.split(":")) == 2:
            return r.meta.type.split(":")[1].replace("_", "-")
        elif isinstance(r, cim.v2.ForcingConstraint):
            return "forcing-constraint"
        elif isinstance(r, cim.v2.TemporalConstraint):
            return "temporal-constraint"
        elif isinstance(r, cim.v2.EnsembleRequirement):
            return "ensemble"
        elif isinstance(r, cim.v2.EnsembleRequirement):
            return "ensemble"
        elif isinstance(r, cim.v2.MultiEnsemble):
            return "multi-ensemble"

        return "unknown"


    result = OrderedDict()
    result['description'] = r.description
    result['isConformanceRequested'] = r.is_conformance_requested
    result['keywords'] = r.keywords
    result['name'] = r.name
    result['type'] = get_requirement_type()

    return result


def _map_experiment(e):
    """Returns an experiment document mapped to a dictionary.

    """
    result = OrderedDict()
    result['canonical_name'] = e.canonical_name
    result['description'] = e.description
    result['keywords'] = e.keywords
    result['long_name'] = e.long_name
    result['mip_era'] = "cmip6"
    result['rationale'] = e.rationale
    result['related_experiments'] = [{
            "mip_era": "cmip6",
            "name": i.name,
            "uid": i.id
        } for i in e.related_experiments]
    result['requirements'] = [_map_requirement(i) for i in e.requirements]
    result['uid'] = e.meta.id
    result['viewerURL'] = "http://view.es-doc.org?renderMethod=id&project=cmip6-draft&id={}&version=latest&client=mohc".format(e.meta.id)

    return result


def _cache_requirements(input_dir):
    """Caches set of experiment requirements for later processing.

    """
    for requirement_type in {
        "cim.2.designing.EnsembleRequirement",
        "cim.2.designing.ForcingConstraint",
        "cim.2.designing.MultiEnsemble",
        "cim.2.designing.NumericalRequirement",
        "cim.2.designing.TemporalConstraint"
    }:
        for doc in _yield_documents(input_dir, requirement_type):
            _DOC_CACHE[doc.meta.id] = doc


def _main(args):
    """Main entry point.

    """
    if not os.path.isdir(args.input_dir):
        raise ValueError("Input directory does not exist")
    if not os.path.isdir(args.output_dir):
        raise ValueError("Output directory does not exist")

    # Step 1: cache requirements.
    _cache_requirements(args.input_dir)

    # Step 2: map experiments & write to file system.
    for e, e_json in _yield_experiments(args.input_dir):
        fpath = "{}/cmip6-experiment-{}.json".format(args.output_dir, e.canonical_name.lower())
        with open(fpath, 'w') as fstream:
            fstream.write(e_json)


# Entry point.
if __name__ == '__main__':
    _main(_ARGS.parse_args())
