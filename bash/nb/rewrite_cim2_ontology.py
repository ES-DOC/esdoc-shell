# -*- coding: utf-8 -*-

"""
.. module:: rewrite_cim2_schema.py
   :platform: Unix, Windows
   :synopsis: Rewrites esdoc-nb cim 2 ontology schema definitions to esdoc-mp.

.. moduleauthor:: Mark Conway-Greenslade <momipsl@ipsl.jussieu.fr>


"""
import argparse
import inspect
import os

from esdoc_nb.mp.core.schema.cim2 import activity_classes
from esdoc_nb.mp.core.schema.cim2 import data_classes
from esdoc_nb.mp.core.schema.cim2 import designing_classes
from esdoc_nb.mp.core.schema.cim2 import drs_entities
from esdoc_nb.mp.core.schema.cim2 import platform_classes
from esdoc_nb.mp.core.schema.cim2 import science_classes
from esdoc_nb.mp.core.schema.cim2 import science_enums
from esdoc_nb.mp.core.schema.cim2 import shared_classes
# from esdoc_nb.mp.core.schema.cim2 import shared_classes_doc
from esdoc_nb.mp.core.schema.cim2 import shared_classes_time
from esdoc_nb.mp.core.schema.cim2 import software_classes
from esdoc_nb.mp.core.schema.cim2 import software_enums



# Define command line options.
_ARGS = argparse.ArgumentParser("Rewrites notebook's CIM v2 ontology schema to esdoc-mp compatible schema.")
_ARGS.add_argument(
    "--dest",
    help="Path to a directory into which esdoc-mp compatible schema will be written.",
    dest="dest",
    type=str
    )


# Set of modules to be rewritten.
_MODULE_SET = set([
    activity_classes,
    data_classes,
    designing_classes,
    drs_entities,
    platform_classes,
    science_classes,
    science_enums,
    shared_classes,
    # shared_classes_doc,
    shared_classes_time,
    software_classes,
    software_enums
    ])


# Code template for module header.
_MOD_HEADER = '''# -*- coding: utf-8 -*-

"""
.. module:: {mod_name}.py
   :synopsis: Set of CIM v2 ontology type definitions.

"""
'''


# Code template for type factory header.
_TYPE_FACTORY = '''def {func_name}():
    """{func_doc}

    """
    return {
        'type': '{func_type}',
        {func_body}
    }
'''

# Code template for class factory.
_CLASS = '''
        'base': {base_class},
        'is_abstract': {is_abstract},{pstr}
        'properties': [{properties}
        ]
'''

# Code template for enum factory.
_ENUM = '''
        'is_open': {is_open},
        'members': [{members}]
'''

# Map of reformtted base class names.
_BASE_CLASS_REFORMAT_MAP = {
    "designing.activity": 'activity.activity'
}

# Map of package names to reformatted package names.
_PACKAGE_REFORMAT_MAP = {
    "shared_time": 'shared'
}

# Set of types to be excluded.
_TYPE_BLACKLIST = {
    'shared.meta',
    'shared.minimal_meta'
}


def _format_doc_string(doc_string):
    """Returns a formatted document string.

    """
    if doc_string is None:
        return "None"

    result = doc_string.strip()
    if result[-1] != ".":
        result += "."
    result = result.replace('"', "'")

    return result


class _TypeFactory(object):
    """Wraps an otology type factory.

    """
    def __init__(self, mod, name, factory, definition):
        """Instance constructor.

        """
        self.definition = definition
        self.mod = mod
        self.name = name
        self.factory = factory


    @property
    def doc_string(self):
        """Returns type declaration doc string.

        """
        return _format_doc_string(self.factory.__doc__)


    @property
    def package(self):
        """Returns associated ontology package name.

        """
        return self.mod.__name__.split(".")[-1].split("_")[0]


    @property
    def full_name(self):
        """Returns associated ontology package name.

        """
        return "{}.{}".format(self.package, self.name)


    def get_code(self):
        """Gets type factory rewritten code.

        """
        result = _TYPE_FACTORY
        result = result.replace("{func_name}", self.name)
        result = result.replace("{func_doc}", self.doc_string)
        result = result.replace("{func_type}", self.definition["type"])
        result = result.replace("{func_body}", self.get_definition().strip())

        return result


class _ClassTypeFactory(_TypeFactory):
    """A type factory that returns a class definition compatible with esdoc-mp.

    """
    def get_definition(self):
        """Gets new class definition compatible with esdoc-mp.

        """
        def _get_base_class():
            """Gets reformatted base class reference.

            """
            base = self.definition.get('base', None)
            if base is None:
                return "None"

            # Ensure base class references are lower case.
            if base:
                base = base.lower()

            # Ensure that base class references are prefixed with package name.
            if base and len(base.split('.')) != 2:
                base = "{0}.{1}".format(self.package, base)

            # Remap where appropriate.
            try:
                base = _BASE_CLASS_REFORMAT_MAP[base]
            except KeyError:
                pass

            return "'{}'".format(base)


        def _get_print_string():
            """Returns code snippet for a class print string.

            """
            pstr = self.definition.get('pstr', None)
            if pstr is None:
                return ""

            return "\n        'pstr': {},".format(pstr)


        def _get_property_type(prop_name, prop_type):
            """Reformats a property type definition.

            """
            # Override document meta attributes.
            if prop_name == "meta":
                return "shared.doc_meta_info"

            # Ensure property types are lower case.
            prop_type = prop_type.lower()

            # Ensure linked_to references are stripped out.
            if prop_type.startswith('linked_to'):
                prop_type = prop_type[10:-1]
                if prop_type.find(".") == -1:
                    prop_type = "{}.{}".format(self.package, prop_type)

            # Override text type.
            if prop_type in ('text', 'shared.cimtext'):
                prop_type = 'str'

            # Override complex type reference.
            if len(prop_type.split(".")) == 2:
                pkg, cls = prop_type.split(".")
                try:
                    pkg = _PACKAGE_REFORMAT_MAP[pkg]
                except KeyError:
                    pass
                else:
                    prop_type = ".".join([pkg, cls])

            return prop_type


        def _get_doc_string(member):
            """Returns code snippet for a class doc string.

            """
            # Derive from property definition.
            if len(member) == 4:
                doc_string = member[3]
            # Derive from doc_strings definition.
            elif member[0] in self.definition.get("doc_strings", dict()):
                doc_string = self.definition["doc_strings"][member[0]]
            # Undefined.
            else:
                print "WARNING: property without doc string: {}.{} --> {}".format(self.package, self.name, member[0])
                doc_string = None

            return _format_doc_string(doc_string)


        def _get_property(member):
            """Returns code snippet for a class property.

            """
            name = member[0].strip()
            typeof = _get_property_type(name, member[1].strip())
            cardinality = member[2].strip()
            doc_string = _get_doc_string(member)

            result = '\n            '
            result += "('{}', '{}', '{}',".format(name, typeof, cardinality)
            result += '\n                '
            result += '"{}")'.format(doc_string)

            return result


        def _get_properties(members):
            """Returns code snippet for a set of class properties.

            """
            properties = [_get_property(m) for m in members]

            return ",".join(sorted(properties))


        result = _CLASS
        result = result.replace("{base_class}", _get_base_class())
        result = result.replace("{pstr}", _get_print_string())
        result = result.replace("{is_abstract}", "{}".format(self.definition.get("is_abstract", False)))
        result = result.replace("{properties}", _get_properties(self.definition.get("properties", [])))

        return result


class _EnumTypeFactory(_TypeFactory):
    """A type factory that returns an enum definition compatible with esdoc-mp.

    """
    def get_definition(self):
        """Gets new enum definition compatible with esdoc-mp.

        """
        def _get_member(member):
            """Returns code snippet for an enum member.

            """
            name = member[0].strip()
            doc = member[1]
            if doc:
                doc = '"{}"'.format(doc.strip())

            return '\n            ("{}", {})'.format(name, doc)


        def _get_members(members):
            """Returns code snippet for a set of enum members.

            """
            code = ""
            for idx, member in enumerate(members):
                code += _get_member(member)
                code += "," if idx < len(members) - 1 else "\n        "

            return code

        result = _ENUM
        result = result.replace("{is_open}", "{}".format(self.definition.get("is_open", False)))
        result = result.replace("{members}", _get_members(self.definition.get("members", [])))

        return result


_TYPE_FACTORY_MAP = {
    "class": _ClassTypeFactory,
    "enum": _EnumTypeFactory
}


class _Module(object):
    """Wraps a module to be rewritten.

    """
    def __init__(self, mod, dest):
        """Instance constructor.

        """
        self.name = mod.__name__.split(".")[-1]
        self.package = self.name.split("_")[0]
        self.mod = mod
        self.dest = os.path.join(dest, self.name) + ".py"
        self.code_header = _MOD_HEADER.replace("{mod_name}", self.name)


    def yield_type_factories(self):
        """Yields set of type factories to be rewritten.

        """
        for name, factory in inspect.getmembers(self.mod, inspect.isfunction):
            definition = factory()
            if "{}.{}".format(self.package, name) not in _TYPE_BLACKLIST:
                yield _TYPE_FACTORY_MAP[definition['type']](self.mod, name, factory, definition)


    def write(self):
        """Writes code to file system.

        """
        print self.dest
        with open(self.dest, 'w') as output:
            output.write(self.code_header)

            # for type_factory in self.yield_type_factories():
            #     output.write("\n\n")
            #     output.write(type_factory.get_code())


def _main(args):
    """Main entry point.

    """
    modules = [_Module(m, args.dest) for m in _MODULE_SET]
    return
    for mod in modules:
        mod.write()



# Entry point.
if __name__ == '__main__':
    _main(_ARGS.parse_args())
