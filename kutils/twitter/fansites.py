# -*- coding: utf-8 -*-
"""
Created on Mon Jan 18 19:52:42 2021

TWITTER FANSITE INACTIVITY CHECKER [fansites.py]
Compatability: Python 3.4+, Windows
Dependencies: python-twitter (pip install python-twitter), Google API (pip install --upgrade google-api-python-client google-auth-httplib2 google-auth-oauthlib)

# TODO use different prompt (currently python prompt lol) use bash or smth

EX USAGE
  > py fansites.py
    Read 'fansites.txt', a new line-delimited text file containing all Twitter IDs (@___) in same 
    directory (the current working directory) as this script and print out 
    fansites that have been inactive (as determined by last tweet) for 6 
    standard months.
    
Detailed usage
  > py fansites.py -f [filepath with forward slashes] -mo [inactivity cutoff in number of months]"
    Examples     
      > py fansites.py -f 'c:/users/mecha/desktop/i love red velvet/fansites.txt' -mo 12
        Use single-quotes when surrounding a filepath (absolute or relative) 
        that has spaces in it.
      > py fansites.py -f /resources/redvelvetfansites.txt
        Access the folder 'resources' within the current working directory and 
        output 6 standard month inactive fansites
  > py fansites.py -ss
    Return inactive fansites dependent on the public Google Spreadsheet (or shared with your service account) and ranges
    that are put into this script.
    
Wherever you see fansites.txt or 6 standard months, you can change the default 
values in the user constants below.

NOTE: NOT OS-AGNOSTIC (FILE HANDLING). NO IN-BUILT ERROR HANDLING. IGNORE TODO COMMENTS.

KNOWN BUGS: NONE ATM

PLANNED FEATURES: Better spreadsheet handling (print out sheet and cell location), modularity across the board (sheetfunctions should be a class that can extract any url)
@author: mecha#7999 on Discord
@version: 0.0.4:mbf
~~ Made with love for RVCord, https://discord.gg/redvelvet ~~
"""
from urllib.parse import urlparse

import twitter
import time
import sys
import os
from pathlib import Path
from googleapiclient.discovery import build
from google.oauth2 import service_account
from kutils.sheets.sheetfunctions import fetch_cell_hyperlinks, get_cells, Cell
from tqdm import tqdm

# --- USER CONSTANTS ----------------------------------------------------------

# FILL THESE IN WITH YOUR OWN TWITTER KEYS/SECRETS
# TODO serialize this using pickle
from kutils.utils import get_default_credentials, get_twitter_credentials

# api_key = ""
# api_secret = ""
# access_tkn_key = ""
# access_tkn_secret = ""

twt_creds = get_twitter_credentials()

api_key = twt_creds['api_key']
api_secret = twt_creds['api_secret']
access_tkn_key = twt_creds['access_tkn_key']
access_tkn_secret = twt_creds['access_tkn_secret']

# change this number to change the default number of standard months of inactivity needed to deem account inactive;
# this is used when no month argument is passed in
default_number_months_cutoff = 6
# default file with all twitter @s to check
default_file_name = "fansites.txt"
# character used in fansites to ignore the line
fansites_comment_character = '#'

# default google sheet ID to read from
# RV Fansite sheet
sheet_id = '18UdgCmsV2AISuM47wVJ1-w2jRrjWlFP_xiKc2EcBUV4'
# default ranges on Google Sheet ID to read from (see *INSERT GOOGLE SHEETS API V4 LINK*)
# sheet_ranges = ['{NAME OF SHEET}!{RANGE OF CELLS}' ...]
# sheet_ranges = ['Irene!C:C', ...]
sheet_ranges = ['Irene!C:C', 'Seulgi!C:C', 'Wendy!C:C', 'Joy!C:C', 'Yeri!C:C', 'Group / Multi!C:C']

# TODO implement developer bypass or make new git branch
debug = False

# --- CODE --------------------------------------------------------------------

curr_time = time.time()
api = twitter.Api(consumer_key=api_key,
                  consumer_secret=api_secret,
                  access_token_key=access_tkn_key,
                  access_token_secret=access_tkn_secret)

g_scopes = ["https://www.googleapis.com/auth/spreadsheets.readonly"]
#g_credentials = service_account.Credentials.from_service_account_file("rvcord_credentials.json", scopes=g_scopes)
g_credentials = get_default_credentials()
sheets = build('sheets', "v4", credentials=g_credentials)

# developer override here
using_spreadsheet = False


def get_twitter_id_to_cells(service, sheet_id: str, sheet_ranges: list) -> dict:
    def get_twitter_id_from_url(url: str) -> str:
        url_path = urlparse(url)[2]
        raw_username = url_path[1:]
        if '/' in raw_username:
            un = raw_username[:raw_username.find('/')]
        else:
            un = raw_username
        return un

    result = fetch_cell_hyperlinks(sheets, sheet_id, sheet_ranges)
    cells = get_cells(result)
    twitter_to_cell = {}
    for c in cells:
        twt_id = get_twitter_id_from_url(c.get_url())
        twitter_to_cell[twt_id] = c
    return twitter_to_cell


def handle_file_path(arg):
    # TODO implement os-agnostic project root file handling, see https://stackoverflow.com/questions/25389095/python-get-path-of-root-project-structure
    # "'c:/expecting spaces/'" -> "c:/expecting spaces/"
    # py fansites.py 'c:/users/ My Documents'
    if arg[0] == "'" and arg[-1] == "'":
        arg = arg[1:-1]
    # relative path
    # see pep 8 e713 for not in
    if ':' not in arg:
        return open(arg, 'r')
    # absolute path
    abs_path = Path(arg)
    return open(abs_path, 'r')


def handle_time(arg):
    # using standard months. clean up time handling
    return float(arg) * 31 * 24 * 60 * 60


def handle_spreadsheet():
    return True


# sys args handling to file obj, time cutoff
# TODO make recursive as a function for cleanliness
# TODO have flags in dictionaries with their respective functions to invoke
# TODO modularize for more flags
# TODO try having the functions handle_* not return anything for modularity down the line (-ss's func probably shouldn't return anything)
f, time_cutoff = None, None
for i in range(len(sys.argv)):
    if sys.argv[i] == '-f':
        f = handle_file_path(sys.argv[i + 1])
    if sys.argv[i] == '-mo':
        time_cutoff = handle_time(sys.argv[i + 1])
    # TODO right now just adding flag manually, but do dictionary !!
    if sys.argv[i] == '-ss':
        using_spreadsheet = handle_spreadsheet()

# use defaults if no flags
f, time_cutoff = f or handle_file_path(default_file_name), \
                 time_cutoff or handle_time(default_number_months_cutoff)

# user dictionary construction
# TODO add error codes that are descriptive

user_dict = {}
if not using_spreadsheet:
    for line in f:
        # allow for comments in fansites.txt
        if not line[0] == fansites_comment_character:
            user_dict[line] = "user"
    f.close()
else:
    user_dict = get_twitter_id_to_cells(sheets, sheet_id, sheet_ranges)

inactive_users = {}
errored_users_msgs = []

for user in tqdm(user_dict, desc='Progress on Twitter Users'):
    timeline = None
    try:
        timeline = api.GetUserTimeline(screen_name=user, count=1)
    except twitter.TwitterError:
        if type(user_dict[user]) is Cell:
            msg = f"{user} (at {user_dict[user].__str__()}) has a TwitterError (likely private)"
        else:
            msg = f"{user} has a TwitterError (likely private)"
        errored_users_msgs.append(msg)
        continue
    if timeline:
        last_tweet_time = timeline[0].created_at_in_seconds
        dt_seconds = curr_time - last_tweet_time
        # TODO add multiple tweets to confirm activity, need to be images/rt w/ images
        if dt_seconds > time_cutoff:
            inactive_users[user] = user_dict[user]
    else:
        if type(user_dict[user]) is Cell:
            msg = f"{user} (at {user_dict[user].__str__()}) couldn't be scanned"
        else:
            msg = f"{user} couldn't be scanned"
        errored_users_msgs.append(msg)

for msg in errored_users_msgs:
    print(msg)

print('------------------------------')

for user in inactive_users:
    if type(inactive_users[user]) is Cell:
        msg = f'{user} (at {inactive_users[user].__str__()}) is inactive'
    else:
        msg = f'{user} is inactive'
    print(msg)
