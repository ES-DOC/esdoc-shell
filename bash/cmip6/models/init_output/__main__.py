# -*- coding: utf-8 -*-

"""
.. module:: write_model_notebooks.py
   :license: GPL/CeCIL
   :platform: Unix, Windows
   :synopsis: Writes CMIP6 IPython model notebooks to file system.

.. moduleauthor:: Mark Conway-Greenslade <momipsl@ipsl.jussieu.fr>

"""
import argparse

import pyesdoc
import pyessv

import defaults
import mappings
import mapper



# Define command line argument parser.
_ARGS = argparse.ArgumentParser("Initializes a CMIP6 model output JSON file.")
_ARGS.add_argument(
    "--institution-id",
    help="An institution identifier",
    dest="institution_id",
    type=str
    )


def _main(args):
    """Main entry point.

    """
    pyessv.log('initialising {} ...'.format(args.institution_id), app='SH')

    _init(args.institution_id)

    pyessv.log('Processing archived CMIP5 model documentation:')
    for cmip5_model_id, cmip5_component, cmip6_institution_id, cmip6_source_id, cmip6_topic in _yield_targets():
        nb_output = mapper.map(cmip5_model_id, cmip5_component, cmip6_institution_id, cmip6_source_id, cmip6_topic)
        nb_output.save()
        pyessv.log('... {};'.format(nb_output.fpath))


def _init(institution_id):
    """Initialises sub-modules.

    """
    pyesdoc.archive.init()
    mappings.init()
    defaults.init(institution_id)


def _yield_targets():
    """Yields targets to be processed.

    """
    for m in pyesdoc.archive.yield_latest_documents("cmip5", "metafor-q", "cim-1-software-modelcomponent"):
        for cmip5_institute, cmip5_model_id, cmip6_institution_id, cmip6_source_id, cmip6_topic in sorted(defaults.DEFAULTS):
            # Escape if institute \ model mismatch.
            if mappings.get_cmip5_institute_id(m) != cmip5_institute or \
               mappings.get_cmip5_model_id(m) != cmip5_model_id:
               continue

            # Emit toplevel.
            if cmip6_topic == 'toplevel':
                yield((cmip5_model_id, m, cmip6_institution_id, cmip6_source_id, cmip6_topic))

            # Emit realms.
            else:
                for c in m.sub_components:
                    cmip5_component = mappings.get_cmip5_component_id(c)
                    if cmip5_component in mappings.REALM_MAPPINGS and mappings.REALM_MAPPINGS[cmip5_component] == cmip6_topic:
                        yield((cmip5_model_id, c, cmip6_institution_id, cmip6_source_id, cmip6_topic))


_main(_ARGS.parse_args())
