#! /usr/bin/python

import sys

import esdoc_mp


# Set target language.
_LANGUAGE = "python"


def get_test_classes():
    """Returns list of test ontology class definitions.

	"""
    def test_class_a():
        return {
            'type': 'class',
            'name': 'test_class_a',
            'base': None,
            'abstract': True,
            'doc': 'Test class A documentation.',
            'properties': [
                ('x', 'int', '0.1', 'Property x documentation.'),
            ]
        }

    def test_class_b():
        return {
            'type': 'class',
            'name': 'test_class_b',
            'base': None,
            'abstract': False,
            'doc': 'Test class B documentation.',
            'properties': [
                ('y', 'int', '0.N', 'Property y documentation.'),
            ]
        }

    def test_class_c():
        return {
            'type': 'class',
            'name': 'test_class_c',
            'base': 'test_package.test_class_a',
            'abstract': False,
            'doc': 'Test class C documentation.',
            'properties': [
                ('z', 'bar.class_b', '0.N', 'Property z documentation'),
            ]
        }

    return [
        test_class_a(),
        test_class_b(),
        test_class_c(),
    ]


def get_test_enums():
    """Returns list of test ontology enum definitions.

	"""
    def test_enum_a():
        return {
            'type': 'enum',
            'name': 'test_enum_a',
            'is_open': False,
                'doc': 'Test enum A documentation.',
            'members': [
                ('enum member 1', 'enum A - member 1 documentation.'),
                ('enum member 2', 'enum A - member 2 documentation.'),
                ('enum member 3', 'enum A - member 3 documentation.'),
                ('enum member 4', 'enum A - member 4 documentation.'),
            ]
        }

    def test_enum_b():
        return {
            'type': 'enum',
            'name': 'test_enum_b',
            'is_open': True,
                'doc': 'Test enum B documentation.',
            'members': [
                ('enum member 1', 'enum B - member 1 documentation.'),
                ('enum member 2', 'enum B - member 2 documentation.'),
                ('enum member 3', 'enum B - member 3 documentation.'),
                ('enum member 4', 'enum B - member 4 documentation.'),
            ]
        }

    return [
        test_enum_a(),
        test_enum_b(),
    ]


def get_test_package():
    """Returns a test ontology package definition.

	"""
    return {
        'name': 'test_package',
        'doc': 'bar package documentation',
        'classes': get_test_classes(),
        'enums': get_test_enums()
    }


def get_test_schema():
    """Returns a test ontology schema definition.

	"""
    return {
        'name': 'test_ontology',
        'version': '1.0',
        'is_latest': True,
        'doc': 'Test ontology schema - version 1.0 - documentation',
        'packages': [
            get_test_package()
        ]
    }


# Generate code.
esdoc_mp.generate(get_test_schema(), _LANGUAGE, sys.argv[1])
