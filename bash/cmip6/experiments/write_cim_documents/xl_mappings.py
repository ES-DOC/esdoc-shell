# -*- coding: utf-8 -*-

"""
.. module:: xl_mappins.py
   :license: GPL/CeCIL
   :platform: Unix, Windows
   :synopsis: Excel worksheet column mappings.

.. moduleauthor:: Mark Conway-Greenslade <momipsl@ipsl.jussieu.fr>

"""
import pyesdoc.ontologies.cim as cim

from constants import *
from convertors import *



# Maps of worksheet to cim type & columns.
WS_MAPS = {
    WS_PROJECT: (cim.v2.Project, [
            ("name", "A"),
            ("long_name", "B"),
            ("canonical_name", "C"),
            ("keywords", "D"),
            ("description", "E"),
            ("rationale", "F"),
            ("responsible_parties", "G", \
                lambda x, y: [i for i in [convert_to_cim_v2_responsibilty(x, y, "H-L")] if i]),
            ("citations", "M-R"),
            ("sub_projects", "V-AM"),
            ("required_experiments", "AN-BY"),
        ]),

    WS_EXPERIMENT: (cim.v2.NumericalExperiment, [
            ("internal_name", "A"),
            ("long_name", "B"),
            ("name", "C"),
            ("canonical_name", "C"),
            ("alternative_names", "D",
                lambda v, _: [] if not v else [i.strip() for i in v.split(",")]),
            ("keywords", "E"),
            ("governing_mips", "E-E", lambda v: v.split(",")[0]),
            ("tier", "E", lambda v: int(v.split(",")[1][-1])),
            ("description", "F"),
            ("rationale", "G"),
            ("responsible_parties", "H", \
                lambda x, y: [i for i in [convert_to_cim_v2_responsibilty(x, y, "I-M")] if i]),
            ("citations", "N-T"),
            ("is_perturbation_from", "V-V"),
            ("is_initialized_by", "W-W"),
            ("is_constrained_by", "X-Y"),
            ("is_sibling_of", "Z-AD"),
            ("temporal_constraints", "AE-AF"),
            ("ensembles", "AG-AJ"),
            ("multi_ensembles", "AK-AN"),
            ("model_configurations", "AO-AS"),
            ("forcing_constraints", "AT-BK"),
        ]),

    # TODO: additional requirements
    WS_REQUIREMENT: (cim.v2.NumericalRequirement, [
            ("name", "A"),
            ("long_name", "B"),
            ("canonical_name", "C"),
            ("keywords", "D"),
            ("description", "E"),
            ("rationale", "F"),
            ("responsible_parties", "G", \
                lambda x, y: [i for i in [convert_to_cim_v2_responsibilty(x, y, "H-J")] if i]),
            ("citations", "K-N"),
            ("is_conformance_requested", "P", convert_to_bool),
            ("additional_requirements", "Q-Z")
        ]),

    # TODO: data link @ col R
    # TODO: info required @ col D
    WS_FORCING_CONSTRAINT: (cim.v2.ForcingConstraint, [
            ("name", "A"),
            ("long_name", "B"),
            ("canonical_name", "C"),
            ("scope", "E", convert_to_cim_v2_numerical_requirement_scope),
            ("keywords", "F"),
            ("description", "G"),
            ("rationale", "H"),
            ("responsible_parties", "I", \
                lambda x, y: [i for i in [convert_to_cim_v2_responsibilty(x, y, "J-L")] if i]),
            ("citations", "M-Q"),
            ("data_link", "R"),
            ("is_conformance_requested", "T", convert_to_bool),
            ("forcing_type", "U")
        ]),

    WS_TEMPORAL_CONSTRAINT: (cim.v2.TemporalConstraint, [
            ("name", "A"),
            ("long_name", "B"),
            ("canonical_name", "C"),
            ("keywords", "D"),
            ("description", "E"),
            ("responsible_parties", "F", \
                lambda x, y: [i for i in [convert_to_cim_v2_responsibilty(x, y, "G-I")] if i]),
            ("citations", "J-J"),
            ("is_conformance_requested", "L", convert_to_bool),
            ("required_duration", "M", convert_to_cim_v2_time_period),
            ("required_calendar", "N", convert_to_cim_v2_calendar),
            ("start_date", "O",
                lambda c, r: convert_to_cim_v2_date_time(c, r(16))),
            ("start_flexibility", "Q", convert_to_cim_v2_time_period)
        ]),

    # TODO: ensemble-member @ O-AF
    WS_ENSEMBLE_REQUIREMENT: (cim.v2.EnsembleRequirement, [
            ("name", "A"),
            ("long_name", "B"),
            ("canonical_name", "C"),
            ("keywords", "D"),
            ("description", "E"),
            ("responsible_parties", "F", \
                lambda x, y: [i for i in [convert_to_cim_v2_responsibilty(x, y, "G-I")] if i]),
            ("citations", "J-J"),
            ("is_conformance_requested", "L", convert_to_bool),
            ("ensemble_type", "M"),
            ("minimum_size", "N", convert_to_int),
            ("members", "O-AF"),
        ]),

    WS_MULTI_ENSEMBLE: (cim.v2.MultiEnsemble, [
            ("name", "A"),
            ("long_name", "B"),
            ("canonical_name", "C"),
            ("keywords", "D"),
            ("description", "E"),
            ("responsible_parties", "F", \
                lambda x, y: [i for i in [convert_to_cim_v2_responsibilty(x, y, "G-I")] if i]),
            ("citations", "J-J"),
            ("is_conformance_requested", "L", convert_to_bool),
            ("ensemble_axis", "M-N")
        ]),

    WS_START_DATE_ENSEMBLE: (cim.v2.NumericalRequirement, [
            ("name", "A"),
            ("long_name", "B"),
            ("canonical_name", "C"),
            ("keywords", "D"),
            ("description", "E"),
            ("responsible_parties", "F", \
                lambda x, y: [i for i in [convert_to_cim_v2_responsibilty(x, y, "G-I")] if i]),
            ("citations", "J-J"),
            ("is_conformance_requested", "L", convert_to_bool),
            # TODO: verify target attributes
            ("regular_timeset_start_date", "M"),
            ("regular_timeset_start_length", "N"),
            ("regular_timeset_start_increment", "O"),
            ("irregular_dateset", "P")
        ]),

    WS_CITATIONS: (cim.v2.Citation, [
            ("doi", "A"),
            ("title", "B"),
            ("context", "C"),
            ("citation_detail", "D"),
            ("url", "E"),
            ("abstract", "F")
        ]),

    WS_PARTY: (cim.v2.Party, [
            ("name", "A"),
            ("organisation", "B", convert_to_bool),
            ("address", "C"),
            ("email", "D"),
            ("url", "E")
        ]),

    WS_URL: (cim.v2.OnlineResource, [
            ("name", "A"),
            ("linkage", "B"),
            ("protocol", "C"),
            ("description", "D"),
        ])
    }
