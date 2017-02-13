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

_mappings = collections.OrderedDict()


def map_model(m):
    """Maps a cim.v1.Model.

    """
    doc = _create_doc(cim.v2.Model, m)

    doc.citations = [map_citation(m, i) for i in m.citations]
    doc.description = m.description
    doc.long_name = m.long_name
    doc.name = m.short_name
    doc.release_date = m.release_date
    doc.responsible_parties = [map_responsibility(m, i) for i in m.responsible_parties]

    for c in m.ext.component_tree:
        pyesdoc.extend(c)
        print c.type
        for p in c.properties:
            pyesdoc.extend(p)
            print p.ext
            print p.short_name
        # print c.type, c.type in _mappings

    return doc


def map_citation(m, c):
    """Maps a cim.v2.Citation.

    """
    doc = _create_doc(cim.v2.Citation, m)
    doc.collective_title = c.collective_title
    doc.title = c.title
    doc.type = c.type
    if c.location:
        doc.url = map_online_resource(c.location, c.title)

    return doc


def map_responsibility(m, rp):
    """Maps a cim.v2.Responsibility.

    """
    doc = _create_doc(cim.v2.Responsibility, m)
    doc.role = _ROLE_CODES[rp.role.lower()]
    doc.party = map_party(m, rp)

    return doc


def map_party(m, rp):
    """Maps a cim.v2.Party.

    """
    doc = _create_doc(cim.v2.Party, m)
    doc.address = rp.address
    doc.email = rp.email
    if rp.individual_name is not None:
        doc.name = rp.individual_name
    else:
        doc.name = rp.organisation_name
        doc.is_organisation = True
    if rp.url:
        doc.url = map_online_resource(rp.url, doc.name)

    return doc


def map_online_resource(url, name):
    """Maps a cim.v2.OnlineResource.

    """
    if not url.startswith("http"):
        url = "http://{}".format(url)
    i = pyesdoc.create(cim.v2.OnlineResource)
    i.linkage = url
    i.name = name

    return i


def _create_doc(typeof, m):
    """Returns a document or document fragment.

    """
    return pyesdoc.create(typeof, project="cmip6", institute=m.meta.institute, source="script")


def get_realm_mappings(realm):
    for k in _mappings:
        if k.startswith(realm):
            print k
    print 666, realm


def init():
    """Initialises set of mappers.

    """
    dpath = os.path.dirname(__file__)
    dpath = os.path.join(dpath, "mappings")

    mappings = dict()
    for fpath in glob.glob(os.path.join(dpath, "*.csv")):
        typeof = fpath.split("/")[-1].split(".")[1]
        data = [i for i in csv.reader(open(fpath, 'r'))][1:]
        for row in data:
            if typeof == "component-tree":
                mappings[row[1]] = row[2]

    for k in sorted(mappings.keys()):
        _mappings[k] = mappings[k]

