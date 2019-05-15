import collections


def write(spreadsheet):
    """Writes a worksheet row per property value.

    """
    if spreadsheet.p.typeof == 'bool':
        write_property_value_bool(spreadsheet)

    elif spreadsheet.p.typeof == 'float':
        write_property_value_float(spreadsheet)

    elif spreadsheet.p.typeof == 'int':
        write_property_value_int(spreadsheet)

    elif spreadsheet.p.typeof in {'str', 'cs-str', 'l-str'}:
        write_property_value_str(spreadsheet)

    elif spreadsheet.p.enum:
        write_property_value_enum(spreadsheet)


def write_property_value_bool(spreadsheet):
    """Writes a property boolean value.

    """
    for val in spreadsheet.p_values or ['']:
        write_property_values(spreadsheet, val, {
            'validate': 'list',
            'source': ['TRUE', 'FALSE']
            })


def write_property_value_enum(spreadsheet):
    """Writes a property enum value.

    """
    # Enum choices need to include their description where appropriate.
    def get_choice_text(c):
        return c.value if c.description is None else \
               "{}: {}".format(c.value, c.description)

    # Create map choice value <--> choice text.
    # TODO - move to domain model
    choice_map = collections.OrderedDict()
    for c in spreadsheet.p.enum.choices:
        choice_map[c.value] = get_choice_text(c)
    if spreadsheet.p.enum.is_open:
        choice_map['OTHER'] = 'Other: document in cell to the right'

    # Set values to be injected into spreadsheet.
    p_values = [_str(i) for i in spreadsheet.p_values] or ['']
    spreadsheet.p_values = [choice_map[i] if i in choice_map else i for i in p_values]

    # Inject values into spreadsheet.
    for val in spreadsheet.p_values:
        write_property_values(spreadsheet, val, {
            'validate': 'list'
            }, choices=choice_map.values())


def write_property_value_float(spreadsheet):
    """Writes a property float value.

    """
    for val in spreadsheet.p_values or ['']:
        write_property_values(spreadsheet, val, {
            'validate': 'decimal',
            'criteria': 'between',
            'maximum': 1000000.0,
            'minimum': -1000000.0
            })


def write_property_value_int(spreadsheet):
    """Writes a property int value.

    """
    for val in spreadsheet.p_values or ['']:
        write_property_values(spreadsheet, val, {
            'validate': 'integer',
            'criteria': '>=',
            'value': 0
            })


def write_property_value_str(spreadsheet):
    """Writes a property str value.

    """
    for val in spreadsheet.p_values or ['']:
        write_property_values(spreadsheet, val, {
            'validate': 'any',
            })


def write_property_values(spreadsheet, val, validation_opts, choices=[]):
    """Writes property values to active worksheet.

    """
    f0 = spreadsheet.create_format(14)
    f0.set_align('left')
    f0.set_bg_color('#CCCCCC')
    f0.set_font_color('#000000')
    f0.set_text_wrap()
    f0.set_align('top')

    spreadsheet.ws_row += 1
    spreadsheet.ws.set_row(spreadsheet.ws_row, 178 if spreadsheet.p.typeof == 'l-str' else 24)
    spreadsheet.ws.write(spreadsheet.ws_row, 1, val, f0)

    if choices:
        for idx, choice in enumerate(choices):
            spreadsheet.ws.write(spreadsheet.ws_row, idx + 26, choice)
        enum_source = 'AA{0}:A{1}{0}'.format(spreadsheet.ws_row + 1, chr(64 + len(choices)))
        validation_opts['source'] = enum_source

    spreadsheet.ws.data_validation(spreadsheet.ws_row, 1, spreadsheet.ws_row, 1, validation_opts)


def _str(val):
    """Formats a string value.

    """
    if val is None:
        return ''

    try:
        val = str(val).strip()
    except UnicodeEncodeError:
        pass

    if len(val):
        return val[0].upper() + val[1:]

    return ''
