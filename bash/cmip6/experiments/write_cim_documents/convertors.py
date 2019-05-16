# -*- coding: utf-8 -*-

"""
.. module:: convertors.py
   :license: GPL/CeCIL
   :platform: Unix, Windows
   :synopsis: Various conversion functions.

.. moduleauthor:: Mark Conway-Greenslade <momipsl@ipsl.jussieu.fr>

"""
import collections
import string

import pyesdoc.ontologies.cim as cim

from constants import *



# Names that could not be converted to documents ... i.e. cell reference issues.
UNCONVERTED_NAMES = collections.defaultdict(set)



def convert_to_bool(value):
    """Converts a cell value to a boolean.

    """
    return unicode(value).lower() in [u'true', u't', u'yes', u'y', u"1"]


def convert_to_unicode(value):
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


def convert_to_int(value):
    """Converts a cell value to an integer.

    """
    return None if value is None else int(value)


def convert_to_string_array(value):
    """Converts a cell value to an array of strings.

    """
    return [] if value is None else value.split(", ")


def convert_to_cim_v2_calendar(value):
    """Converts a cell value to a cim.v2.DateTime instance.

    """
    if value is None:
        return

    # TODO
    return
    raise NotImplementedError("CIM v2 Calendar value needs to be converted from cell content")


def convert_to_cim_v2_time_period(value):
    """Converts a cell value to a cim.v2.TimePeriod instance.

    """
    if value is None:
        return

    instance = cim.v2.TimePeriod()
    instance.length = value.split(" ")[0]
    instance.units = value.split(" ")[1]
    instance.date_type = u'unused'

    return instance


def convert_to_cim_v2_numerical_requirement_scope(value, other):
    """Converts a cell value to a cim.v2.NumericalRequirementScope enum value.

    """
    if value is not None:
        return {
            1: "mip-era",
            2: "mip-group",
            3: "mip",
            4: "experiment",
        }[abs(value)]


def convert_to_cim_v2_date_time(value, offset):
    """Converts a cell value to a cim.v2.DateTime instance.

    """
    if value is None:
        return

    instance = cim.v2.DateTime()
    instance.value = value
    instance.offset = convert_to_bool(offset)

    return instance


def convert_to_cim_v2_responsibilty(role, row, col_idx):
    """Returns experiment responsibility info.

    """
    if role is None:
        return

    col_from = convert_col_idx(col_idx.split("-")[0])
    col_to = convert_col_idx(col_idx.split("-")[1])
    offsets = range(col_to - col_from + 1)

    responsibility = cim.v2.Responsibility()
    responsibility.role = convert_to_unicode(role)
    responsibility.parties = [i for i in [row(col_from + j) for j in offsets] if i]

    return responsibility


def convert_name(
    name,
    collection,
    slots=["citation_detail", "canonical_name", "name"]
    ):
    """Converts a document name.

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
        name = name.strip()
        if len(name) == 0:
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


def convert_names(
    collection_type,
    names,
    collection,
    slots=["citation_detail", "canonical_name", "name"],
    collection_name=None
    ):
    """Converts a set of names.

    """
    result = []
    for name in names:
        doc = convert_name(name, collection, slots)
        if doc is None:
            UNCONVERTED_NAMES[collection_type].add('{}:{}:{}'.format(collection_name, name, slots))
        else:
            result.append(doc)

    return result


def convert_col_idx(col_idx):
    """Converts a column index to an integer.

    """
    num = 0
    for c in col_idx:
        if c in string.ascii_letters:
            num = num * 26 + (ord(c.upper()) - ord('A')) + 1
    return num
