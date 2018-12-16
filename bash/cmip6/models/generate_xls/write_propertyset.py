def write(spreadsheet):
    """Write property set worksheet rows.

    """
    # Set formats.
    f0 = spreadsheet.create_format(18)
    f0.set_bg_color('#003366')
    f0.set_bold()
    f0.set_font_color('#FFFFFF')

    f1 = spreadsheet.create_format(14)
    f1.set_bold()
    f1.set_italic()

    # Write header.
    if len(spreadsheet.ps.id.split('.')) == 3:
        spreadsheet.ws_row += 0
    else:
        spreadsheet.ws_row += 3
    spreadsheet.ws.set_row(spreadsheet.ws_row, 24)
    spreadsheet.ws.write(spreadsheet.ws_row, 0, spreadsheet.ps.idx, f0)
    spreadsheet.ws.write(spreadsheet.ws_row, 1, _get_property_set_label(spreadsheet.ps), f0)

    # Write description.
    spreadsheet.ws_row += 1
    spreadsheet.ws.set_row(spreadsheet.ws_row, 24)
    spreadsheet.ws.write(spreadsheet.ws_row, 1, spreadsheet.ps.description, f1)


def _get_property_set_label(ps):
    """Returns label associated with a property set.

    """
    names = ps.names().split(' --> ')
    if len(names) == 3:
        return names[-1]
    elif len(names) == 4:
        return ps.names(2)
    else:
        return ps.names(2)
