# -*- coding: utf-8 -*-

"""
.. module:: write_model_notebooks.py
   :license: GPL/CeCIL
   :platform: Unix, Windows
   :synopsis: Writes CMIP6 IPython model notebooks to file system.

.. moduleauthor:: Mark Conway-Greenslade <momipsl@ipsl.jussieu.fr>

"""
import pyesdoc
import pyessv

import defaults
import mappings
import mapper



def _yield_model():
    """Yields mappable CMIP5 model documents.

    """
    for m in pyesdoc.archive.yield_latest_documents("cmip5", "metafor-q", "cim-1-software-modelcomponent"):
        yield m


def _yield_model_components():
    """Yields mappable CMIP5 model components.

    """
    for m in _yield_model():
        for c in m.sub_components:
            if defaults.get_source_id(m, c):
                yield (m, c)


def _yield_notebook_outputs():
    """Yields CMIP6 notebook outputs.

    """
    for docs in _yield_model_components():
        yield mapper.map(docs)


# Initialise sub-modules.
pyesdoc.archive.init()
mappings.init()
defaults.init()

# Process mapped documents.
pyessv.log('Processing archived model documentation:', app='CMIP6')
for nb_output in _yield_notebook_outputs():
    nb_output.save()
    pyessv.log(nb_output.fpath, app='CMIP6')
