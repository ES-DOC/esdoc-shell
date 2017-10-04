import collections
import csv
import glob
import os

import pyesdoc
from pyesdoc.ontologies import cim



# Map of CMIP5 to CMIP6 role codes.
_ROLE_CODES = {
    "pi": "Principal Investigator",
    "funder": "sponsor",
    "contact": "point of contact",
    "centre": "custodian"
}



def map(m):
    """Maps a CMIP5 model component to a CIM v2 document.

    :param cim.v1.Model m: CMIP5 CIM v1 model document.

    :returns: CMIP6 IPython notebook output.
    :rtype: dict

    """
    return

    doc = _create_doc(cim.v2.Model, m.meta.institute)
    doc.citations = [_map_citation(m, i) for i in m.citations]
    doc.description = m.description
    doc.long_name = m.long_name
    doc.name = m.short_name
    doc.release_date = m.release_date
    doc.responsible_parties = [_map_responsibility(m, i) for i in m.responsible_parties]

    # Build collection of values to be emitted.
    values = []
    for c in m.ext.component_tree:
        for p in c.ext.scientific_property_tree:
            for v in p.values:
                cmip5_id = p.ext.full_display_name.lower()
                cmip5_id = "cmip5{}".format(cmip5_id)
                cmip5_id = cmip5_id.replace(" > ", ".")
                cmip5_id = cmip5_id.replace(" >> ", ".")
                cmip5_id = cmip5_id.replace(" ", "_")
                cmip5_id = cmip5_id.replace("scientific_properties.", "")
                values.append((cmip5_id, c, p, v))

    for cmip5_id, c, p, v in values:
        print cmip5_id, " :: ", v, cmip5_id in _MAPPINGS

    return doc


def _map_citation(m, c):
    """Returns a cim.v2.Citation instance.

    """
    doc = _create_doc(cim.v2.Citation, m.meta.institute)
    doc.collective_title = c.collective_title
    doc.title = c.title
    doc.type = c.type
    if c.location:
        doc.url = _map_online_resource(c.location, c.title)

    return doc


def _map_responsibility(m, rp):
    """Returns a cim.v2.Responsibility instance.

    """
    doc = _create_doc(cim.v2.Responsibility, m.meta.institute)
    doc.role = _ROLE_CODES[rp.role.lower()]
    doc.party = _map_party(m, rp)

    return doc


def _map_party(m, rp):
    """Returns a cim.v2.Party instance.

    """
    doc = _create_doc(cim.v2.Party, m.meta.institute)
    doc.address = rp.address
    doc.email = rp.email
    if rp.individual_name is not None:
        doc.name = rp.individual_name
    else:
        doc.name = rp.organisation_name
        doc.is_organisation = True
    if rp.url:
        doc.url = _map_online_resource(rp.url, doc.name)

    return doc


def _map_online_resource(url, name):
    """Returns a cim.v2.OnlineResource instance.

    """
    if not url.startswith("http"):
        url = "http://{}".format(url)
    i = pyesdoc.create(cim.v2.OnlineResource)
    i.linkage = url
    i.name = name

    return i


def _create_doc(typeof, institute):
    """Returns a document or document fragment.

    """
    return pyesdoc.create(
        typeof,
        project="cmip5",
        institute=institute,
        source="script"
        )

