def write(spreadsheet):
    """Write property worksheet rows.

    """
    # Set formats.
    f0 = spreadsheet.create_format(14)
    f0.set_bg_color('#337ab7')
    f0.set_bold()
    f0.set_font_color('#FFFFFF')

    f1 = spreadsheet.create_format(11)

    f2 = spreadsheet.create_format()
    f2.set_bold()

    f3 = spreadsheet.create_format(10)
    f3.set_align('left')
    f3.set_italic()

    # Write header.
    spreadsheet.ws_row += 2
    spreadsheet.ws.set_row(spreadsheet.ws_row, 24)
    spreadsheet.ws.write(spreadsheet.ws_row, 0, '{} {}'.format(spreadsheet.p.idx, '*' if spreadsheet.p.is_required else ''), f0)
    spreadsheet.ws.write(spreadsheet.ws_row, 1, spreadsheet.p.name_camel_case_spaced, f0)

    # Write details.
    spreadsheet.ws_row += 1
    spreadsheet.ws.set_row(spreadsheet.ws_row, 24)
    spreadsheet.ws.write(spreadsheet.ws_row, 0, spreadsheet.p.typeof_label, f1)
    spreadsheet.ws.write(spreadsheet.ws_row, 1, spreadsheet.p.description, f2)
    spreadsheet.ws.write(spreadsheet.ws_row, 2, spreadsheet.p.id, f2)

    # Write note: comma separated strings.
    if spreadsheet.p.typeof == 'cs-str':
        spreadsheet.ws_row += 1
        spreadsheet.ws.set_row(spreadsheet.ws_row, 24)
        spreadsheet.ws.write(spreadsheet.ws_row, 1, 'NOTE: Please enter a comma seperated list', f3)

    # Write note: long strings.
    if spreadsheet.p.typeof == 'l-str':
        spreadsheet.ws_row += 1
        spreadsheet.ws.set_row(spreadsheet.ws_row, 24)
        spreadsheet.ws.write(spreadsheet.ws_row, 1, 'NOTE: Double click to expand if text is too long for cell', f3)

    # Write note: X.N cardinality.
    if spreadsheet.p.is_collection:
        spreadsheet.ws_row += 1
        spreadsheet.ws.set_row(spreadsheet.ws_row, 24)
        spreadsheet.ws.write(spreadsheet.ws_row, 1, 'NOTE: Multiple entries are allowed.  To enter a new row, copy & paste an existing row, and edit accordingly.', f2)
