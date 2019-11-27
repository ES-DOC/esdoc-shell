"""
.. module:: verify_repos.py
   :license: GPL/CeCIL
   :platform: Unix, Windows
   :synopsis: Verifies that all CMIP6 instituional repos exist.

.. moduleauthor:: Mark Conway-Greenslade <momipsl@ipsl.jussieu.fr>

"""
import argparse
import os

import pyessv

from cmip6.utils import io_mgr
from cmip6.utils import logger
from cmip6.utils import vocabs



# Define command line argument parser.
_ARGS = argparse.ArgumentParser("Scans & validates institutional repos.")
_ARGS.add_argument(
    "--institution-id",
    help="An institution identifier",
    dest="institution_id",
    type=str
    )

# Set of expected sub-folders.
SUB_FOLDERS = (
    'citations',
    'citations/json',
    'models',
    'responsible_parties',
    'responsible_parties/json'
    )

# Set of expected static files.
STATIC_FILES = (
    'cmip6/citations/cmip6_{}_citations.xlsx',
    'cmip6/citations/json/cmip6_{}_citations.json',
    'cmip6/models/initialization_from_CMIP5.json',
    'cmip6/models/model_publication.json',
    'cmip6/responsible_parties/cmip6_{}_responsible_parties.xlsx',
    'cmip6/responsible_parties/json/cmip6_{}_responsible_parties.json'
    )


def _verify_repo(i, errs):
    """Verifies that an institutional repo exists.

    """
    path = io_mgr.get_folder([i])
    if not os.path.exists(path):
        errs.append("ERROR: repo not found: {}".format(i.raw_name))


def _verify_sub_folders(i, errs):
    """Verifies that an institutional repo sub-folder exists.

    """
    for sub_folder in SUB_FOLDERS:
        path = [i] + sub_folder.split('/')
        folder = io_mgr.get_folder(path)
        if not os.path.exists(folder):
            errs.append("ERROR: sub-folder not found: {} --> {}".format(i.raw_name, sub_folder))


def _verify_static_files(i, errs):
    """Verifies that a set of institutional static files exists.

    """
    for static_file in STATIC_FILES:
        folder = io_mgr.get_folder([i])
        fname = static_file.format(i.canonical_name)
        path = os.path.join(folder, fname)
        if not os.path.exists(path):
            errs.append("ERROR: static file not found: {} --> {}".format(i.raw_name, fname))



def _verify_models(institute, errs):
    """Verifies that a set of institutional model documentation files exists.

    """
    # Root folder for models.
    folder = io_mgr.get_folder([institute, 'cmip6', 'models'])

    # Model configurations to be documented.
    configurations = vocabs.get_model_configurations(institute)

    # Set of model configuration names.
    models = set([i.canonical_name for i in configurations])

    # Model directories.
    folders = set([i for i in os.listdir(folder) if os.path.isdir(os.path.join(folder, i))])

    # Undocumented models.
    undocumented = models.difference(folders)
    for model in undocumented:
        errs.append("{} --> {} :: model undocumented".format(institute.raw_name, model))

    # Obsolete folders.
    obsolete = folders.difference(models)
    for model in obsolete:
        errs.append("{} --> {} :: model obsolete".format(institute.raw_name, model))

    # Documented models: validate sub-folders / files.
    documented = [i for i in configurations if i.canonical_name not in undocumented]
    for source_id in documented:
        # ... model CIM document;
        fpath = io_mgr.get_model_cim(institute, source_id)
        if not os.path.isfile(fpath):
            err = "{} --> {} :: CIM file not found".format(
                institute.raw_name, source_id.raw_name)
            errs.append(err)

        # ... model topic xls|json|pdf
        for topic in vocabs.get_model_topics(source_id):
            for fpath_factory, ftype in (
                    (io_mgr.get_model_topic_xls, 'XLS'),
                    (io_mgr.get_model_topic_json, 'JSON'),
                    (io_mgr.get_model_topic_pdf, 'PDF'),
                ):
                fpath = fpath_factory(institute, source_id, topic)
                if not os.path.isfile(fpath):
                    err = "{} --> {} --> {} :: {} file not found".format(
                        institute.raw_name, source_id.raw_name, topic.raw_name, ftype)
                    errs.append(err)


# Set of verifiers to be executed.
_VERIFIERS = (
    _verify_repo,
    # _verify_sub_folders,
    # _verify_static_files,
    _verify_models
    )


def _main(args):
    """Main entry point.

    """
    errs = []
    for i in vocabs.get_institutes(args.institution_id):
        for verifier in _VERIFIERS:
            verifier(i, errs)

    for err in errs:
        logger.log(err)


# Main entry point.
if __name__ == '__main__':
    _main(_ARGS.parse_args())
