from googleapiclient.discovery import build
from google.oauth2 import service_account
import kutils.sheets.sheetfunctions as shf
from urllib.parse import urlparse

sh_id = "1FKsk1QwLYHNqeW9l0Y9jFCacWe6KkPj9QMgcKt4ZaTQ"
#ranges = ["Music Shows!E:E", 'Music Shows!F7:F30', "Discography!F:F"]
ranges = ['Radio Shows!D:D', 'Radio Shows!H:H', 'Misc!C:C', 'Misc!E:E']
# ranges must be individual columns

g_scopes = ['https://www.googleapis.com/auth/youtube.readonly', "https://www.googleapis.com/auth/spreadsheets.readonly"]
g_credentials = service_account.Credentials.from_service_account_file("creds.json", scopes=g_scopes)
sheets = build('sheets', "v4", credentials=g_credentials)

result = shf.fetch_cell_hyperlinks(sheets, sh_id, ranges)

cells = shf.get_cells(result)
