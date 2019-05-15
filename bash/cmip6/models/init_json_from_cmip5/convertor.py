# -*- coding: utf-8 -*-

"""
.. module:: convertor.py
   :license: GPL/CeCIL
   :platform: Unix, Windows
   :synopsis: Property value conversion utility functions.

.. moduleauthor:: Mark Conway-Greenslade <momipsl@ipsl.jussieu.fr>

"""
import mappings



def convert_property_values(values, spec):
    """Converts a collection of CMIP5 property values.

    """
    # Convert values.
    vals = []
    for val in values:
        vals += _convert_property_value(spec, val)
    values = sorted([i for i in vals if i is not None])

    # Collapse values.
    if spec.is_collection == False and len(values) > 1:
        values = [', '.join([str(i) for i in values])]

    return values


def _convert_property_value(spec, val):
    """Converts a CMIP5 property value.

    """
    # Set convertor.
    if spec.enum:
        func = _convert_enum
    else:
        func = _CONVERTORS.get(spec.typeof, _noop)

    # Convert.
    converted = func(spec, val) or val
    if not isinstance(converted, list):
        converted = [converted]

    # Validate.
    validated = [_validate_property_value(spec, i) for i in converted]

    return [i for i in validated if val is not None]


def _validate_property_value(spec, val):
    """Validates property value by applying specialization rules.

    """
    try:
        spec.validate_value(val)
    except ValueError as err:
        return
        print 'Invalid CMIP5 Property Value:'
        print '\tSpec. Info:\t', spec.typeof, spec.cardinality
        print '\tSpec. ID:\t', spec.id
        if spec.enum:
            print '\tSpec. Choices:\t', ', '.join([i.value for i in spec.enum.choices])
        print '\tInvalid Value:\t', val
    else:
        return val


def _noop(spec, val):
    """Conversion no-op for scenarios when conversion is unnecessary.

    """
    return val


def _convert_bool(spec, val):
    """Returns a value converted to a boolean.

    """
    try:
        return bool(val)
    except ValueError:
        if str(val).strip().lower() in {'yes', 'true', 'y', 't', 'ok'}:
            return True
        elif str(val).strip().lower() in {'no', 'false', 'n', 'f'}:
            return False

    return val


def _convert_enum(spec, val):
    """Returns a value converted to an enum.

    """
    val = str(val).strip().lower()
    try:
        val = mappings.ENUM_CHOICE_MAPPINGS[val]
    except KeyError:
        pass

    if isinstance(val, list):
        return [_convert_enum_choice(spec, i) for i in val]
    else:
        return _convert_enum_choice(spec, val)


def _convert_enum_choice(spec, val):
    """Returns a value converted to an enum choice.

    """
    val = str(val).strip().lower()
    choices = {i.value.lower(): i.value for i in spec.enum.choices}
    try:
        return choices[val]
    except KeyError:
        try:
            return choices[val.split(' ')[0]]
        except KeyError:
            if spec.enum.is_open:
                return 'Other: {}'.format(val)
            else:
                print 'enum mapping failure: {} -> {}'.format(spec.id, val)



def _convert_float(spec, val):
    """Returns a value converted to a float.

    """
    try:
        return float(val)
    except ValueError:
        for val in str(val).strip().split(' '):
            try:
                return float(val)
            except ValueError:
                pass


def _convert_int(spec, val):
    """Returns a value converted to an int.

    """
    try:
        return int(val)
    except ValueError:
        pass

    for i in str(val).strip().split(' '):
        try:
            return int(i)
        except ValueError:
            try:
                return int(float(i))
            except ValueError:
                pass

    i = ''
    for s in str(val).strip().split(' ')[0]:
        if s not in '01234567890':
            break
        i += s
    try:
        return int(i)
    except ValueError:
        pass


def _convert_str(spec, val):
    """Returns a value converted to a string.

    """
    try:
        val = str(val)
    except UnicodeEncodeError:
        pass

    return val.strip()


# Map of property value types to conversion functions.
_CONVERTORS = {
    'bool': _convert_bool,
    'enum': _convert_enum,
    'float': _convert_float,
    'int': _convert_int,
    'str':_convert_str
}
