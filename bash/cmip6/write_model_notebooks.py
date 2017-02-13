# -*- coding: utf-8 -*-

"""
.. module:: write_model_notebooks.py
   :license: GPL/CeCIL
   :platform: Unix, Windows
   :synopsis: Writes CMIP6 IPython model notebooks to file system.

.. moduleauthor:: Mark Conway-Greenslade <momipsl@ipsl.jussieu.fr>

"""
import argparse
import datetime as dt
import json
import os

from tornado import template

import pyesdoc
from pyesdoc.ipython.model_realm_properties import NotebookOutput
from pyesdoc.cv.archive import load_collection as load_cv_collection
from pyesdoc.cv.model import Collection



# Command line options.
_ARGS = argparse.ArgumentParser("Writes CMIP6 IPython model notebooks to file system.")
_ARGS.add_argument(
    "--output",
    help="Path to a directory into which notebooks will be written.",
    dest="output_dir",
    type=str
    )
_ARGS.add_argument(
    "--cfg",
    help="Path to a confguration file driving which notebooks will be written.",
    dest="cfg_fpath",
    type=str,
    default="{}.conf".format(__file__.split(".")[0])
    )

# Template cache.
_TEMPLATES = template.Loader(os.path.join(os.path.dirname(os.path.abspath(__file__)), "templates"))


def _main(args):
    """Main entry point.

    """
    # Validate inputs.
    if not os.path.isdir(args.output_dir):
        raise ValueError("Output directory does not exist")
    if not os.path.isfile(args.cfg_fpath):
        raise ValueError("Configration file does not exist")

    # Read CMIP6 JSON/CV
    models = _get_cv()

    # should be pulled in from someplace else, not set here
    mip_era = 'cmip6'

    # For each institute / model / realm combination, emit a notebook.
    for institute, model, realms in [(i['institute'], i['name'], i['realms']) for i in models]:
        for realm in realms:
            # ... load output;
            output = _get_output(args.output_dir, mip_era, institute, model, realm)

            # ... write notebook;
            _write(output)


def _get_output(output_dir, mip_era, institute, source_id, realm):
    """Returns notebook output data wrapper.

    """
    return NotebookOutput(
        mip_era,
        institute,
        source_id,
        realm,
        os.path.join(output_dir, "output")
        )


def _write(output):
    """Writes notebook to file system.

    """
    fpath = output.fpath.replace("output", "notebooks")
    fpath = fpath.replace(".json", ".ipynb")
    if not os.path.isdir(os.path.dirname(fpath)):
        os.makedirs(os.path.dirname(fpath))
    with open(fpath, 'w') as fstream:
        fstream.write(_get_notebook(output))


def _get_notebook(data):
    """Returns notebook content.

    """
    # Load template.
    tmpl = _TEMPLATES.load("model-realm.tornado")

    # Generate content.
    content = tmpl.generate(
        DOC=data,
        escape=lambda s: s.strip().replace('"', "'"),
        now=dt.datetime.now(),
        r=data.specialization
        )

    # Return prettified content.
    return json.dumps(json.loads(content), indent=4)


def _get_cv():
    models = []

    # possible realms- should be set to definitive list, not this
    #realms = ['aerosol', 'atmosphere', 'atmospheric_chemistry', 'land_ice',
    #          'land_surface', 'ocean', 'ocean_biogeochemistry', 'sea_ice']
    # should work, but sea_ice / seaice
    #realms = ['atmosphere', 'ocean', 'sea_ice']
    realms = ['atmosphere', 'ocean']

    # get the CMIP6 source_id JSON
    cv_models = load_cv_collection('wcrp', 'cmip6', 'source-id')
    assert isinstance(cv_models, Collection)

    # for each participating model, record the name, institutes, and realms simulated
    for cv_model in cv_models.terms:

        # foreach institute that runs the model
        for institute in cv_model.data['institution_id']:
            model = dict()
            model['name'] = cv_model.data['source_id'].lower()
            model['institute'] = institute.lower()
            model['realms'] = []
            for realm in realms:
                if (cv_model.data[realm] and cv_model.data[realm] != 'None'):
                    model['realms'].append(realm)

            models.append(model)

    return models

# Entry point.
if __name__ == '__main__':
    _main(_ARGS.parse_args())
