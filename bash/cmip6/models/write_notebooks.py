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

import pyessv
from pyesdoc.ipython.model_realm_properties import NotebookOutput



# Command line options.
_ARGS = argparse.ArgumentParser("Writes CMIP6 IPython model notebooks to file system.")

# Template cache.
_TEMPLATES = template.Loader(os.path.join(os.path.dirname(os.path.abspath(__file__)), "templates"))

# MIP era.
_MIP_ERA = "cmip6"

# Map of realm names to specialization repo & source id attribute.
_REALMS = {
    'aerosol': {
        'is_active': False,
        'source_id_attr': 'aerosol',
    },
    'atmos': {
        'is_active': True,
        'source_id_attr': 'atmosphere',
    },
    'atmoschem': {
        'is_active': False,
        'source_id_attr': 'atmospheric_chemistry',
    },
    'land': {
        'is_active': False,
        'source_id_attr': 'land_surface',
    },
    'landice': {
        'is_active': False,
        'source_id_attr': 'land_ice',
    },
    'ocean': {
        'is_active': True,
        'source_id_attr': 'ocean',
    },
    'ocnbgchem': {
        'is_active': True,
        'source_id_attr': 'ocean_biogeochemistry',
    },
    'seaice': {
        'is_active': True,
        'source_id_attr': 'sea_ice',
    }
}

# Test institute / source id.
_TEST_INSTITUTE = "test-institute"
_TEST_SOURCE_ID = "test-model"


def _main(args):
    """Main entry point.

    """
    ctx = _ProcessingContextInfo()
    for idx, info in enumerate(sorted(_get_config())):
        ctx.set_info(info)
        # print "writing notebook {} :: {}/{}/{}/{}".format(idx + 1, _MIP_ERA, ctx.institution_id, ctx.source_id, ctx.specialization_id)
        ctx.set_output()
        ctx.set_notebook()
        ctx.write()

class _ProcessingContextInfo(object):
    def __init__(self):
        """Instance initializer.

        """
        self.institution_id = None
        self.output = None
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
            self.specialization_id
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


def _get_config():
    """Returns set of notebooks to be generated.

    """
    result = set()

    # Load CMIP6 vocabularies.
    cv_institution_id, cv_source_id, cv_realm = \
        pyessv.load('wcrp', 'cmip6', 'institution-id'), \
        pyessv.load('wcrp', 'cmip6', 'source-id'), \
        pyessv.load('wcrp', 'cmip6', 'realm')
    cv_realm = [i for i in cv_realm if _REALMS[i.name]['is_active']]

    # Add test related notebook info.
    for i in range(3):
        institute_id = '{}-{}'.format(_TEST_INSTITUTE, i + 1)
        source_id = '{}-{}'.format(_TEST_SOURCE_ID, i + 1)
        result.add((institute_id, source_id, "toplevel"))
        for realm in cv_realm:
            result.add((institute_id, source_id, realm.name))

    # For each source_id, institution_id combination:
    for institution_id in cv_institution_id:
        for source_id in cv_source_id:
            # ... exclude unsupported insitutes;
            if institution_id.label not in source_id.data['institution_id']:
                continue
            # ... emit top-level + realms;
            result.add((institution_id.name, source_id.name, 'toplevel'))
            for realm in cv_realm:
                result.add((institution_id.name, source_id.name, realm.name))

    return result


# Entry point.
if __name__ == '__main__':
    _main(_ARGS.parse_args())
