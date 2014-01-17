import datetime
import uuid
import xml.etree.ElementTree as ET

from dateutil import parser as date_parser

import pyesdoc
from pyesdoc import ontologies
from pyesdoc.utils import convert_to_camel_case
from pyesdoc.utils import runtime as rt



# Set of ontology types.
_TYPES = ontologies.get_types()


def _decode_scalar(sv, type, iterable):
    """Decodes a scalar value."""
    def _do(s):
        s = s.encode('utf-8') if isinstance(s, unicode) else str(s)

        if type in (datetime.datetime, datetime.date, datetime.time):
            return date_parser.parse(s)
        elif type is uuid.UUID:
            return uuid.UUID(s)
        elif type is bool:
            if s.lower() in ("yes", "true", "t", "1", "y"):
                return True
            return False
        else:
            try:
                return type(s)
            except Error as e:
                print "Scalar decoding error", s, type, iterable

    return map(lambda i : _do(i), sv) if iterable else _do(sv)


def _decode(repr, typeof, iterable):
    """Decodes an xml element."""        
    def _do(xml):
        # Set doc type.
        doc_type = typeof
        if typeof.type_key != xml.get('ontologyTypeKey'):
            doc_type = ontologies.get_type_from_key(xml.get('ontologyTypeKey'))
        if doc_type is None:
            rt.raise_error('Decoding type is unrecognized')
    
        # Create doc.
        doc = doc_type()

        # Set doc attributes.
        for _name, _type, _required, _iterable in ontologies.get_type_info(doc_type):
            elem = xml.find(convert_to_camel_case(_name))
            # ... not found therefore ignore.
            if elem is None:
                continue
            # ... no sub-elements/value therefore None.
            elif not len(elem) and (elem.text is None or not len(elem.text.strip())):
                setattr(doc, _name, [] if _iterable else None)
            # ... supported type therefore decode.
            elif _type in _TYPES:
                setattr(doc, _name, _decode(elem, _type, _iterable))
            else:
                setattr(doc, _name, _decode_scalar(elem.text, _type, _iterable))

        return doc

    return _do(repr) if not iterable else map(lambda i : _do(i), repr)


def decode(repr):
    """Decodes a document from an xml string.

    :param repr: Document xml representation.
    :type repr: str | xml.etree.ElementTree

    :returns: A pyesdoc document instance.
    :rtype: object

    """
    # Convert to etree.
    xml = repr if type(repr) == ET else ET.fromstring(repr)

    # Get target type.
    o, v, p, t = xml.get("ontologyTypeKey").split('.')
    doc_type = pyesdoc.ontologies.get_type(o, v, p, t)

    print dir(xml)
    return _decode(xml, doc_type, False)


DOC_PATH = "/Users/macg/dev/prj/esdoc/repos/esdoc-py-client/tests/pyesdoc_test/files/xml-metafor-cim-v1/cim.1.shared.Platform.xml"
DOC_PROJECT = "CMIP5"
DOC_INSTITUTE = "MOHC"

def get_doc_as_xml():
    doc = pyesdoc.decode(DOC_PATH, pyesdoc.METAFOR_CIM_XML_ENCODING)
    doc.doc_info.project = "CMIP5"
    doc.doc_info.institute = "MOHC"
    xml_repr = pyesdoc.encode(doc, pyesdoc.ESDOC_ENCODING_XML)

    return xml_repr






print decode(get_doc_as_xml())

