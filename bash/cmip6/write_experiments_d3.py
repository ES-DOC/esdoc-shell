# -*- coding: utf-8 -*-

"""
.. module:: run_publish_cmip6_documents.py
   :license: GPL/CeCIL
   :platform: Unix, Windows
   :synopsis: Publishes CMIP6 documents from the CMIP6 experiment spreadsheet.

.. moduleauthor:: Mark Conway-Greenslade <momipsl@ipsl.jussieu.fr>

"""
import argparse
import collections
import glob
import json
import os

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
_VIEWER_URL = "http://view.es-doc.org?renderMethod=id&project=cmip6-draft&id={}&version=latest&client=esdoc"

# Map of document types to node types.
_NODE_TYPES = {
    cim.v2.Project: "p",
    cim.v2.NumericalExperiment: "e",
    cim.v2.ForcingConstraint: "r:fc",
    cim.v2.TemporalConstraint: "r:tc",
    cim.v2.EnsembleRequirement: "r:e",
    cim.v2.MultiEnsemble: "r:me",
}


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


    result = collections.OrderedDict()
    result['canonical_name'] = i.name
    result['description'] = i.description
    result['isConformanceRequested'] = i.is_conformance_requested
    result['keywords'] = i.keywords
    result['label'] = i.name
    result['type'] = get_requirement_type()

    return result


def _map_related_experiment(i):
    """Returns a related experiment document mapped to a dictionary.

    """
    result = collections.OrderedDict()
    result['canonical_name'] = i.name
    result['mip_era'] = "cmip6"
    result['uid'] = i.id
    result['viewerURL'] = _VIEWER_URL.format(i.id)

    return result


def _get_nodes(doc_type):
    return [(i.meta.id, i.name) for i in _get_cached_documents(doc_type)]


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


def _set_project_associations(associations):
    for p in _get_cached_documents("cim.2.designing.Project"):
        for e in p.requires_experiments:
            associations["p:e"].append((p.meta.id, e.id))
        for c in p.citations:
            associations["p:c"].append((p.meta.id, c.id))

    for e in _get_cached_documents("cim.2.designing.NumericalExperiment"):
        for c in e.citations:
            associations["e:c"].append((e.meta.id, c.id))
        for re in e.related_experiments:
            associations["e:e"].append((e.meta.id, re.id))
        for rm in e.related_mips:
            associations["e:p"].append((e.meta.id, rm.id))


def _main(args):
    """Main entry point.

    """
    if not os.path.isdir(args.input_dir):
        raise ValueError("Input directory does not exist")
    if not os.path.isdir(args.output_dir):
        raise ValueError("Output directory does not exist")

    # Step 1: cache documents.
    _load_cache(args.input_dir)

    # Step 2: set nodes.
    nodes = {
        'p': _get_nodes('cim.2.designing.Project'),
        'e': _get_nodes('cim.2.designing.NumericalExperiment'),
    }

    # Step 2: set associations.
    associations = collections.defaultdict(list)
    _set_project_associations(associations)

    fpath = "{}/cmip6.experiments.d3.json".format(args.output_dir)
    with open(fpath, 'w') as fstream:
        fstream.write(json.dumps({
        "nodes": nodes,
        "associations": associations
    }))


# Entry point.
if __name__ == '__main__':
    _main(_ARGS.parse_args())
