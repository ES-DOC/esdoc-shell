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



# Define command line argument parser.
_ARGS = argparse.ArgumentParser("Generates an institute's CMIP6 model IPython notebooks.")
_ARGS.add_argument(
    "--institution-id",
    help="An institution identifier",
    dest="institution_id",
    type=str
    )

# All institute filter.
_ALL_INSTITUTES = 'all'

# MIP era.
_MIP_ERA = "cmip6"

# Template cache.
_TEMPLATES_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "templates_ipynb")
_TEMPLATES = template.Loader(_TEMPLATES_PATH)



def _main(args):
    """Main entry point.

    """
    pyessv.log('Writing notebooks ... ', app='JHUB')
    for source_id, topic_id in _yield_config(args.institution_id):
        ctx = _ProcessingContextInfo(args.institution_id, source_id, topic_id)
        ctx.set_output()
        ctx.set_notebook()
        ctx.write()


def _yield_config(institution_id):
    """Returns set of notebooks to be generated.

    """
    # Test institutes.
    if institution_id in {'test-institute-1', 'test-institute-2', 'test-institute-3'}:
        for j in range(3):
            for k in pyessv.ESDOC.cmip6.get_model_topics():
                yield "sandbox-{}".format(j + 1), k.canonical_name

    # Instititutional notebooks.
    else:
        for i in pyessv.WCRP.cmip6.institution_id:
            if i.canonical_name != institution_id:
                continue

            # ... live
            for j in pyessv.WCRP.cmip6.get_institute_sources(i):
                for k in pyessv.ESDOC.cmip6.get_model_topics(j):
                    yield j.canonical_name, k.canonical_name

            # ... sandboxes
            for j in range(3):
                for k in pyessv.ESDOC.cmip6.get_model_topics():
                    yield "sandbox-{}".format(j + 1), k.canonical_name


class _ProcessingContextInfo(object):
    """Encpasulates information used during processing.

    """
    def __init__(self, institution_id, source_id, topic_id):
        """Instance initializer.

        """
        self.institution_id = institution_id
        self.source_id = source_id
        self.topic_id = topic_id
        self.output = None
        self.notebook = None


    def set_output(self):
        """Set notebook output.

        """
        # Set path to notebook output file.
        path = os.path.join(os.getenv('JH_ARCHIVE_HOME'), 'data')
        path = os.path.join(path, self.institution_id)
        path = os.path.join(path, _MIP_ERA)
        path = os.path.join(path, 'models')
        path = os.path.join(path, self.source_id)
        path = os.path.join(path, self.topic_id)
        path += '.json'

        # Set notebook output wrapper.
        self.output = NotebookOutput(
            _MIP_ERA,
            self.institution_id,
            self.source_id,
            self.topic_id,
            path=path
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
            print "ERROR: ", self.institution_id, self.source_id, self.topic_id, err
            self.notebook = content
        else:
            self.notebook = json.dumps(as_dict, indent=4)


    def write(self):
        """Write output to file system.

        """
        path = os.path.join(os.getenv('JH_HOME'), 'notebooks')
        path = os.path.join(path, self.institution_id)
        path = os.path.join(path, _MIP_ERA)
        path = os.path.join(path, 'models')
        path = os.path.join(path, self.source_id)
        if not os.path.isdir(path):
            os.makedirs(path)
        path = os.path.join(path, self.topic_id)
        path += '.ipynb'

        pyessv.log('generating --> {}'.format(path), app='SH')
        with open(path, 'w') as fstream:
            fstream.write(self.notebook)


# Main entry point.
if __name__ == '__main__':
    _main(_ARGS.parse_args())
