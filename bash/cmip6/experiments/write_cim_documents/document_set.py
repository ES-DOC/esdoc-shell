# -*- coding: utf-8 -*-

"""
.. module:: document_set.py
   :license: GPL/CeCIL
   :platform: Unix, Windows
   :synopsis: Wraps set of CIM documents to be written to file system.

.. moduleauthor:: Mark Conway-Greenslade <momipsl@ipsl.jussieu.fr>

"""
from operator import add
import collections

import pyesdoc.ontologies.cim as cim

from constants import *
from convertors import *



class DocumentSet(object):
    """The set of documents extracted from the workwheet.

    """
    def __init__(self, spreadsheet):
        """Instance constructor.

        """
        self.docs = collections.defaultdict(list)
        for sheet in WS_SHEETS:
            self[sheet] = spreadsheet[sheet]
        self._set_derived_info()
        self._set_data_request_info()


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
        return self[WS_PROJECT] + \
               self[WS_EXPERIMENT] + \
               self.numerical_requirements + \
               self[WS_CITATIONS] + \
               self[WS_PARTY]


    @property
    def numerical_requirements(self):
        """Gets full set of managed numerical requirements.

        """
        return self[WS_REQUIREMENT] + \
               self[WS_FORCING_CONSTRAINT] + \
               self[WS_TEMPORAL_CONSTRAINT] + \
               self[WS_ENSEMBLE_REQUIREMENT] + \
               self[WS_MULTI_ENSEMBLE] + \
               self[WS_START_DATE_ENSEMBLE]


    @property
    def citation_containers(self):
        """Gets full set of managed objects that have citation collections.

        """
        return self[WS_EXPERIMENT] + \
               self.numerical_requirements + \
               self[WS_PROJECT]


    @property
    def url_containers(self):
        """Gets full set of managed objects that have url collections.

        """
        return self[WS_PARTY] + self[WS_CITATIONS]


    @property
    def responsible_party_containers(self):
        """Gets full set of managed objects that have responsible partie collections.

        """
        return self[WS_EXPERIMENT] + \
               self.numerical_requirements + \
               self[WS_PROJECT]


    @property
    def responsible_parties(self):
        """Gets full set of managed responsible parties.

        """
        return reduce(add, [i.responsible_parties for i in self.responsible_party_containers])


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


    def _set_derived_info(self):
        """Assign information derived from document set.

        """
        # Experimental tier is derived from 2nd keyword.
        for e in self[WS_EXPERIMENT]:
            e.tier = int(e.keywords.split(",")[1][-1])


    def _set_data_request_info(self):
        """Sets information dervied from the CMIP6 data request.

        """
        def _do(p, mip):
            if not mip or p.name.lower() == 'cmip':
                return
            if mip.url not in (None, 'None'):
                p.homepage = mip.url
            p.objectives = ["{}: {}".format(o.label, o.description) for o in mip.objectives]
            p.objectives = sorted(p.objectives)

        for p in self[WS_PROJECT]:
            _do(p, pyesdoc.drq.query('mip', p.canonical_name))


    def ignore_documents(self):
        """Filters out documents deemed unworthy of persisting.

        """
        self[WS_EXPERIMENT] = [e for e in self[WS_EXPERIMENT] if e.canonical_name and e.canonical_name.lower() != "n/a"]


    def set_document_connections(self):
        """Sets inter document connections.

        """
        # Set urls.
        for x in self.url_containers:
            x.url = convert_name(x.url, self[WS_URL])

        # Set data links.
        for x in [i for i in self[WS_FORCING_CONSTRAINT] if i.data_link]:
            if x.data_link == 'TBD':
                x.data_link = None
                continue
            url = convert_name(x.data_link, self[WS_URL])
            if url is None:
                print 'INVALID FORCING CONSTRAINT DATA LINK:', x.data_link
            else:
                dataset = cim.v2.Dataset()
                dataset.availability.append(url)
                dataset.name = url.name
                x.data_link = dataset

        # Set citations.
        for x in self.citation_containers:
            x.citations = convert_names("citations", x.citations, self[WS_CITATIONS])

        # Set responsibility parties.
        for rp in self.responsible_parties:
            rp.parties = convert_names(WS_PARTY, rp.parties, self[WS_PARTY])

        # Set intra-experiment relationships.
        for e in self[WS_EXPERIMENT]:
            for r in {"is_constrained_by", "is_perturbation_from", "is_initialized_by", "is_sibling_of"}:
                setattr(e, r, convert_names("exp-to-exp", getattr(e, r), self[WS_EXPERIMENT]))
        for e in self[WS_EXPERIMENT]:
            for r in {"is_constrainer_of", "is_control_for", "is_initializer_of"}:
                setattr(e, r, [])
        for e in self[WS_EXPERIMENT]:
            for r_exp in e.is_constrained_by:
                r_exp.is_constrainer_of.append(e)
            for r_exp in e.is_perturbation_from:
                r_exp.is_control_for.append(e)
            for r_exp in e.is_initialized_by:
                r_exp.is_initializer_of.append(e)
        for e in self[WS_EXPERIMENT]:
            for r in {"is_constrainer_of", "is_control_for", "is_initializer_of"}:
                setattr(e, r, list(set(getattr(e, r))))

        # Set experiment requirements.
        for e in self[WS_EXPERIMENT]:
            e.temporal_constraints = \
                convert_names(WS_TEMPORAL_CONSTRAINT, e.temporal_constraints, self[WS_TEMPORAL_CONSTRAINT])
            e.forcing_constraints = [convert_name(i, self[WS_FORCING_CONSTRAINT]) or
                                     convert_name(i, self[WS_REQUIREMENT])
                                     for i in e.forcing_constraints]
            e.ensembles = \
                convert_names(WS_ENSEMBLE_REQUIREMENT, e.ensembles, self[WS_ENSEMBLE_REQUIREMENT])
            e.model_configurations = \
                convert_names(WS_REQUIREMENT, e.model_configurations, self[WS_REQUIREMENT])
            e.multi_ensembles = \
                convert_names(WS_MULTI_ENSEMBLE, e.multi_ensembles, self[WS_MULTI_ENSEMBLE])

        # Set project sub-projects.
        for p in self[WS_PROJECT]:
            pass

        # Set experiment governing mip.
        for e in self[WS_EXPERIMENT]:
            e.governing_mips = convert_names("exp-to-project", e.governing_mips, self[WS_PROJECT], slots=["name"], collection_name=e.name)
            for p in e.governing_mips:
                p.governed_experiments.append(e)

        # Set experiment sub-projects.
        for e in self[WS_EXPERIMENT]:
            for project in self[WS_PROJECT]:
                if e.canonical_name in project.required_experiments:
                    e.meta.sub_projects.append(project.name)
                    e.related_mips.append(project)
            e.meta.sub_projects = sorted(e.meta.sub_projects)

        # Set additional experimental requirements.
        for rq in self[WS_REQUIREMENT]:
            rq.additional_requirements = \
                convert_names("additional requirements", rq.additional_requirements, self.numerical_requirements)

        # Set multi-ensemble axis.
        for me in self[WS_MULTI_ENSEMBLE]:
            me.ensemble_axis = convert_names("multi-ensemble", me.ensemble_axis, self.numerical_requirements)

        # Set sub-projects.
        for p in self[WS_PROJECT]:
            p.meta.sub_projects = sorted(p.sub_projects)
            p.sub_projects = convert_names("sub-projects", p.sub_projects, self[WS_PROJECT])

        # Set project required experiments.
        for p in self[WS_PROJECT]:
            p.required_experiments = convert_names("prj-to-exp", p.required_experiments, self[WS_EXPERIMENT], collection_name=p.name)

        # Set governed experiments - order as per required experiments.
        for p in self[WS_PROJECT]:
            governed_experiments = [i for i in p.required_experiments if i in p.governed_experiments]
            governed_experiments += sorted(list(set(p.governed_experiments) - set(governed_experiments)), key=lambda i: i.name)
            p.governed_experiments = governed_experiments


    def set_document_links(self):
        """Sets inter document links.

        """
        def set_links(doc, doc_attr, fi_attr=None):
            """Helper function to assign a collection of links.

            """
            links = []
            for i in getattr(doc, doc_attr):
                links.append(self._get_doc_link(i))
                if fi_attr:
                    links[-1].further_info = str(getattr(i, fi_attr))

            setattr(doc, doc_attr, links)

        # Responsible parties.
        for rp in self.responsible_parties:
            set_links(rp, "parties")

        # Citations.
        for c in self.citation_containers:
            set_links(c, "citations")

        # Experiments.
        for e in self[WS_EXPERIMENT]:
            for r in EXPERIMENTAL_RELATIONSHIP_TYPES:
                for re in [self._get_doc_link(d) for d in getattr(e, r)]:
                    re.relationship = r
                    e.related_experiments.append(re)
                delattr(e, r)

        # Experimental requirements.
        for e in self[WS_EXPERIMENT]:
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
        for r in self[WS_REQUIREMENT]:
            set_links(r, "additional_requirements")

        # Experiment --> MIP.
        for e in self[WS_EXPERIMENT]:
            set_links(e, "governing_mips")
            set_links(e, "related_mips")

        # Project --> Project.
        for p in self[WS_PROJECT]:
            set_links(p, "sub_projects")

        # Project --> Experiment.
        for p in self[WS_PROJECT]:
            set_links(p, "required_experiments", "tier")
            set_links(p, "governed_experiments", "tier")


    def write(self, io_dir):
        """Writes documents to file system.

        """
        def _write(doc, encoding):
            """Writes document to file system.

            """
            pyesdoc.write(doc, io_dir, encoding=encoding)

        # Remove helper attributes that do not need to be serialized.
        for experiment in self[WS_EXPERIMENT]:
            del experiment.temporal_constraints
            del experiment.forcing_constraints
            del experiment.ensembles
            del experiment.model_configurations
            del experiment.multi_ensembles

        for doc in self.documents:
            _write(doc, pyesdoc.constants.ENCODING_JSON)
