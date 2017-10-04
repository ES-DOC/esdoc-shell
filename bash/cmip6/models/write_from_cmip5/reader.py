# -*- coding: utf-8 -*-

"""
.. module:: reader.py
   :license: GPL/CeCIL
   :platform: Unix, Windows
   :synopsis: Reads CMIP5 files from file system.

.. moduleauthor:: Mark Conway-Greenslade <momipsl@ipsl.jussieu.fr>

"""
import argparse
import os

from pyesdoc import archive

import mappings
import seedings
import mapper_cim
import mapper_ipython
import writer_cim
import writer_ipython


# Map of encodings to mappers.
_MAPPERS = {
    'cim': mapper_cim,
    'ipython': mapper_ipython
}

# Map of encodings to writers.
_WRITERS = {
    'cim': writer_cim,
    'ipython': writer_ipython
}


def yield_model_components():
    """Yields mappable CMIP5 model components.

    """
    for m in archive.yield_latest_documents("cmip5", "metafor-q", "cim-1-software-modelcomponent"):
        for c in m.sub_components:
            if seedings.get_source_id(m, c):
                yield m, c
