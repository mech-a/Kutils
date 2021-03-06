from kutils.utils import get_column_alphabetical_index_from_zero_indexed_num


class Cell:
    sheet = None
    row_idx = 0
    col_idx = ''
    data = None

    def __init__(self, a_sheet, a_row_idx, a_col_idx, a_data):
        self.sheet = a_sheet
        self.row_idx = a_row_idx
        self.col_idx = a_col_idx
        self.data = a_data

    def get_url(self):
        return self.data['values'][0]['hyperlink']

    def get_cell_url_relation(self, url_data_extractor):
        return self, url_data_extractor(self.get_url())

    def __str__(self):
        return self.sheet + ' ' + self.col_idx + str(self.row_idx)


def fetch_cell_hyperlinks(service, spreadsheet_id, ranges):
    fields = "sheets/properties/title,sheets/data/rowData/values/hyperlink,sheets/data/startRow,sheets/data/startColumn"
    return get_resource(service, spreadsheet_id, ranges, fields)


def get_resource(service, spreadsheet_id: str, ranges: list, fields: str):
    result = service.spreadsheets().get(
        spreadsheetId=spreadsheet_id,
        ranges=ranges,
        fields=fields
    ).execute()
    return result


def get_cells(result) -> list:
    """
    Extract cells from Sheet response of Google Sheets API V4
    """
    cells = []
    for sheet in result['sheets']:
        sheet_name = sheet['properties']['title']
        for a_range in sheet['data']:
            col_alpha = get_column_alphabetical_index_from_zero_indexed_num(a_range['startColumn'])
            # TODO check if rows are indexed by 1
            row_idx = a_range['startRow'] + 1 if 'startRow' in a_range else 1
            row_data = a_range['rowData']
            for i in range(len(row_data)):
                cell_data = row_data[i]
                if cell_data:
                    c = Cell(sheet_name, row_idx + i, col_alpha, cell_data)
                    cells.append(c)
    return cells



# def get_sheet_name_from_range(rangestr: str) -> str:
#     return rangestr[:rangestr.find('!')]
#
#
# def get_twitter_usernames_from_sheet(spreadsheet_id, ranges, key=google_key):
#     """Deprecated"""
#     service = build('sheets', 'v4', developerKey=key)
#     hyperlinks = fetch_cell_hyperlinks(service, spreadsheet_id, ranges)
#     urls = extract_url_from_hyperlinks(hyperlinks)
#     usernames = []
#     for url in urls:
#         # TODO see if twitter api can handle username from url
#         # TODO understand why this didn't work in a function
#         # from last occurence of slash
#         raw_username = url[url.rfind('/') + 1:]
#         # remove queries
#         if '?' in raw_username:
#             username = raw_username[:raw_username.find('?')]
#             usernames.append(username)
#         else:
#             usernames.append(raw_username)
#     return usernames
#
#
# def extract_url_from_hyperlinks(hyperlinks) -> list:
#     """Deprecated"""
#     urls = []
#     # TODO switch to while loop and return dictionary such that we can track urls to their sheet position
#     #  (or, perhaps use nested lists)
#     for sheet in hyperlinks['sheets']:
#         for e in sheet['data'][0]['rowData']:
#             # filters for {}, represents any non-hyperlinked line
#             # checks if we can access hyperlink
#             if e and 'hyperlink' in e['values'][0]:
#                 urls.append(e['values'][0]['hyperlink'])
#     return urls
