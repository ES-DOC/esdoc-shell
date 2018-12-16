def write(spreadsheet):
    """Write parties & citations worksheet.

    """
    # Set formats.
    f0 = spreadsheet.create_format()
    f0.set_bg_color('#FFFFFF')

    f1 = spreadsheet.create_format(24)
    f1.set_bg_color('#003366')
    f1.set_bold()
    f1.set_font_color('#FFFFFF')

    f2 = spreadsheet.create_format(14)
    f2.set_bg_color('#337ab7')
    f2.set_bold()
    f2.set_font_color('#FFFFFF')

    f3 = spreadsheet.create_format(11)

    f4 = spreadsheet.create_format()
    f4.set_bold()

    f5 = spreadsheet.create_format(10)
    f5.set_align('left')
    f5.set_italic()

    f6 = spreadsheet.create_format(14)
    f6.set_align('left')
    f6.set_bg_color('#CCCCCC')
    f6.set_font_color('#000000')
    f6.set_text_wrap()
    f6.set_align('top')

    # Write worksheet.
    ws_title = 'Parties & Citations'
    ws = spreadsheet.wb.add_worksheet(ws_title)

    # set column dimensions.
    ws.set_column(0, 0, 80)
    ws.set_column(1, 1, 40)
    ws.set_column('C:XFD', None, f0)

    # Write title.
    ws_row = 0
    ws.write(ws_row, 0, 'Parties & Citations', f1)
    ws.write(ws_row, 1, '', f1)

    # Write help.
    ws_row += 2
    ws.write(ws_row, 0, 'NOTE: Multiple entries are allowed.  To enter a new row, copy & paste an existing row, and edit accordingly.', f5)

    # Write responsible parties.
    # ... title
    ws_row += 2
    ws.write(ws_row, 0, 'Responsible Parties', f2)
    ws.write(ws_row, 1, '', f2)
    # ... help
    ws_row += 1
    ws.write(ws_row, 0, 'https://es-doc.org/how-to-use-model-responsible-party-spreadsheets.', f5)
    ws_row += 1
    ws.write(ws_row, 0, 'Enter responsible party identifiers below, one identifier per line.  You can optionally specify a role.', f5)
    # ... headers
    ws_row += 1
    ws.write(ws_row, 0, 'Identifier', f4)
    ws.write(ws_row, 1, 'Role', f4)
    # ... input value
    ws_row += 1
    ws.write(ws_row, 0, '', f6)
    ws.write(ws_row, 1, '', f6)
    ws.data_validation(ws_row, 1, ws_row, 1, {
        'validate': 'list',
        'source': [
            'Author',
            'Contributor',
            'Principal Investigator',
            'Point of Contact',
            'Sponsor'
        ]
    })

    # Write citations.
    ws_row += 3
    # ... title
    ws.write(ws_row, 0, 'Citations', f2)
    ws.write(ws_row, 1, '', f2)
    # ... help
    ws_row += 1
    ws.write(ws_row, 0, 'https://es-doc.org/how-to-use-model-citation-spreadsheets.', f5)
    ws_row += 2
    ws.write(ws_row, 0, 'Enter citation identifiers below, one identifier per line.  You can optionally specify a process.', f5)
    # ... headers
    ws_row += 1
    ws.write(ws_row, 0, 'Identifier', f4)
    ws.write(ws_row, 1, 'Process', f4)
    # ... input value
    ws_row += 1
    ws.write(ws_row, 0, '', f6)
    ws.write(ws_row, 1, '', f6)
    ws.data_validation(ws_row, 1, ws_row, 1, {
        'validate': 'list',
        'source': ['Top Level'] + [i.names(2) for i in spreadsheet.t.sub_topics]
    })
