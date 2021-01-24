# -*- coding: utf-8 -*-
"""
Created on Mon Jan 18 19:52:42 2021

TWITTER FANSITE INACTIVITY CHECKER [fansites.py]
Compatability: Python 3.4+, Windows
Dependencies: python-twitter (pip install python-twitter)

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
      > py fansites.py -f 'c:/users/mecha/desktop/i love red velvet/fansites.txt' -mo 238
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
@version: 0.0.2:gs
~~ Made with love for RVCord, https://discord.gg/redvelvet ~~
"""

import twitter
import time
import sys
# import os
from pathlib import Path
import src.sheets.sheetfunctions as shf

# REMOVE THIS LINE IF YOU ARE NOT A DEVELOPER! THE SCRIPT WILL NOT RUN OTHERWISE
import src.private.credentials as c, src.private.testdata as t

# --- USER CONSTANTS ----------------------------------------------------------

# FILL THESE IN WITH YOUR OWN KEYS/SECRETS
# TODO serialize this using pickle this is too crude
api_key = "" or c.twitter_api_key
api_secret = "" or c.twitter_api_key_secret
access_tkn_key = "" or c.twitter_access_token
access_tkn_secret = "" or c.twitter_access_token_secret

# change this number to change the default number of standard months of inactivity needed to deem account inactive;
# this is used when no month argument is passed in
default_number_months_cutoff = 6
# default file with all twitter @s to check
default_file_name = "fansites.txt"
# character used in fansites to ignore the line
fansites_comment_character = '#'


# default google sheet ID to read from
sheet_id = '' or t.testsheet_id
# default ranges on Google Sheet ID to read from (see *INSERT GOOGLE SHEETS API V4 LINK)
# sheet_ranges = ['{NAME OF SHEET}!{RANGE OF CELLS}' ...]
# sheet_ranges = ['Irene!C:C', ...]
sheet_ranges = [] or t.testrange
#

# TODO implement developer bypass or make new git branch
debug = False

# --- CODE --------------------------------------------------------------------

curr_time = time.time()
api = twitter.Api(consumer_key=api_key,
                  consumer_secret=api_secret,
                  access_token_key=access_tkn_key,
                  access_token_secret=access_tkn_secret)
# developer override here
using_spreadsheet = True
use_sleep = True


def handle_file_path(arg):
    # TODO implement os-agnostic project root file handling, see https://stackoverflow.com/questions/25389095/python-get-path-of-root-project-structure
    # "'c:/expecting spaces/'" -> "c:/expecting spaces/"
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
    return arg * 31 * 24 * 60 * 60

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
        f = handle_file_path(sys.argv[i+1])
    if sys.argv[i] == '-mo':
        time_cutoff = handle_time(sys.argv[i+1])
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
        print(line)
        # allow for comments in fansites.txt
        if not line[0] == fansites_comment_character:
            user_dict[line] = "active"
    f.close()
else:
    usernames = shf.get_twitter_usernames_from_sheet(sheet_id, ranges=sheet_ranges)
    for username in usernames:
        user_dict[username] = 'active'

for user in user_dict:
    timeline = None
    try:
        timeline = api.GetUserTimeline(screen_name=user, count=1)
    except twitter.TwitterError:
        print(user, 'has a TwitterError')
        continue
    if timeline:
        last_tweet_time = timeline[0].created_at_in_seconds
        dt_seconds = curr_time - last_tweet_time
        # TODO add multiple tweets to confirm activity, need to be images/rt w/ images
        if dt_seconds > time_cutoff:
            user_dict[user] = "inactive"
            print(user, "is inactive")
    else:
        print('could not scan twitter user', user)
