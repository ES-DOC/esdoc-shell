    # -*- coding: utf-8 -*-

"""
.. module:: run_publish_cmip6_documents.py
   :license: GPL/CeCIL
   :platform: Unix, Windows
   :synopsis: Publishes CMIP6 documents from the CMIP6 experiment spreadsheet.

.. moduleauthor:: Mark Conway-Greenslade <momipsl@ipsl.jussieu.fr>

"""
import argparse
import json
import os
import string
import uuid
from collections import defaultdict
from operator import add
from datetime import datetime as dt

import dreq
import xlrd

import pyesdoc
import pyesdoc.ontologies.cim as cim



# Define command line options.
_ARGS = argparse.ArgumentParser("Publishes CIM documents extracted from CMIP6 experiment spreadsheet.")
_ARGS.add_argument(
    "--io-dir",
    help="Path to a directory into which documents will be written.",
    dest="io_dir",
    type=str
    )
_ARGS.add_argument(
    "--spreadsheet",
    help="Path to the CMIP6 experiments worksheet.",
    dest="spreadsheet_filepath",
    type=str
    )
_ARGS.add_argument(
    "--identifiers",
    help="Path to set of CMIP6 experiments document identifiers.",
    dest="identifiers",
    type=str
    )



# Spreadsheet worksheet names.
_WS_PROJECT = "project"
_WS_EXPERIMENT = "experiment"
_WS_REQUIREMENT = "requirement"
_WS_FORCING_CONSTRAINT = "ForcingConstraint"
_WS_TEMPORAL_CONSTRAINT = "TemporalConstraint"
_WS_ENSEMBLE_REQUIREMENT = "EnsembleRequirement"
_WS_MULTI_ENSEMBLE = "MultiEnsemble"
_WS_START_DATE_ENSEMBLE = "StartDateEnsemble"
_WS_CITATIONS = "references"
_WS_PARTY = "party"
_WS_URL = "url"

# Spreadsheet row offsets.
_WS_ROW_OFFSETS = {
    _WS_PROJECT: 2,
    _WS_EXPERIMENT: 2,
    _WS_REQUIREMENT: 2,
    _WS_FORCING_CONSTRAINT: 2,
    _WS_TEMPORAL_CONSTRAINT: 2,
    _WS_ENSEMBLE_REQUIREMENT: 2,
    _WS_MULTI_ENSEMBLE: 2,
    _WS_START_DATE_ENSEMBLE: 2,
    _WS_CITATIONS: 1,
    _WS_PARTY: 1,
    _WS_URL: 1
}

# Set of worksheet name keys.
_WS_SHEETS = [
    _WS_PROJECT,
    _WS_EXPERIMENT,
    _WS_REQUIREMENT,
    _WS_FORCING_CONSTRAINT,
    _WS_TEMPORAL_CONSTRAINT,
    _WS_ENSEMBLE_REQUIREMENT,
    _WS_MULTI_ENSEMBLE,
    _WS_START_DATE_ENSEMBLE,
    _WS_CITATIONS,
    _WS_PARTY,
    _WS_URL
]

# Default document project code.
_DOC_PROJECT = 'CMIP6-DRAFT'

# Default document source.
_DOC_SOURCE = 'spreadsheet'

# Default document author.
_DOC_AUTHOR = pyesdoc.create(cim.v2.Party,
                             source=_DOC_SOURCE,
                             uid=u'253825f3-fbc8-43fb-b1f6-cc575dc693eb',
                             version=1)
_DOC_AUTHOR.email = u"charlotte.pascoe@stfc.ac.uk"
_DOC_AUTHOR.name = u"Charlotte Pascoe"

# Default document author reference.
_DOC_AUTHOR_REFERENCE = cim.v2.DocReference()
_DOC_AUTHOR_REFERENCE.uid = _DOC_AUTHOR.meta.id
_DOC_AUTHOR_REFERENCE.version = _DOC_AUTHOR.meta.version

# Default document create / update dates.
_DOC_CREATE_DATE = dt.strptime("2016-07-04 13:00:00", "%Y-%m-%d %H:%M:%S")
_DOC_UPDATE_DATE = _DOC_CREATE_DATE

# Set of experimental relationships.
_EXPERIMENTAL_RELATIONSHIP_TYPES = {
    "is_constrained_by",
    "is_constrainer_of",
    "is_perturbation_from",
    "is_control_for",
    "is_initialized_by",
    "is_initializer_of",
    "is_sibling_of"
    }

# Set "controlled vocabulary".
_CV = {
    _WS_EXPERIMENT: [],
    _WS_PROJECT: []
}

fpath = os.path.join(os.path.dirname(os.path.abspath(__file__)), "cv_experiment_id.json")
with open(fpath) as fstream:
    _CV[_WS_EXPERIMENT] = json.loads(fstream.read())['experiment_id']


def _convert_to_bool(value):
    """Converts a cell value to a boolean.

    """
    return unicode(value).lower() in [u'true', u't', u'yes', u'y', u"1"]


def _convert_to_unicode(value):
    """Converts a cell value to a boolean.

    """
    if value is None:
        return

    value = unicode(value)

    # Null substitutions.
    if value.lower() in [u"n/a"]:
        return

    # Strip superfluos suffixes.
    value = value.strip()
    if len(value) > 0 and value[-1] in [u":"]:
        return value[0:-1]

    return value


def _convert_to_int(value):
    """Converts a cell value to an integer.

    """
    return None if value is None else int(value)


def _convert_to_string_array(value):
    """Converts a cell value to an array of strings.

    """
    return [] if value is None else value.split(", ")


def _convert_to_cim_v2_calendar(value):
    """Converts a cell value to a cim.v2.DateTime instance.

    """
    if value is None:
        return

    # TODO
    return
    raise NotImplementedError("CIM v2 Calendar value needs to be converted from cell content")


def _convert_to_cim_v2_time_period(value):
    """Converts a cell value to a cim.v2.TimePeriod instance.

    """
    if value is None:
        return

    instance = cim.v2.TimePeriod()
    instance.length = value.split(" ")[0]
    instance.units = value.split(" ")[1]
    instance.date_type = u'unused'

    return instance


def _convert_to_cim_v2_numerical_requirement_delivery_order(value):
    """Converts a cell value to a cim.v2.NumericalRequirementScope enum value.

    """
    return {
        1: "pre-simulation",
        2: "post-simulation",
    }[value]


def _convert_to_cim_v2_numerical_requirement_scope(value):
    """Converts a cell value to a cim.v2.NumericalRequirementScope enum value.

    """
    return {
        1: "mip-era",
        2: "mip-group",
        3: "mip",
        4: "experiment",
    }[value]


def _convert_to_cim_v2_date_time(value, offset):
    """Converts a cell value to a cim.v2.DateTime instance.

    """
    if value is None:
        return

    instance = cim.v2.DateTime()
    instance.value = value
    instance.offset = _convert_to_bool(offset)

    return instance


def _convert_to_cim_2_responsibilty(role, row, col_idx):
    """Returns experiment responsibility info.

    """
    if role is None:
        return

    col_idx = _convert_col_idx(col_idx)

    responsibility = cim.v2.Responsibility()
    responsibility.role = _convert_to_unicode(role)
    responsibility.parties = [r for r in [row(col_idx), row(col_idx + 1), row(col_idx + 2)] if r]

    return responsibility


def _convert_name(name, collection, slots=["citation_detail", "canonical_name", "name"]):
    """Retrieves a document from a collection.

    """
    if not collection or name is None:
        return

    try:
        float(name)
    except:
        pass
    else:
        name = str(name).split('.')[0]
    finally:
        if len(name.strip()) == 0:
            return

    name = name.lower()
    for item in collection:
        for attr in slots:
            try:
                item_name = getattr(item, attr)
            except AttributeError:
                continue
            else:
                if name == unicode(item_name).lower():
                    return item


def _convert_names(names, collection, slots=["citation_detail", "canonical_name", "name"]):
    """Converts a set of names to a set of document.

    """
    result = [_convert_name(n, collection, slots) for n in names]

    return [d for d in result if d]


def _convert_col_idx(col_idx):
    """Converts a column index to an integer.

    """
    num = 0
    for c in col_idx:
        if c in string.ascii_letters:
            num = num * 26 + (ord(c.upper()) - ord('A')) + 1
    return num


# Maps of worksheet to cim type & columns.
_WS_MAPS = {
    _WS_PROJECT: (cim.v2.Project, [
            ("name", "A"),
            ("long_name", "B"),
            ("canonical_name", "C"),
            ("keywords", "D"),
            ("description", "E"),
            ("rationale", "F"),
            ("responsible_parties", "G", \
                lambda x, y: [i for i in [_convert_to_cim_2_responsibilty(x, y, "H")] if i]),
            ("citations", "K-P"),
            ("sub_projects", "T-AK"),
            ("required_experiments", "AL-BU"),
        ]),

    _WS_EXPERIMENT: (cim.v2.NumericalExperiment, [
            ("internal_name", "A"),
            ("long_name", "B"),
            ("name", "C"),
            ("canonical_name", "C"),
            ("alternative_names", "D",
                lambda v, _: [] if not v else [i.strip() for i in v.split(",")]),
            ("keywords", "E"),
            ("governing_mips", "E-E", lambda v: v.split(",")[0]),
            ("description", "F"),
            ("rationale", "G"),
            ("responsible_parties", "H", \
                lambda x, y: [i for i in [_convert_to_cim_2_responsibilty(x, y, "I")] if i]),
            ("citations", "L-R"),
            ("is_perturbation_from", "T-T"),
            ("is_initialized_by", "U-U"),
            ("is_constrained_by", "V-W"),
            ("is_sibling_of", "X-AB"),
            ("temporal_constraints", "AC-AD"),
            ("ensembles", "AE-AH"),
            ("multi_ensembles", "AI-AL"),
            ("model_configurations", "AM-AQ"),
            ("forcing_constraints", "AR-BI"),
        ]),

    # TODO: additional requirements
    _WS_REQUIREMENT: (cim.v2.NumericalRequirement, [
            ("name", "A"),
            ("long_name", "B"),
            ("canonical_name", "C"),
            ("keywords", "D"),
            ("description", "E"),
            ("rationale", "F"),
            ("responsible_parties", "G", \
                lambda x, y: [i for i in [_convert_to_cim_2_responsibilty(x, y, "H")] if i]),
            ("citations", "K-N"),
            ("is_conformance_requested", "P", _convert_to_bool),
            ("additional_requirements", "Q-Z")
        ]),

    _WS_FORCING_CONSTRAINT: (cim.v2.ForcingConstraint, [
            ("name", "A"),
            ("long_name", "B"),
            ("canonical_name", "C"),
            ("delivery_order", "D", _convert_to_cim_v2_numerical_requirement_delivery_order),
            ("scope", "E", _convert_to_cim_v2_numerical_requirement_scope),
            ("keywords", "F"),
            ("description", "G"),
            ("rationale", "H"),
            ("responsible_parties", "I", \
                lambda x, y: [i for i in [_convert_to_cim_2_responsibilty(x, y, "J")] if i]),
            ("citations", "M-Q"),
            ("is_conformance_requested", "S", _convert_to_bool),
            ("forcing_type", "T")
        ]),

    _WS_TEMPORAL_CONSTRAINT: (cim.v2.TemporalConstraint, [
            ("name", "A"),
            ("long_name", "B"),
            ("canonical_name", "C"),
            ("keywords", "D"),
            ("description", "E"),
            ("responsible_parties", "F", \
                lambda x, y: [i for i in [_convert_to_cim_2_responsibilty(x, y, "G")] if i]),
            ("citations", "J-J"),
            ("is_conformance_requested", "L", _convert_to_bool),
            ("required_duration", "M", _convert_to_cim_v2_time_period),
            ("required_calendar", "N", _convert_to_cim_v2_calendar),
            ("start_date", "O",
                lambda c, r: _convert_to_cim_v2_date_time(c, r(16))),
            ("start_flexibility", "Q", _convert_to_cim_v2_time_period)
        ]),

    # TODO: ensemble-member, cols 15, 16, 17
    _WS_ENSEMBLE_REQUIREMENT: (cim.v2.EnsembleRequirement, [
            ("name", "A"),
            ("long_name", "B"),
            ("canonical_name", "C"),
            ("keywords", "D"),
            ("description", "E"),
            ("responsible_parties", "F", \
                lambda x, y: [i for i in [_convert_to_cim_2_responsibilty(x, y, "G")] if i]),
            ("citations", "J-J"),
            ("is_conformance_requested", "L", _convert_to_bool),
            ("ensemble_type", "M"),
            ("minimum_size", "N", _convert_to_int),
            # TODO: map to cim type
            ("members", "O-T"),
        ]),

    # TODO: map to cim type
    _WS_MULTI_ENSEMBLE: (cim.v2.MultiEnsemble, [
            ("name", "A"),
            ("long_name", "B"),
            ("canonical_name", "C"),
            ("keywords", "D"),
            ("description", "E"),
            ("responsible_parties", "F", \
                lambda x, y: [i for i in [_convert_to_cim_2_responsibilty(x, y, "G")] if i]),
            ("citations", "J-J"),
            ("is_conformance_requested", "L", _convert_to_bool),
            ("ensemble_axis", "M-N")
        ]),

    # TODO: map to cim type
    _WS_START_DATE_ENSEMBLE: (cim.v2.NumericalRequirement, [
            ("name", "A"),
            ("long_name", "B"),
            ("canonical_name", "C"),
            ("keywords", "D"),
            ("description", "E"),
            ("responsible_parties", "F", \
                lambda x, y: [i for i in [_convert_to_cim_2_responsibilty(x, y, "G")] if i]),
            ("citations", "J-J"),
            ("is_conformance_requested", "L", _convert_to_bool),
            # TODO: verify target attributes
            ("regular_timeset_start_date", "M"),
            ("regular_timeset_start_length", "N"),
            ("regular_timeset_start_increment", "O"),
            ("irregular_dateset", "P"),
        ]),

    _WS_CITATIONS: (cim.v2.Citation, [
            ("doi", "A"),
            ("title", "B"),
            ("context", "C"),
            ("citation_detail", "D"),
            ("url", "E"),
            ("abstract", "F")
        ]),

    _WS_PARTY: (cim.v2.Party, [
            ("name", "A"),
            ("organisation", "B", _convert_to_bool),
            ("address", "C"),
            ("email", "D"),
            ("url", "E")
        ]),

    _WS_URL: (cim.v2.OnlineResource, [
            ("name", "A"),
            ("linkage", "B"),
            ("protocol", "C"),
            ("description", "D"),
        ])
    }


class ControlledVocabularies(object):
    """Wrapper around the controlled vocabularies in use.

    """
    def __init__(self):
        """Instance constructor.

        """
        dpath = os.path.dirname(os.path.abspath(__file__))
        for cv_type in {"experiment", "activity"}:
            fpath = os.path.join(dpath, "cv_{}_id.json".format(cv_type))
            with open(fpath) as fstream:
                setattr(self, cv_type, json.loads(fstream.read())["{}_id".format(cv_type)])


    def validate(self, projects, experiments):
        """Validate various CV termsets within collections.

        """
        def _validate(typeof, terms, docs):
            """Inner function to perform the validation.

            """
            terms = [i.lower() for i in terms]
            invalid_docs = []
            for doc in docs:
                if doc.name.lower() not in terms:
                    invalid_docs.append(doc)

            invalid_terms = []
            for term in terms:
                found = False
                for doc in docs:
                    if doc.name.lower() == term:
                        found = True
                        break
                if not found:
                    invalid_terms.append(term)

            if invalid_docs:
                print "------------------------------------------------------"
                print "NON-VALIDATED {} NAMES".format(typeof.upper())
                print "------------------------------------------------------"
                for doc in sorted(invalid_docs, key=lambda i: i.name.lower()):
                    print doc.name

            if invalid_terms:
                print "------------------------------------------------------"
                print "NON-VALIDATED {} TERMS".format(typeof.upper())
                print "------------------------------------------------------"
                for term in sorted(invalid_terms):
                    print term

        _validate("project", self.activity, projects)
        _validate("experiment", self.experiment.keys(), experiments)


class Spreadsheet(object):
    """The spreadhsset from which CIM documents are to be extracted.

    """
    def __init__(self, worksheet_fpath, identifiers):
        """Instance constructor.

        """
        self.ids = identifiers
        self._spreadsheet = xlrd.open_workbook(worksheet_fpath)


    def _get_sheet(self, ws_name):
        """Returns pointer to a named worksheet.

        """
        return self._spreadsheet.sheet_by_name(ws_name)


    def _get_rows(self, ws_name):
        """Returns collection of rows within a named worksheet.

        """
        return enumerate(self._get_sheet(ws_name).get_rows())


    def _yield_rows(self, ws_name):
        """Yields rows within a named worksheet.

        """
        for idx, row in self._get_rows(ws_name):
            if idx >= _WS_ROW_OFFSETS[ws_name] and \
               len(row[0].value):
                yield idx, row


    def _get_cell_value(self, row, col_idx, convertor):
        """Returns the (converted) value of a worksheet cell.

        """
        # Extract raw cell value.
        value = row[col_idx - 1].value

        # Nullify dead text.
        if isinstance(value, (unicode, str)):
            value = value.strip()
            if len(value) == 0:
                value = None
            elif value.upper() in {u"NONE", u"N/A"}:
                value = None

        # Convert if necessary.
        if convertor:
            try:
                return convertor(value)
            except TypeError:
                return convertor(value, lambda i: row[i - 1].value)

        return value


    def __getitem__(self, ws_name):
        """Returns a child table attribute.

        """
        doc_type, mappings = _WS_MAPS[ws_name]

        return [self._get_document(self.ids[ws_name][str(idx)], doc_type, row, mappings)
                for idx, row in self._yield_rows(ws_name)]


    def _set_document_attribute(self, doc, row, mapping):
        """Asssigns a document attribute form a mapping.

        """
        # Unpack mapping info.
        try:
            attr, col_idx, convertor = mapping
        except ValueError:
            try:
                attr, col_idx = mapping
            except ValueError:
                print mapping
                raise ValueError()
            convertor = None

        # Convert cell value.
        if col_idx.find("-") == -1:
            attr_value = self._get_cell_value(row, _convert_col_idx(col_idx), convertor)
        else:
            col_idx_from, col_idx_to = [_convert_col_idx(i) for i in col_idx.split("-")]
            attr_value = [i for i in (self._get_cell_value(row, i, convertor)
                          for i in range(col_idx_from, col_idx_to + 1)) if i]

        # Set aattribute value.
        setattr(doc, attr, attr_value)


    def _get_document(self, doc_uid, doc_type, row, mappings):
        """Returns a CIM document from a spreadsheet row.

        """
        # Create document.
        doc = pyesdoc.create(doc_type,
                             project=_DOC_PROJECT,
                             source=_DOC_SOURCE,
                             version=1,
                             uid=doc_uid)

        # Assign document dates.
        try:
            doc.meta
        except AttributeError:
            pass
        else:
            doc.meta.create_date = _DOC_CREATE_DATE
            doc.meta.update_date = _DOC_UPDATE_DATE

        # Assign document author.
        try:
            doc.meta.author = _DOC_AUTHOR_REFERENCE
        except AttributeError:
            pass

        # Set document attributes from mapped worksheet cells.
        for mapping in mappings:
            self._set_document_attribute(doc, row, mapping)

        return doc


class DocumentIdentifiers(object):
    """Wraps the set of predefined document identifiers.

    """
    def __init__(self, fpath):
        """Instance constructor.

        """
        self._uids = defaultdict(lambda: defaultdict(int))
        with open(fpath, 'r') as fstream:
            for line in fstream.readlines():
                ws_name, ws_row, doc_uid = line.split("::")
                self._uids[ws_name][ws_row] = uuid.UUID(doc_uid.replace("\n", ""))


    def __getitem__(self, ws_name):
        """Returns document collection.

        """
        return self._uids[ws_name]


class DocumentSet(object):
    """The set of documents extracted from the workwheet.

    """
    def __init__(self, spreadsheet):
        """Instance constructor.

        """
        self.docs = defaultdict(list)
        for sheet in _WS_SHEETS:
            self[sheet] = spreadsheet[sheet]
        self._set_dreq_info()


    def __getitem__(self, ws_name):
        """Returns document collection.

        """
        return self.docs[ws_name]


    def __setitem__(self, ws_name, collection):
        """Set document collection.

        """
        self.docs[ws_name] = collection


    @property
    def documents(self):
        """Gets full set of managed documents.

        """
        return self[_WS_PROJECT] + \
               self[_WS_EXPERIMENT] + \
               self.numerical_requirements + \
               self[_WS_CITATIONS] + \
               self[_WS_PARTY]


    @property
    def numerical_requirements(self):
        """Gets full set of managed numerical requirements.

        """
        return self[_WS_REQUIREMENT] + \
               self[_WS_FORCING_CONSTRAINT] + \
               self[_WS_TEMPORAL_CONSTRAINT] + \
               self[_WS_ENSEMBLE_REQUIREMENT] + \
               self[_WS_MULTI_ENSEMBLE] + \
               self[_WS_START_DATE_ENSEMBLE]


    @property
    def citation_containers(self):
        """Gets full set of managed objects that have citation collections.

        """
        return self[_WS_EXPERIMENT] + \
               self.numerical_requirements + \
               self[_WS_PROJECT]


    @property
    def url_containers(self):
        """Gets full set of managed objects that have citation collections.

        """
        return self[_WS_PARTY] + self[_WS_CITATIONS]


    @property
    def responsible_party_containers(self):
        """Gets full set of managed objects that have responsible partie collections.

        """
        return self[_WS_EXPERIMENT] + \
               self.numerical_requirements + \
               self[_WS_PROJECT]


    @property
    def responsible_parties(self):
        """Gets full set of managed responsible parties.

        """
        return reduce(add, [i.responsible_parties for i in self.responsible_party_containers])


    @property
    def urls(self):
        """Gets full set of managed url's.

        """
        return reduce(add, [i.url for i in self.url_containers])


    def _get_doc_link(self, doc, type_note=None):
        """Returns a document link.

        """
        if not doc:
            return

        reference = cim.v2.DocReference()
        reference.id = doc.meta.id
        reference.version = doc.meta.version
        if type_note:
            reference.type = "{}:{}".format(doc.type_key, type_note)
        else:
            reference.type = doc.type_key
        if isinstance(doc, cim.v2.designing.Project):
            reference.name = doc.name
        else:
            for attr in ["canonical_name", "name"]:
                try:
                    reference.name = getattr(doc, attr)
                except AttributeError:
                    pass
                else:
                    break
        try:
            reference.canonical_name = doc.canonical_name
        except AttributeError:
            pass

        return reference


    def _set_dreq_info(self):
        """Sets information dervied from the data request.

        """
        dreq.initialize()
        for p in self[_WS_PROJECT]:
            mip = dreq.query('mip', p.canonical_name)
            if mip:
                if mip.url != 'None':
                    p.homepage = mip.url
                p.objectives = ["{}: {}".format(o.label, o.description) for o in mip.objectives]
                p.objectives = sorted(p.objectives)


    def ignore_documents(self):
        """Filters out documents deemed unwirthy of persisting.

        """
        self[_WS_EXPERIMENT] = [e for e in self[_WS_EXPERIMENT] if e.canonical_name and e.canonical_name.lower() != "n/a"]


    def set_document_connections(self):
        """Sets inter document connections.

        """
        # Set urls.
        for x in self.url_containers:
            x.url = _convert_name(x.url, self[_WS_URL])

        # Set citations.
        for x in self.citation_containers:
            x.citations = _convert_names(x.citations, self[_WS_CITATIONS])

        # Set responsibility parties.
        for rp in self.responsible_parties:
            rp.parties = _convert_names(rp.parties, self[_WS_PARTY])

        # Set intra-experiment relationships.
        for e in self[_WS_EXPERIMENT]:
            for r in {"is_constrained_by", "is_perturbation_from", "is_initialized_by", "is_sibling_of"}:
                setattr(e, r, _convert_names(getattr(e, r), self[_WS_EXPERIMENT]))
        for e in self[_WS_EXPERIMENT]:
            for r in {"is_constrainer_of", "is_control_for", "is_initializer_of"}:
                setattr(e, r, [])
        for e in self[_WS_EXPERIMENT]:
            for r_exp in e.is_constrained_by:
                r_exp.is_constrainer_of.append(e)
            for r_exp in e.is_perturbation_from:
                r_exp.is_control_for.append(e)
            for r_exp in e.is_initialized_by:
                r_exp.is_initializer_of.append(e)
        for e in self[_WS_EXPERIMENT]:
            for r in {"is_constrainer_of", "is_control_for", "is_initializer_of"}:
                setattr(e, r, list(set(getattr(e, r))))

        # Set experiment requirements.
        for e in self[_WS_EXPERIMENT]:
            e.temporal_constraints = \
                _convert_names(e.temporal_constraints, self[_WS_TEMPORAL_CONSTRAINT])
            e.forcing_constraints = [_convert_name(i, self[_WS_FORCING_CONSTRAINT]) or
                                     _convert_name(i, self[_WS_REQUIREMENT])
                                     for i in e.forcing_constraints]
            e.ensembles = \
                _convert_names(e.ensembles, self[_WS_ENSEMBLE_REQUIREMENT])
            e.model_configurations = \
                _convert_names(e.model_configurations, self[_WS_REQUIREMENT])
            e.multi_ensembles = \
                _convert_names(e.multi_ensembles, self[_WS_MULTI_ENSEMBLE])

        # Set project sub-projects.
        for p in self[_WS_PROJECT]:
            pass

        # Set experiment governing mip.
        for e in self[_WS_EXPERIMENT]:
            e.governing_mips = _convert_names(e.governing_mips, self[_WS_PROJECT], slots=["name"])
            for p in e.governing_mips:
                p.governed_experiments.append(e)

        # Set experiment sub-projects.
        for e in self[_WS_EXPERIMENT]:
            for project in self[_WS_PROJECT]:
                if e.canonical_name in project.required_experiments:
                    e.meta.sub_projects.append(project.name)
                    e.related_mips.append(project)
            e.meta.sub_projects = sorted(e.meta.sub_projects)

        # Set additional experimental requirements.
        for rq in self[_WS_REQUIREMENT]:
            rq.additional_requirements = _convert_names(rq.additional_requirements, self.numerical_requirements)

        # Set multi-ensemble axis.
        for me in self[_WS_MULTI_ENSEMBLE]:
            me.ensemble_axis = _convert_names(me.ensemble_axis, self.numerical_requirements)

        # Set sub-projects.
        for p in self[_WS_PROJECT]:
            p.meta.sub_projects = sorted(p.sub_projects)
            p.sub_projects = _convert_names(p.sub_projects, self[_WS_PROJECT])

        # Set project required experiments.
        for p in self[_WS_PROJECT]:
            p.required_experiments = _convert_names(p.required_experiments, self[_WS_EXPERIMENT])

        # Set governed experiments - order as per required experiments.
        for p in self[_WS_PROJECT]:
            governed_experiments = [i for i in p.required_experiments if i in p.governed_experiments]
            governed_experiments += sorted(list(set(p.governed_experiments) - set(governed_experiments)), key=lambda i: i.name)
            p.governed_experiments = governed_experiments

        for e in self[_WS_EXPERIMENT]:
            if e.name is None and e.canonical_name is None:
                print "XXX", e.__dict__


    def set_document_links(self):
        """Sets inter document links.

        """
        def set_links(doc, doc_attr):
            """Helper function to assign a collection of links.

            """
            setattr(doc, doc_attr, [self._get_doc_link(i) for i in getattr(doc, doc_attr)])

        # Responsible parties.
        for rp in self.responsible_parties:
            set_links(rp, "parties")

        # Citations.
        for c in self.citation_containers:
            set_links(c, "citations")

        # Experiments.
        for e in self[_WS_EXPERIMENT]:
            for r in _EXPERIMENTAL_RELATIONSHIP_TYPES:
                for re in [self._get_doc_link(d) for d in getattr(e, r)]:
                    re.relationship = r
                    e.related_experiments.append(re)
                delattr(e, r)

        # Experimental requirements.
        for e in self[_WS_EXPERIMENT]:
            e.requirements += [self._get_doc_link(d) for d in e.temporal_constraints]
            for fc in e.forcing_constraints:
                if isinstance(fc, cim.v2.ForcingConstraint):
                    e.requirements.append(self._get_doc_link(fc))
                else:
                    e.requirements.append(self._get_doc_link(fc, "forcing_constraint"))
            e.requirements += [self._get_doc_link(d) for d in e.ensembles]
            e.requirements += [self._get_doc_link(d, "model_configuration") for d in e.model_configurations]
            e.requirements += [self._get_doc_link(d) for d in e.multi_ensembles]

        # Requirement --> Requirement.
        for r in self[_WS_REQUIREMENT]:
            set_links(r, "additional_requirements")

        # Experiment --> MIP.
        for e in self[_WS_EXPERIMENT]:
            set_links(e, "governing_mips")
            set_links(e, "related_mips")

        # Project --> Project.
        for p in self[_WS_PROJECT]:
            set_links(p, "sub_projects")

        # Project --> Experiment.
        for p in self[_WS_PROJECT]:
            set_links(p, "required_experiments")
            set_links(p, "governed_experiments")


    def write(self, io_dir):
        """Writes documents to file system.

        """
        def _write(doc, encoding):
            """Writes document to file system.

            """
            pyesdoc.write(doc, io_dir, encoding=encoding)

        # Remove helper attributes that do not need to be serialzed.
        for experiment in self[_WS_EXPERIMENT]:
            del experiment.temporal_constraints
            del experiment.forcing_constraints
            del experiment.ensembles
            del experiment.model_configurations
            del experiment.multi_ensembles

        for doc in self.documents:
            _write(doc, pyesdoc.ENCODING_JSON)


def _main(args):
    """Main entry point.

    """
    if not os.path.isfile(args.spreadsheet_filepath):
        raise ValueError("Spreadsheet file does not exist")
    if not os.path.isdir(args.io_dir):
        raise ValueError("Archive directory does not exist")

    docs = DocumentSet(
        Spreadsheet(args.spreadsheet_filepath, DocumentIdentifiers(args.identifiers))
            )
    docs.ignore_documents()

    cv = ControlledVocabularies()
    cv.validate(docs[_WS_PROJECT], docs[_WS_EXPERIMENT])
    return

    docs.set_document_connections()
    docs.set_document_links()
    docs.write(args.io_dir)


# Entry point.
if __name__ == '__main__':
    _main(_ARGS.parse_args())
