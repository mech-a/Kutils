import os
from pathlib import Path
from googleapiclient.discovery import build
from google.oauth2 import service_account
# internal project imports

def fetch_cell_hyperlinks(service, spreadsheet_id, ranges):
    # TODO cite stackoverflow
    result = service.spreadsheets().values().batchGet(
        spreadsheetId=spreadsheet_id,
        ranges=ranges#,
        # fields="sheets/data/rowData/values/hyperlink"
        # includeGridData=True
    ).execute()
    return result
# TODO potential solution; batchGet row data as one request and match row idx to url idx, but doesn't solve for cols with only a few hyperlinks
# TODO honestly best sol might just be to go row by row, mark if it contains data we need, query for that data specifically


sheet_id = '18UdgCmsV2AISuM47wVJ1-w2jRrjWlFP_xiKc2EcBUV4'
sheet_ranges = ['Irene!C:C', 'Seulgi!C:C', 'Wendy!C:C', 'Joy!C:C', 'Yeri!C:C', 'Group / Multi!C:C']

credentials_file = Path(os.environ['KUTILSPVT']) / 'tester-google-credentials.json'

if not credentials_file.is_file():
    print('tester-google-credentials.json is not a file')
    raise IOError

g_scopes = ["https://www.googleapis.com/auth/spreadsheets.readonly"]
g_credentials = service_account.Credentials.from_service_account_file(credentials_file, scopes=g_scopes)
sheets_svc = build('sheets', 'v4', credentials=g_credentials)
result = fetch_cell_hyperlinks(sheets_svc, sheet_id, sheet_ranges[0])


