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


def _map_requirements(i):
    """Returns a collection of mapped requirements.

    """
    result = dict()
    for j in i.required_experiments:
        j = _DOC_CACHE_2[cim.NumericalExperiment][j.canonical_name]
        for k in j.requirements:
            result[k.canonical_name] = _map_requirement(k)

    return result


def _map_requirement(i):
    """Returns a requirement document mapped to a dictionary.

    """
    def get_requirement_type():
        """Returns a shortened requirement type description.

        """
        try:
            return _REQUIREMENT_TYPE_KEYS[type(i)]
        except KeyError:
            if len(i.meta.type.split(":")) == 2:
                return i.meta.type.split(":")[1].replace("_", "-")
            return "unknown"

    # Set associated data-link.
    data_link = None
    try:
        i.data_link
    except AttributeError:
        pass
    else:
        if i.data_link is not None:
            data_link = i.data_link.availability[0].name

    result = collections.OrderedDict()
    result['canonical_name'] = i.canonical_name
    if data_link:
        result['data_link'] = data_link
    result['description'] = i.description
    result['isConformanceRequested'] = i.is_conformance_requested
    result['keywords'] = i.keywords
    result['label'] = i.name
    # if i.scope:
    result['scope'] = i.scope
    result['type'] = get_requirement_type()
    result['uid'] = i.meta.id

    return result


def _map_experiments(i):
    """Returns a collection of mapped experiments.

    """
    return {j.canonical_name: _map_experiment(j.canonical_name) \
            for j in i.required_experiments}


def _map_experiment(canonical_name):
    """Returns an experiment document mapped to a dictionary.

    """
    i = _DOC_CACHE_2[cim.NumericalExperiment][canonical_name]

    i.requirements = [_get_requirement(j) for j in i.requirements]

    result = collections.OrderedDict()
    result['canonical_name'] = i.canonical_name
    result['description'] = i.description
    result['governing_mips'] = [j.canonical_name for j in i.governing_mips]
    result['keywords'] = i.keywords
    result['long_name'] = i.long_name
    result['mip_era'] = "cmip6"
    result['rationale'] = i.rationale
    result['related_experiments'] = [{'name': j.name, 'relationship': j.relationship} for j in i.related_experiments]
    result['related_mips'] = [j.canonical_name for j in i.related_mips]
    result['requirements'] = [j.canonical_name for j in i.requirements]
    result['tier'] = i.tier
    result['uid'] = i.meta.id
    result['viewerURL'] = _VIEWER_URL.format("experiments", i.canonical_name)

    return result


def _map_data_links(i):
    result = dict()
    for j in i.required_experiments:
        j = _DOC_CACHE_2[cim.NumericalExperiment][j.canonical_name]
        for k in j.requirements:
            try:
                k.data_link
            except AttributeError:
                pass
            else:
                if k.data_link is not None:
                    result[k.data_link.availability[0].name] = _map_data_link(k.data_link)

    return result


def _map_data_link(i):
    result = dict()
    result['description'] = i.availability[0].description
    result['linkage'] = i.availability[0].linkage
    result['name'] = i.availability[0].name
    result['protocol'] = i.availability[0].protocol

    return result


def _map_mip(i):
    """Returns an MIP document mapped to a dictionary.

    """
    result = collections.OrderedDict()
    result['canonical_name'] = i.canonical_name
    result['description'] = i.description
    result['experiments'] = [j.canonical_name for j in i.required_experiments]
    result['keywords'] = i.keywords
    result['long_name'] = i.long_name
    result['label'] = i.name
    result['rationale'] = i.rationale
    result['uid'] = i.meta.id
    result['viewerURL'] = _VIEWER_URL.format("mips", i.canonical_name)

    return result


def _get_output(i):
    """Returns output to be written to file system.

    """
    result = collections.OrderedDict()
    result['mip'] = _map_mip(i)
    result['experiments'] = _map_experiments(i)
    result['requirements'] = _map_requirements(i)
    result['data_links'] = _map_data_links(i)

    return result


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


def _main(args):
    """Main entry point.

    """
    if not os.path.isdir(args.input_dir):
        raise ValueError("Input directory does not exist")
    if not os.path.isdir(args.output_dir):
        raise ValueError("Output directory does not exist")

    # Step 1: cache documents.
    _load_cache(args.input_dir)

    # Step 2: map mip & write to file system.
    for i in _DOC_CACHE_2[cim.Project].values():
        fpath = "{}/{}.json".format(args.output_dir, i.canonical_name.lower())
        with open(fpath, 'w') as fstream:
            fstream.write(json.dumps(_get_output(i), indent=4))


# Entry point.
if __name__ == '__main__':
    _main(_ARGS.parse_args())
