def write(spreadsheet):
    """Write sub-topic worksheet.

    """
    # Set formats.
    f0 = spreadsheet.create_format()
    f0.set_bg_color('#FFFFFF')

    # Write worksheet.
    ws_title = '{}. {}'.format(spreadsheet.st.idx.split('.')[0], spreadsheet.st.names(2))[0:31]
    spreadsheet.ws = spreadsheet.wb.add_worksheet(ws_title)
    spreadsheet.ws_row = 0

    # Write columns.
    spreadsheet.ws.set_column(0, 0, 13)
    spreadsheet.ws.set_column(1, 1, 150)
    spreadsheet.ws.set_column('C:C', None, None, {
        'hidden': 1,
        })
    spreadsheet.ws.set_column('D:XFD', None, f0)
