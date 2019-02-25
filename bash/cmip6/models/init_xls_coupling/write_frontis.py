def write(ctx):
    """Write frontis worksheet.

    """
    # Write worksheet.
    ws = ctx.wb.add_worksheet('Frontis')

    # Set columns.
    f0 = ctx.create_format()
    f0.set_bg_color('#337ab7')
    f0.set_font_color('#FFFFFF')
    ws.set_column('A:A', 35, f0)
    ws.set_column('B:B', 180, f0)
    ws.set_column('C:XFD', None, f0)

    # Set formats.
    f0 = ctx.create_format(26)
    f0.set_bold()
    f0.set_bg_color('#337ab7')
    f0.set_font_color('#FFFFFF')

    f1 = ctx.create_format(16)
    f1.set_bold()
    f1.set_bg_color('#337ab7')
    f1.set_font_color('#FFFFFF')

    f2 = ctx.create_format(16)
    f2.set_bg_color('#337ab7')
    f2.set_font_color('#FFFFFF')

    f3 = ctx.create_format(11)
    f3.set_bg_color('#337ab7')
    f3.set_font_color('#FFFFFF')
    f3.set_italic()

    f4 = ctx.create_format(14)
    f4.set_align('left')
    f4.set_bg_color('#CCCCCC')
    f4.set_font_color('#000000')

    f5 = ctx.create_format(14)
    f5.set_bg_color('#337ab7')
    f5.set_font_color('#FFFFFF')

    ws_row = 0
    ws.write(ws_row, 0, 'ES-DOC CMIP6 Model Coupling Documentation', f0)

    ws_row += 2
    ws.write(ws_row, 0, 'MIP Era', f1)
    ws.write(ws_row, 1, ctx.MIP_ERA.upper(), f2)

    ws_row += 1
    ws.write(ws_row, 0, 'Institute', f1)
    ws.write(ws_row, 1, ctx.institution_id.upper(), f2)

    ws_row += 1
    ws.write(ws_row, 0, 'Model', f1)
    ws.write(ws_row, 1, ctx.source_id.upper(), f2)

    ws_row += 2
    ws.write(ws_row, 0, 'How To Use', f5)
    ws.write(ws_row, 1, 'https://es-doc.org/how-to-use-coupling-spreadsheets/', f5)

    ws_row += 1
    ws.write(ws_row, 0, 'Further Info', f5)
    ws.write(ws_row, 1, 'https://es-doc.org/{}'.format(ctx.MIP_ERA.lower()), f5)

    ws_row += 1
    ws.write(ws_row, 0, 'Spreadsheet Generator Version', f5)
    ws.write(ws_row, 1, ctx.VERSION, f5)

    ws_row += 2
    ws.write(ws_row, 0, 'Initialised By', f1)
    ws.write(ws_row, 1, '', f2)

    ws_row += 1
    ws.write(ws_row, 0, 'Internal notes', f1)
    ws.write(ws_row, 1, '', f2)
