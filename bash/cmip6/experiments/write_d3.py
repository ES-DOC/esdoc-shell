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
_CIM_CACHE = {}

# Cache of experiment definitions to be written to file system.
_OUTPUT = {}

# Viewer url.
_VIEWER_URL = "http://view.es-doc.org?renderMethod=id&project=cmip6&id={}&version=latest&client=esdoc"

# Map of document types to node types.
_NODE_TYPES = {
    cim.v2.Project: "p",
    cim.v2.NumericalExperiment: "e",
    cim.v2.ForcingConstraint: "r:fc",
    cim.v2.TemporalConstraint: "r:tc",
    cim.v2.EnsembleRequirement: "r:e",
    cim.v2.MultiEnsemble: "r:me",
}

# CIM types of interest.
_CIM_CITATION = "cim.2.shared.Citation"
_CIM_ENSEMBLE_REQUIREMENT = "cim.2.designing.EnsembleRequirement"
_CIM_FORCING_CONSTRAINT = "cim.2.designing.ForcingConstraint"
_CIM_MULTI_ENSEMBLE = "cim.2.designing.MultiEnsemble"
_CIM_NUMERICAL_EXPERIMENT = "cim.2.designing.NumericalExperiment"
_CIM_NUMERICAL_REQUIREMENT = "cim.2.designing.NumericalRequirement"
_CIM_PROJECT = "cim.2.designing.Project"
_CIM_TEMPORAL_CONSTRAINT = "cim.2.designing.TemporalConstraint"

_CIM_TYPES = {
    _CIM_CITATION,
    _CIM_ENSEMBLE_REQUIREMENT,
    _CIM_FORCING_CONSTRAINT,
    _CIM_MULTI_ENSEMBLE,
    _CIM_NUMERICAL_EXPERIMENT,
    _CIM_NUMERICAL_REQUIREMENT,
    _CIM_PROJECT,
    _CIM_TEMPORAL_CONSTRAINT
}


def _yield_documents(input_dir, doc_type):
    """Yields set of document for further processing.

    """
    for fpath in glob.iglob("{}/{}*.*".format(input_dir, doc_type)):
        yield pyesdoc.read(fpath)


def _init_cache(input_dir):
    """Caches set of documents for later processing.

    """
    for doc_type in _CIM_TYPES:
        for doc in _yield_documents(input_dir, doc_type):
            doc._ID = len(_CIM_CACHE)
            _CIM_CACHE[doc.meta.id] = doc


def _get_requirement(r_ref):
    """Returns a cached requirement.

    """
    r = _CIM_CACHE[r_ref.id]
    r.meta.type = r_ref.type

    return r


def _get_cached_documents(doc_type):
    """Returns cached document set.

    """
    return [i for i in _CIM_CACHE.values() if i.meta.type == doc_type]


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


def _get_associations():
    """Returns mesh of document associations.

    """
    associations = collections.defaultdict(list)
    for p in _get_cached_documents("cim.2.designing.Project"):
        for e in p.required_experiments:
            # associations["p:e"].append((p.meta.id, e.id))
            associations["p:e"].append((p._ID, _CIM_CACHE[e.id]._ID))
        for c in p.citations:
            # associations["p:c"].append((p.meta.id, c.id))
            associations["p:c"].append((p._ID, _CIM_CACHE[c.id]._ID))

    for e in _get_cached_documents("cim.2.designing.NumericalExperiment"):
        for c in e.citations:
            associations["e:c"].append((e._ID, _CIM_CACHE[c.id]._ID))
            # associations["e:c"].append((e.meta.id, c.id))
        for re in e.related_experiments:
            associations["e:e"].append((e._ID, _CIM_CACHE[re.id]._ID))
            # associations["e:e"].append((e.meta.id, re.id))
        for rm in e.related_mips:
            associations["e:p"].append((e._ID, _CIM_CACHE[rm.id]._ID))
            # associations["e:p"].append((e.meta.id, rm.id))

    return associations


def _get_legend():
    """Returns legend of node types.

    """
    return {
        'p': 'A MIP, e.g. FAFMIP',
        'e': 'A numerical experiment, e.g. amip',
        'c': 'A Citation',
        'r': 'An experimental requirement',
        'r:fc': 'A forcing constraint experimental requirement',
        'r:tc': 'A temporal constraint experimental requirement',
        'r:e': 'An ensemble experimental requirement',
        'r:me': 'An multi-ensemble experimental requirement'
    }


def _get_nodes():
    """Returns nodes, i.e. minimal info about relevant CIM entities.

    """
    def get_node_label(i):
        if isinstance(i, cim.v2.Citation):
            return i.title
        return i.name

    def _get_nodeset(doc_type):
        return [(i._ID, i.meta.id, get_node_label(i)) for i in _get_cached_documents(doc_type)]

    return {
        'c': _get_nodeset(_CIM_CITATION),
        'p': _get_nodeset(_CIM_PROJECT),
        'e': _get_nodeset(_CIM_NUMERICAL_EXPERIMENT)
    }


def _main(args):
    """Main entry point.

    """
    if not os.path.isdir(args.input_dir):
        raise ValueError("Input directory does not exist")
    if not os.path.isdir(args.output_dir):
        raise ValueError("Output directory does not exist")

    # Step 1: set inputs.
    _init_cache(args.input_dir)

    # Step 2: set output.
    output = {
        "legend": _get_legend(),
        "nodes": _get_nodes(),
        "associations": _get_associations()
    }

    # Step 3: write output to file system.
    fpath = "{}/cmip6.experiments.d3.json".format(args.output_dir)
    with open(fpath, 'w') as fstream:
        fstream.write(json.dumps(output))


# Entry point.
if __name__ == '__main__':
    _main(_ARGS.parse_args())
