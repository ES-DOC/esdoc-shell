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
import shutil

from tornado import template

import pyessv
from pyesdoc.ipython.model_topic import NotebookOutput



# Define command line options.
_ARGS = argparse.ArgumentParser("Writes CMIP6 IPython notebooks.")
_ARGS.add_argument(
    "--institute",
    help="CMIP6 institute identier (* for all).",
    dest="institute",
    type=str
    )
_ARGS = _ARGS.parse_args()

# All institute filter.
_ALL_INSTITUTES = 'all'

# Template cache.
_TEMPLATES = template.Loader(os.path.join(os.path.dirname(os.path.abspath(__file__)), "templates"))

# MIP era.
_MIP_ERA = "cmip6"

# Test institute / source id.
_TEST_INSTITUTE = "test-institute"
_TEST_SOURCE_ID = "test-model"


def _main():
    """Main entry point.

    """
    ctx = _ProcessingContextInfo()
    for info in sorted(_get_config(_ARGS.institute)):
        ctx.set_info(info)
        ctx.set_output()
        ctx.set_notebook()
        ctx.write()


class _ProcessingContextInfo(object):
    """Encpasulates information used during processing.

    """
    def __init__(self):
        """Instance initializer.

        """
        self.institution_id = None
        self.output = None
        self.output_dir = os.path.join(os.getenv('ESDOC_HOME'), 'repos/esdoc-jupyterhub')
        self.source_id = None
        self.specialization_id = None


    def set_info(self, info):
        """Set information related to notebook about to be emitted.

        """
        self.institution_id, self.source_id, self.specialization_id = info
        self.output = self.notebook = None


    def set_output(self):
        """Set notebook output.

        """
        self.output = NotebookOutput(
            _MIP_ERA,
            self.institution_id,
            self.source_id,
            self.specialization_id,
            self.output_dir
            )


    def set_notebook(self):
        """Set notebook.

        """
        # Load template.
        tmpl = _TEMPLATES.load("model-realm.tornado")

        # Generate content.
        content = tmpl.generate(
            DOC=self.output,
            escape=lambda s: s.strip().replace('"', "'"),
            now=dt.datetime.now(),
            t=self.output.specialization
            )

        # Set notebook.
        try:
            as_dict = json.loads(content)
        except ValueError as err:
            print "ERROR: ", self.institution_id, self.source_id, self.specialization_id, err
            self.notebook = content
        else:
            self.notebook = json.dumps(as_dict, indent=4)


    def write(self):
        """Write output to file system.

        """
        dpath = os.path.dirname(self.output.fpath)
        if not os.path.isdir(dpath):
            os.makedirs(dpath)
        fpath = os.path.join(dpath, "{}.ipynb".format(self.output.specialization.name))
        with open(fpath, 'w') as fstream:
            fstream.write(self.notebook)


    def get_notebook(self):
        """Load notebook JSON content.

        """
        # Load template.
        tmpl = _TEMPLATES.load("model-realm.tornado")

        # Generate content.
        content = tmpl.generate(
            DOC=self.output,
            escape=lambda s: s.strip().replace('"', "'"),
            now=dt.datetime.now(),
            r=self.output.specialization
            )

        try:
            as_dict = json.loads(content)
        except ValueError as err:
            print "ERROR: ", self.institution_id, self.source_id, self.specialization_id, err
            # Return raw content.
            return content
        else:
            # Return prettified content.
            return json.dumps(as_dict, indent=4)


def _get_config(institute_filter):
    """Returns set of notebooks to be generated.

    """
    result = set()

    # Load CMIP6 vocabularies.
    institutes, sources, realms = \
        pyessv.load('wcrp:cmip6:institution-id'), \
        pyessv.load('wcrp:cmip6:source-id'), \
        pyessv.load('wcrp:cmip6:realm')
    if institute_filter != _ALL_INSTITUTES:
        institutes = [i for i in institutes if i.canonical_name == institute_filter]

    # 1 notebook per test institute / topic combination.
    if institute_filter in {_ALL_INSTITUTES, 'test'}:
        for i in range(3):
            institute_id = '{}-{}'.format(_TEST_INSTITUTE, i + 1)
            source_id = '{}-{}'.format(_TEST_SOURCE_ID, i + 1)
            result.add((institute_id, source_id, "toplevel"))
            for realm in realms:
                result.add((institute_id, source_id, realm.canonical_name))

    # 1 notebook per institution_id / source_id / toplevel combination:
    for institute in institutes:
        for source in [i for i in sources if institute.label in i.data['institution_id']]:
            result.add((institute.canonical_name, source.canonical_name, 'toplevel'))

    # 1 notebook per institution_id / source_id / topic combination:
    for institute in institutes:
        for source in [i for i in sources if institute.label in i.data['institution_id']]:
            for realm in [i for i in realms if i.raw_name in source.data['model_component']]:
                result.add((institute.canonical_name, source.canonical_name, realm.canonical_name))

    # 1 notebook per institution_id / sandbox / topic combination:
    for institute in institutes:
        for i in range(2):
            source_id = "sandbox-{}".format(i + 1)
            result.add((institute.canonical_name, source_id, 'toplevel'))
            for realm in realms:
                result.add((institute.canonical_name, source_id, realm.canonical_name))

    return result


# Entry point.
_main()
