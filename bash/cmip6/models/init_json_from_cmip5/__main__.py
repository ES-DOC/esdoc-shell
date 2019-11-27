# -*- coding: utf-8 -*-

"""
.. module:: write_model_notebooks.py
   :license: GPL/CeCIL
   :platform: Unix, Windows
   :synopsis: Writes CMIP6 IPython model notebooks to file system.

.. moduleauthor:: Mark Conway-Greenslade <momipsl@ipsl.jussieu.fr>

"""
import argparse

import pyessv

from cmip6.utils import logger
from cmip6.utils import vocabs

import cmip5_documents
import defaults
import mappings
import mapper


# Define command line argument parser.
_ARGS = argparse.ArgumentParser("Generates CMIP6 output file from CMIP5 model documents.")
_ARGS.add_argument(
    "--institution-id",
    help="An institution identifier",
    dest="institution_id",
    type=str,
    default="all"
    )


def _main(args):
    """Main entry point.

    """
    # Initialise CMIP5 to CMIP6 mappings.
    mappings.init()

    # Write a JSON file for each CMIP6 institute | CMIP5 document combination.
    for institution_id in vocabs.get_institutes():
        if not args.institution_id in ["all", institution_id.canonical_name]:
            continue
        if not cmip5_documents.init(institution_id.canonical_name):
            continue
        for output in _yield_outputs(institution_id):
            output.save()
            logger.log('... {};'.format(output.fpath))


def _yield_outputs(institution_id):
    """Yields set of output documents.

    """
    defaults.init(institution_id.canonical_name)
    for mapping_info in _yield_mapping_targets():
        yield mapper.map(mapping_info)


def _yield_mapping_targets():
    """Yields targets to be processed.

    """
    for cmip5_institute, cmip5_model_id, cmip6_institution_id, cmip6_source_id, cmip6_topic in sorted(defaults.DEFAULTS):
        for m in cmip5_documents.DOCUMENTS:
            # Escape if institute \ model mismatch.
            if mappings.get_cmip5_institute_id(m) != cmip5_institute or \
               mappings.get_cmip5_model_id(m) != cmip5_model_id:
               continue

            # Emit toplevel.
            if cmip6_topic == 'toplevel':
                yield mapper.MappingInfo(cmip5_model_id, m, cmip6_institution_id, cmip6_source_id, cmip6_topic)

            # Emit realms.
            else:
                for c in m.sub_components:
                    cmip5_component = mappings.get_cmip5_component_id(c)
                    if cmip5_component in mappings.REALM_MAPPINGS and mappings.REALM_MAPPINGS[cmip5_component] == cmip6_topic:
                        yield mapper.MappingInfo(cmip5_model_id, c, cmip6_institution_id, cmip6_source_id, cmip6_topic)


# Entry point.
_main(_ARGS.parse_args())
