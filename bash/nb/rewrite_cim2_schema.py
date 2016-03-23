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
from collections import defaultdict

from esdoc_nb.mp.core.schema.cim2 import activity_classes
from esdoc_nb.mp.core.schema.cim2 import data_classes
from esdoc_nb.mp.core.schema.cim2 import designing_classes
from esdoc_nb.mp.core.schema.cim2 import drs_entities
from esdoc_nb.mp.core.schema.cim2 import platform_classes
from esdoc_nb.mp.core.schema.cim2 import science_classes
from esdoc_nb.mp.core.schema.cim2 import science_enums
from esdoc_nb.mp.core.schema.cim2 import shared_classes
from esdoc_nb.mp.core.schema.cim2 import software_classes
from esdoc_nb.mp.core.schema.cim2 import software_enums
from esdoc_nb.mp.core.schema.cim2 import time as time_classes



# Define command line options.
_ARGS = argparse.ArgumentParser("Rewrites notebook's CIM v2 ontology schema to esdoc-mp compatible schema.")
_ARGS.add_argument(
    "--dest",
    help="Path to a directory into which esdoc-mp compatible schema will be written.",
    dest="dest",
    type=str
    )


# Report line break.
_LINE_BREAK = '\n'

# Report section break.
_SECTION_BREAK = '------------------------------------------------------------------------------\n'

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
    software_classes,
    software_enums,
    time_classes
    ])


# Set of class constructs imported from notebook.
_CLASS_CONSTRUCTS = {
    'base', 'constraints', 'derived', 'is_abstract', 'properties', 'type', 'pstr'
}

# Set of enum constructs imported from notebook.
_ENUM_CONSTRUCTS = {
    'is_open', 'members', 'type'
}

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
        ]{constraints}{derived}
'''

# Code template for enum factory.
_ENUM = '''
        'is_open': {is_open},
        'members': [{members}]
'''

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

    doc_string = doc_string.strip()
    if len(doc_string) == 0:
        return "None"

    if doc_string[-1] != ".":
        doc_string += "."
    doc_string = doc_string.replace('"', "'")

    return doc_string


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


    def __repr__(self):
        """Instance representation.

        """
        return self.full_name


    @property
    def doc_string(self):
        """Returns type declaration doc string.

        """
        if not self.factory.__doc__ or not self.factory.__doc__.strip():
            print "WARNING: function without doc string: {}.{}".format(self.package, self.name)
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
    @property
    def ommitted_keys(self):
        return [k for k in self.definition.keys() if k not in _CLASS_CONSTRUCTS]


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

            # Remap package where appropriate.
            if base.split(".")[0] in _PACKAGE_REFORMAT_MAP:
                base = "{0}.{1}".format(_PACKAGE_REFORMAT_MAP[base.split(".")[0]],
                                        base.split(".")[1])

            return "'{}'".format(base)


        def _get_print_string():
            """Returns code snippet for a class print string.

            """
            pstr = self.definition.get('pstr', None)
            if pstr is None:
                return ""

            pstr = (pstr[0].replace("%s", "{}"), pstr[1])

            return "\n        'pstr': {},".format(pstr)


        def _get_linked_to_property_type(prop_type):
            """Reformats a linked to property type definition.

            """
            # ... extract linked to fields
            defn = [i.strip() for i in prop_type[10:-1].split(",")]
            target = defn[0]
            qualifier = None if len(defn) == 1 else defn[1]

            # ... reset property type
            if target.find(".") == -1:
                target = "{}.{}".format(self.package, target)
            if qualifier and qualifier.find(".") == -1:
                qualifier = "{}.{}".format(self.package, qualifier)

            if qualifier:
                return "linked_to({}, {})".format(target, qualifier)

            return "linked_to({})".format(target)


        def _get_property_type(prop_name, prop_type):
            """Reformats a property type definition.

            """
            # Override document meta attributes.
            if prop_name == "meta":
                return "shared.doc_meta_info"

            # Ensure property types are lower case.
            prop_type = prop_type.lower()

            # Linked to properties.
            if prop_type.startswith('linked_to'):
                return _get_linked_to_property_type(prop_type)

            # Override text type.
            elif prop_type in ('text', 'shared.cimtext'):
                return 'str'

            # Override complex type reference.
            elif len(prop_type.split(".")) == 2:
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


        def _get_derived_property(member):
            """Returns code snippet for a derived member.

            """
            name, derivation = member

            return "            ('{}', '{}')".format(name, derivation)


        def _get_constrained_property(member):
            """Returns code snippet for a constrained member.

            """
            if member[1] == 'hidden':
                member = (member[0], "cardinality", "0.0")

            name, typeof, value = member

            return "            ('{}', '{}', '{}')".format(name, typeof, value)


        def _get_constraints(members):
            """Returns code snippet for a set of constrained properties.

            """
            if not members:
                return ""

            code = ",\n"
            code += "        'constraints': [\n"
            code += ",\n".join(_get_constrained_property(m) for m in sorted(members, key=lambda m: m[0]))
            code += "\n"
            code += "        ]\n"

            return code


        def _get_derived(members):
            """Returns code snippet for a set of derived properties.

            """
            if not members:
                return ""

            code = ",\n"
            code += "        'derived': [\n"
            code += ",\n".join(_get_derived_property(m) for m in sorted(members, key=lambda m: m[0]))
            code += "\n"
            code += "        ]\n"

            return code

        result = _CLASS
        result = result.replace("{base_class}", _get_base_class())
        result = result.replace("{pstr}", _get_print_string())
        result = result.replace("{is_abstract}", "{}".format(self.definition.get("is_abstract", False)))
        result = result.replace("{properties}", _get_properties(self.definition.get("properties", [])))
        result = result.replace("{derived}", _get_derived(self.definition.get("derived", [])))
        result = result.replace("{constraints}", _get_constraints(self.definition.get("constraints", [])))

        return result


class _EnumTypeFactory(_TypeFactory):
    """A type factory that returns an enum definition compatible with esdoc-mp.

    """
    @property
    def ommitted_keys(self):
        return [k for k in self.definition.keys() if k not in _ENUM_CONSTRUCTS]


    def get_definition(self):
        """Gets new enum definition compatible with esdoc-mp.

        """
        def _get_member(member):
            """Returns code snippet for an enum member.

            """
            name = member[0].strip()
            doc = member[1]
            if not doc:
                doc = "None"
            else:
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


# Map of definition types to factories.
_DEFINITION_TYPE_FACTORY_MAP = {
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
                yield _DEFINITION_TYPE_FACTORY_MAP[definition['type']](self.mod, name, factory, definition)


    def write(self, ommitted):
        """Writes code to file system.

        """
        with open(self.dest, 'w') as output:
            output.write(self.code_header)
            for type_factory in self.yield_type_factories():
                output.write("\n\n")
                output.write(type_factory.get_code())
                # Remember definitions ommitted from rewrite.
                for key in type_factory.ommitted_keys:
                    ommitted[key].add(type_factory)


def _write_ommitted_definitions(ommitted):
    """Writes to stdout the set of ommitted definitions.

    """
    fpath = __file__.replace(".py", ".txt")
    if os.path.exists(fpath):
        os.remove(fpath)

    with open(fpath, 'w') as report:
        for key in sorted(ommitted.keys()):
            report.write(_SECTION_BREAK)
            report.write("Skipped construct = {}".format(key))
            report.write(_LINE_BREAK)
            for type_factory in sorted(ommitted[key], key=lambda i: i.full_name):
                if isinstance(type_factory, _ClassTypeFactory):
                    report.write("\t{} (cls)".format(type_factory.full_name))
                else:
                    report.write("\t{} (enum)".format(type_factory.full_name))
                report.write(_LINE_BREAK)
            report.write(_LINE_BREAK)


def _main(args):
    """Main entry point.

    """
    ommitted = defaultdict(set)
    modules = [_Module(m, args.dest) for m in _MODULE_SET]
    for mod in modules:
        mod.write(ommitted)

    if ommitted:
        _write_ommitted_definitions(ommitted)


# Entry point.
if __name__ == '__main__':
    _main(_ARGS.parse_args())
