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

# Viewer url.
_VIEWER_URL = "https://documentation.es-doc.org/cmip6/experiments/{}?client=mohc"


def _yield_documents(input_dir, doc_type):
    """Yields set of document for further processing.

    """
    for fpath in glob.iglob("{}/{}*.*".format(input_dir, doc_type)):
        yield pyesdoc.read(fpath)


def _get_requirement(r_ref):
    """Returns a cached requirement.

    """
    r = _DOC_CACHE[r_ref.id]
    r.meta.type = r_ref.type

    return r


def _get_cached_documents(doc_type):
    """Returns cached document set.

    """
    return [i for i in _DOC_CACHE.values() if i.meta.type == doc_type]


def _map_requirement(i):
    """Returns a requirement document mapped to a dictionary.

    """
    def get_requirement_type():
        """Returns a shortened requirement type description.

        """
        if len(i.meta.type.split(":")) == 2:
            return i.meta.type.split(":")[1].replace("_", "-")
        elif isinstance(i, cim.v2.ForcingConstraint):
            return "forcing-constraint"
        elif isinstance(i, cim.v2.TemporalConstraint):
            return "temporal-constraint"
        elif isinstance(i, cim.v2.EnsembleRequirement):
            return "ensemble"
        elif isinstance(i, cim.v2.EnsembleRequirement):
            return "ensemble"
        elif isinstance(i, cim.v2.MultiEnsemble):
            return "multi-ensemble"

        return "unknown"


    result = OrderedDict()
    result['canonical_name'] = i.name
    result['description'] = i.description
    result['isConformanceRequested'] = i.is_conformance_requested
    result['keywords'] = i.keywords
    result['label'] = i.name
    if i.scope:
        result['scope'] = i.scope
    result['type'] = get_requirement_type()

    return result


def _map_experiment(i):
    """Returns an experiment document mapped to a dictionary.

    """
    i.requirements = [_get_requirement(j) for j in i.requirements]

    result = OrderedDict()
    result['canonical_name'] = i.canonical_name
    result['description'] = i.description
    result['governing_mips'] = sorted([j.canonical_name for j in i.governing_mips])
    result['keywords'] = i.keywords
    result['long_name'] = i.long_name
    result['mip_era'] = "cmip6"
    result['rationale'] = i.rationale
    result['related_experiments'] = sorted([{'name': j.name, 'relationship': j.relationship} for j in i.related_experiments])
    result['related_mips'] = sorted([j.canonical_name for j in i.related_mips])
    result['requirements'] = [_map_requirement(j) for j in i.requirements]
    result['tier'] = i.tier
    result['uid'] = i.meta.id
    result['viewerURL'] = _VIEWER_URL.format(i.canonical_name)

    return result


def _map_mip(i):
    """Returns an MIP document mapped to a dictionary.

    """
    result = OrderedDict()
    result['canonical_name'] = i.canonical_name
    result['description'] = i.description
    result['experiments'] = [j.name for j in i.required_experiments]
    result['keywords'] = i.keywords
    result['long_name'] = i.long_name
    result['label'] = i.name
    result['rationale'] = i.rationale
    result['uid'] = i.meta.id

    return result


def _load_cache(input_dir):
    """Caches set of documents for later processing.

    """
    for doc_type in {
        "cim.2.designing.EnsembleRequirement",
        "cim.2.designing.ForcingConstraint",
        "cim.2.designing.MultiEnsemble",
        "cim.2.designing.NumericalExperiment",
        "cim.2.designing.NumericalRequirement",
        "cim.2.designing.Project",
        "cim.2.designing.TemporalConstraint"
    }:
        for doc in _yield_documents(input_dir, doc_type):
            _DOC_CACHE[doc.meta.id] = doc


def _main(args):
    """Main entry point.

    """
    if not os.path.isdir(args.input_dir):
        raise ValueError("Input directory does not exist")
    if not os.path.isdir(args.output_dir):
        raise ValueError("Output directory does not exist")

    # Step 1: cache documents.
    _load_cache(args.input_dir)

    # Step 2: map experiments & write to file system.
    for i in _get_cached_documents('cim.2.designing.NumericalExperiment'):
        fpath = "{}/experiment_{}.json".format(args.output_dir, i.canonical_name.lower())
        with open(fpath, 'w') as fstream:
            fstream.write(json.dumps(_map_experiment(i), indent=4))

    # Step 3: map mip & write to file system.
    for i in _get_cached_documents('cim.2.designing.Project'):
        fpath = "{}/mip_{}.json".format(args.output_dir, i.canonical_name.lower())
        with open(fpath, 'w') as fstream:
            fstream.write(json.dumps(_map_mip(i), indent=4))

# Entry point.
if __name__ == '__main__':
    _main(_ARGS.parse_args())
