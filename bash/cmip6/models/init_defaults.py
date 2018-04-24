# -*- coding: utf-8 -*-

"""
.. module:: init_defaults.py
   :license: GPL/CeCIL
   :platform: Unix, Windows
   :synopsis: Initializes a CMIP6 model-initialization.json file.

.. moduleauthor:: Mark A. Conway-Greenslade


"""
import argparse
import collections
import json
import os

import pyessv



# Define command line argument parser.
_ARGS = argparse.ArgumentParser("Initializes a CMIP6 model-initialization.json file.")
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
    institution_id = _get_institution_id(args.institution_id)
    fpath = _get_fpath(args.institution_id)
    content = _get_content(institution_id)

    if not os.path.isdir(os.path.dirname(fpath)):
        os.makedirs(os.path.dirname(fpath))
    with open(fpath, 'w') as fstream:
        fstream.write(json.dumps(content, indent=4))


def _get_institution_id(institution_id):
    """Returns institution vocab term.

    """
    if institution_id in {'test-institute-1', 'test-institute-2', 'test-institute-3'}:
        return institution_id

    term = pyessv.WCRP.cmip6.institution_id[institution_id]
    if term is None:
        raise ValueError('{} is invalid'.format(institution_id))

    return term


def _get_fpath(institution_id):
    """Returns path to an institutes model-default.json.

    """
    fpath = os.getenv('ESDOC_HOME')
    fpath = os.path.join(fpath, 'repos')
    fpath = os.path.join(fpath, 'institutional')
    fpath = os.path.join(fpath, institution_id)
    if not os.path.isdir(fpath):
        raise ValueError('{} GitHub repo does not exist.'.format(institution_id))

    fpath = os.path.join(fpath, 'cmip6')
    fpath = os.path.join(fpath, 'models')
    fpath = os.path.join(fpath, 'model-initialization.json')
    if os.path.isfile(fpath):
        raise ValueError('{} model-initialization.json file already exists.'.format(institution_id))

    return fpath


def _get_content(institution_id):
    """Returns content to be written to file system.

    """
    obj = collections.OrderedDict()
    if institution_id in {'test-institute-1', 'test-institute-2', 'test-institute-3'}:
        for i in range(3):
            source_id = 'sandbox-{}'.format(i + 1)
            obj[source_id] = collections.OrderedDict()
            for realm in pyessv.WCRP.cmip6.get_source_realms():
                obj[source_id][realm.canonical_name] = collections.OrderedDict([
                    ('initializedFrom', 'cmip5:mohc:hadgem2-es')
                ])
            obj[source_id]['toplevel'] = collections.OrderedDict([
                ('initializedFrom', 'cmip5:mohc:hadgem2-es')
            ])
    else:
        for source_id in pyessv.WCRP.cmip6.get_institute_sources(institution_id):
            obj[source_id.canonical_name] = collections.OrderedDict()
            for realm in pyessv.WCRP.cmip6.get_source_realms(source_id):
                obj[source_id.canonical_name][realm.canonical_name] = collections.OrderedDict([
                    ('initializedFrom', '')
                ])
            obj[source_id.canonical_name]['toplevel'] = collections.OrderedDict([
                ('initializedFrom', '')
            ])

    return obj


# Main entry point.
if __name__ == '__main__':
    _main(_ARGS.parse_args())
