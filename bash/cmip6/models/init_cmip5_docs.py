# -*- coding: utf-8 -*-

"""
.. module:: init_cmip5_docs.py
   :license: GPL/CeCIL
   :platform: Unix, Windows
   :synopsis: Initializes CMIP5 model documents.

.. moduleauthor:: Mark A. Conway-Greenslade


"""
import os

import pyesdoc

from cmip6.utils import logger



# CMIP5 to CMIP6 institute mappings.
_INSTITUTE_MAPPINGS = {
    'csiro-bom': 'csiro-arccss-bom',
    'csiro-qccce': 'csiro',
    'ec-earth': 'ec-earth-consortium',
    'lasg-cess': 'thu'
    }


def _main():
    """Main entry point.

    """
    for m, institution_id, model_id, repo in _yield_targets():
        if not os.path.exists(repo):
            logger.log_warning('unmappable cmip5 institution: {}'.format(model_id))
            continue
        _write(m, institution_id, model_id, repo)


def _write(m, institution_id, model_id, repo):
    """Writes a model to the file system.

    """
    fpath = os.path.join(repo, 'cmip5')
    fpath = os.path.join(fpath, 'models')
    fpath = os.path.join(fpath, model_id)
    fpath = os.path.join(fpath, 'cim')
    if not os.path.isdir(fpath):
        os.makedirs(fpath)
    fname = 'cmip5_{}_{}.json'.format(institution_id, model_id)
    fpath = os.path.join(fpath, fname)

    pyesdoc.write(m, fpath)


def _yield_targets():
    """Yields model documents to be processed.

    """
    pyesdoc.archive.init()
    for m in pyesdoc.archive.yield_latest_documents("cmip5", "metafor-q", "cim-1-software-modelcomponent"):
        institution_id = _get_cmip6_institute_id(m)
        model_id = _get_cmip5_model_id(m)
        repo = _get_institution_repo(institution_id)
        yield m, institution_id, model_id, repo


def _get_cmip6_institute_id(m):
    """Returns CMIP6 institute identifier mapped from a CMIP5 document.

    """
    identifier = m.meta.institute.lower()

    return _INSTITUTE_MAPPINGS.get(identifier, identifier)


def _get_cmip5_model_id(m):
    """Returns CMIP5 model identifier mapped from a CMIP5 document.

    """
    return m.short_name.lower()


def _get_institution_repo(institution_id):
    """Returns path to institutional repo.

    """
    fpath = os.getenv('ESDOC_HOME')
    fpath = os.path.join(fpath, 'repos')
    fpath = os.path.join(fpath, 'institutional')
    fpath = os.path.join(fpath, institution_id)

    return fpath


# Main entry point.
if __name__ == '__main__':
    _main()
