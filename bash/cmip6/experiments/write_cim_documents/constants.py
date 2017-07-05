# -*- coding: utf-8 -*-

"""
.. module:: constants.py
   :license: GPL/CeCIL
   :platform: Unix, Windows
   :synopsis: Constants used across package.

.. moduleauthor:: Mark Conway-Greenslade <momipsl@ipsl.jussieu.fr>

"""
import datetime as dt

import pyesdoc
import pyesdoc.ontologies.cim as cim



# Spreadsheet worksheet names.
WS_PROJECT = "project"
WS_EXPERIMENT = "experiment"
WS_REQUIREMENT = "requirement"
WS_FORCING_CONSTRAINT = "ForcingConstraint"
WS_TEMPORAL_CONSTRAINT = "TemporalConstraint"
WS_ENSEMBLE_REQUIREMENT = "EnsembleRequirement"
WS_MULTI_ENSEMBLE = "MultiEnsemble"
WS_START_DATE_ENSEMBLE = "StartDateEnsemble"
WS_CITATIONS = "references"
WS_PARTY = "party"
WS_URL = "url"

# Spreadsheet row offsets.
WS_ROW_OFFSETS = {
    WS_PROJECT: 2,
    WS_EXPERIMENT: 2,
    WS_REQUIREMENT: 2,
    WS_FORCING_CONSTRAINT: 2,
    WS_TEMPORAL_CONSTRAINT: 2,
    WS_ENSEMBLE_REQUIREMENT: 2,
    WS_MULTI_ENSEMBLE: 2,
    WS_START_DATE_ENSEMBLE: 2,
    WS_CITATIONS: 1,
    WS_PARTY: 1,
    WS_URL: 1
}

# Set of worksheet name keys.
WS_SHEETS = [
    WS_PROJECT,
    WS_EXPERIMENT,
    WS_REQUIREMENT,
    WS_FORCING_CONSTRAINT,
    WS_TEMPORAL_CONSTRAINT,
    WS_ENSEMBLE_REQUIREMENT,
    WS_MULTI_ENSEMBLE,
    WS_START_DATE_ENSEMBLE,
    WS_CITATIONS,
    WS_PARTY,
    WS_URL
]

# Default document project code.
DOC_PROJECT = 'CMIP6'

# Default document source.
DOC_SOURCE = 'spreadsheet'

# Default document author.
DOC_AUTHOR = pyesdoc.create(cim.v2.Party,
                             source=DOC_SOURCE,
                             uid=u'253825f3-fbc8-43fb-b1f6-cc575dc693eb',
                             version=1)
DOC_AUTHOR.email = u"charlotte.pascoe@stfc.ac.uk"
DOC_AUTHOR.name = u"Charlotte Pascoe"

# Default document author reference.
DOC_AUTHOR_REFERENCE = cim.v2.DocReference()
DOC_AUTHOR_REFERENCE.uid = DOC_AUTHOR.meta.id
DOC_AUTHOR_REFERENCE.version = DOC_AUTHOR.meta.version

# Default document create / update dates.
DOC_CREATE_DATE = dt.datetime.strptime("2017-03-21 00:00:00", "%Y-%m-%d %H:%M:%S")
DOC_UPDATE_DATE = DOC_CREATE_DATE

# Set of experimental relationships.
EXPERIMENTAL_RELATIONSHIP_TYPES = {
    "is_constrained_by",
    "is_constrainer_of",
    "is_perturbation_from",
    "is_control_for",
    "is_initialized_by",
    "is_initializer_of",
    "is_sibling_of"
    }
