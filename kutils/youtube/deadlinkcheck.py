# -*- coding: utf-8 -*-
"""
Created on Tue Jan 19 21:28:36 2021

youtube link checker bot pre-alpha satge

https://www.youtube.com/watch?v=EPZP8SqbPSI some random deleted video

referenced https://python-forum.io/Thread-How-to-check-if-video-has-been-deleted-or-removed-in-youtube-using-python

@author: mecha#7999
v: 0.0.4:mbf

TODO: playlist handling, double hyperlink cells, better text cleaning (keyword list is bad),
 handle time_continue flag (currently makes id == '')
"""
import googleapiclient
import os
from kutils.sheets.sheetfunctions import get_cells, fetch_cell_hyperlinks
from googleapiclient.discovery import build
from google.oauth2 import service_account
from tqdm import tqdm
from filtering import extract_youtube_ids_from_urls
from pathlib import Path

sheet_id = '1FKsk1QwLYHNqeW9l0Y9jFCacWe6KkPj9QMgcKt4ZaTQ'

# TODO give individual columns
# sheet_ranges = ['Discography!F:F', 'Solo/Subunit Discography!E:E',
#                 'Music Shows!C:K', 'Live Performances!D:K', 'Solo/Subunit Live Performances!C:C',
#                 'Solo/Subunit Live Performances!F:F', 'Livestreams!D:D', 'Variety!D:D', 'Variety!D:H',
#                 'Radio Shows!D:D', 'Radio Shows!H:H', 'Misc!C:C', 'Misc!E:E'
#                 ]

sheet_ranges = ['Live Performances!D10:D18']


credentials_file = Path(os.environ['KUTILSPVT']) / 'tester-google-credentials.json'

if not credentials_file.is_file():
    print('tester-google-credentials.json is not a file')
    raise IOError

# initialize service objects
g_scopes = ['https://www.googleapis.com/auth/youtube.readonly', "https://www.googleapis.com/auth/spreadsheets.readonly"]
g_credentials = service_account.Credentials.from_service_account_file(credentials_file, scopes=g_scopes)
youtube = build('youtube', "v3", credentials=g_credentials)
sheets = build('sheets', "v4", credentials=g_credentials)

# construct relevant cells
cell_hyperlinks = fetch_cell_hyperlinks(sheets, sheet_id, sheet_ranges)
cells = get_cells(cell_hyperlinks)

# easter egg! just like the game
dead_cells = []

# add a progress bar
for c in tqdm(cells, desc='Progress on Cells'):
    urls = [c.get_url()]
    ids, _ = extract_youtube_ids_from_urls(urls)
    for an_id in ids:
        request = youtube.videos().list(part="status,contentDetails", id=an_id)
        try:
            response = request.execute()
        except googleapiclient.errors.HttpError:
            print(c, c.get_url())
            continue
        items = response['items']
        if not len(items) and an_id:
            dead_cells.append(c)

for dc in dead_cells:
    print(dc, "contains a dead link")

print("FINISHED\n", len(dead_cells), "links dead in total")
