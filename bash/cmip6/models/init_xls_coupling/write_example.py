import pyessv


def write(ctx):
    """Write couplings worksheet.

    """
    # Formats.
    f0 = ctx.create_format(16)
    f0.set_align('left')

    f1 = ctx.create_format(16)
    f1.set_bold()
    f1.set_bg_color('#337ab7')
    f1.set_font_color('#FFFFFF')

    f2 = ctx.create_format()
    f2.set_bold()

    f6 = ctx.create_format(14)
    f6.set_align('left')
    f6.set_text_wrap()
    f6.set_align('top')

    # Write worksheet.
    ws = ctx.wb.add_worksheet('Example')

    # ... columns
    ws.set_column('A:A', 35, f0)
    ws.set_column('B:B', 28, f0)
    ws.set_column('C:C', 28, f0)
    ws.set_column('D:D', 40, f0)
    ws.set_column('E:E', 70, f0)

    # ... headers
    ws_row = 0
    ws.write(ws_row, 0, 'Variable *', f1)
    ws.write(ws_row, 1, 'Source Realm *', f1)
    ws.write(ws_row, 2, 'Target Realm *', f1)
    ws.write(ws_row, 3, 'Time Frequency (in seconds) *', f1)
    ws.write(ws_row, 4, 'Coupling Details *', f1)

    # ... example 1
    ws_row += 1
    ws.write(ws_row, 0, 'sea_surface_temperature', f6)
    ws.write(ws_row, 1, 'Ocean', f6)
    ws.write(ws_row, 2, 'Atmosphere', f6)
    ws.write(ws_row, 3, '10800', f6)
    ws.write(ws_row, 4, 'The area-weighted average of ocean grid cell within each atmosphere grid cell is used', f6)

    # ... drop-downs
    ws.data_validation(ws_row, 1, ws_row, 1, {
        'validate': 'list',
        'source': [r.description for r in ctx.realms]
    })
    ws.data_validation(ws_row, 2, ws_row, 2, {
        'validate': 'list',
        'source': [r.description for r in ctx.realms]
    })

    # ... example 2
    ws_row += 1
    ws.write(ws_row, 0, 'uas', f6)
    ws.write(ws_row, 1, 'Atmosphere', f6)
    ws.write(ws_row, 2, 'Ocean', f6)
    ws.write(ws_row, 3, '3600', f6)
    ws.write(ws_row, 4, 'OASIS coupling using vector transformation on rotated grid and using ocean grid points only', f6)

    # ... drop-downs
    ws.data_validation(ws_row, 1, ws_row, 1, {
        'validate': 'list',
        'source': [r.description for r in ctx.realms]
    })
    ws.data_validation(ws_row, 2, ws_row, 2, {
        'validate': 'list',
        'source': [r.description for r in ctx.realms]
    })
