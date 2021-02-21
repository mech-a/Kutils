# -*- coding: utf-8 -*-
"""
Created on Tue Jan 19 21:28:36 2021

youtube link checker bot pre-alpha satge

https://www.youtube.com/watch?v=EPZP8SqbPSI some random deleted video

@author: mecha#7999
v: 0.0.4:mbf

TODO: playlist handling, double hyperlink cells, better text cleaning (keyword list is bad), handle time_continue flag (currently makes id == '')
"""
import requests
from pprint import pprint
from sheetfunctions import extract_url_from_hyperlinks, fetch_cell_hyperlinks
from googleapiclient.discovery import build
from google.oauth2 import service_account
# https://python-forum.io/Thread-How-to-check-if-video-has-been-deleted-or-removed-in-youtube-using-python

delete_keywords = ['&feature', '&list', '&index', '&lc', '&ab_channel', '&t']

def extract_youtube_ids_from_urls(urls):
    ids = []
    count_non_yt_vid = 0
    for url in urls:
        if not is_youtube_video_url(url):
            count_non_yt_vid += 1
            continue

        for kw in delete_keywords:
            if kw in url:
                url = url[:url.find(kw)]
        # if '&feature' in url:
        #     url = url[:url.find('&feature')]
        # if '&feature' in url:
        #     url = url[:url.find('&feature')]

        if is_link_shortened(url) and url.rfind('?') > 0:
            id = url[url.rfind('/')+1:url.rfind('?')]
        elif is_link_shortened(url):
            id = url[url.rfind('/') + 1:]
        # TODO special chars not in id list
        elif '&' in url:
            id = url[url.rfind('=')+1:url.find('&')]
        elif ']' in url:
            id = url[url.rfind('=') + 1:url.find(']')]
        else:
            id = url[url.rfind('=')+1:]

        ids.append(id)
    return ids, count_non_yt_vid


def is_youtube_video_url(url):
    # wow aint this one line of code. do better clean url
    return ('playlist' not in url) and ('youtube.com' in url or 'youtu.be' in url) and ('results' not in url)


def is_link_shortened(yt_url):
    # not necessarily the best b/c of double youtube phenomenon (youtube.com...&feature=youtu.be
    return 'youtu.be' in yt_url


def find_url_idx_by_str(str):
    # testing function for finding errors
    for i in range(len(urls)):
        if str in urls[i]:
            return i

sheet_id = '1FKsk1QwLYHNqeW9l0Y9jFCacWe6KkPj9QMgcKt4ZaTQ'
sheet_ranges = ['Discography!F:F', 'Solo/Subunit Discography!E:E',
                'Music Shows!C:K', 'Live Performances!D:K', 'Solo/Subunit Live Performances!C:C',
                'Solo/Subunit Live Performances!F:F', 'Livestreams!D:D', 'Variety!D:D', 'Variety!D:H',
                'Radio Shows!D:D', 'Radio Shows!H:H', 'Misc!C:C', 'Misc!E:E'
                ]

g_scopes = ['https://www.googleapis.com/auth/youtube.readonly', "https://www.googleapis.com/auth/spreadsheets.readonly"]
g_credentials = service_account.Credentials.from_service_account_file("rvcord_credentials.json", scopes=g_scopes)
youtube = build('youtube', "v3", credentials=g_credentials)
sheets = build('sheets', "v4", credentials=g_credentials)
cell_hyperlinks = fetch_cell_hyperlinks(sheets, sheet_id, sheet_ranges)
urls = extract_url_from_hyperlinks(cell_hyperlinks)
yt_ids, count_non_yt = extract_youtube_ids_from_urls(urls)

num_dead = 0

for an_id in yt_ids:
    request = youtube.videos().list(part="status,contentDetails", id=an_id)
    response = request.execute()
    items = response['items']
    if not len(items) and an_id:
        num_dead += 1
        print(an_id, "is dead")

print("FINISHED\n", num_dead, "links dead in total")
