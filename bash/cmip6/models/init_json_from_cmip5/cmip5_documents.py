# -*- coding: utf-8 -*-

"""
.. module:: defaults.py
   :license: GPL/CeCIL
   :platform: Unix, Windows
   :synopsis: CMIP6 default model configuration information.

.. moduleauthor:: Mark Conway-Greenslade <momipsl@ipsl.jussieu.fr>

"""
import os

import pyesdoc

# Collection of CMIP5 documents to process.
DOCUMENTS = None


def init(institution_id):
    """Initialises seedings from institutional seeding config files.

    :param str institution_id: ID of institution being processed.

    """
    # Reset.
    global DOCUMENTS
    DOCUMENTS = list()

    # Set root folder path.
    fpath = os.getenv('ESDOC_HOME')
    fpath = os.path.join(fpath, 'repos')
    fpath = os.path.join(fpath, 'institutional')
    fpath = os.path.join(fpath, institution_id)
    fpath = os.path.join(fpath, 'cmip5')
    fpath = os.path.join(fpath, 'models')
    if not os.path.exists(fpath):
        return

    # Cache each model's cim document.
    for model_id in os.listdir(fpath):
        path = os.path.join(fpath, model_id)
        path = os.path.join(path, 'cim')
        if not os.path.exists(path):
            continue

        # Cache extended documents.
        for fname in os.listdir(path):
            doc_path = os.path.join(path, fname)
            DOCUMENTS.append(pyesdoc.extend(pyesdoc.read(doc_path)))

    return len(DOCUMENTS) > 0
