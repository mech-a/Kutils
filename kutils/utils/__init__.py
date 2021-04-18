"""
Collection of utilities for Kutils that do not fit in neatly with other classes.
"""

import os
from pathlib import Path
import json
from google.oauth2 import service_account


def get_column_alphabetical_index_from_zero_indexed_num(col_idx: int) -> str:
    """Convert zero-index column number to alphabetical base-26 (e.g. 0 -> 'A', 27 -> 'AA'"""
    num_letters_alphabet = 26

    def get_letter_from_zero_indexed_idx(idx: int):
        ascii_start = 65
        return chr(ascii_start + idx)

    prefix_str = ''
    if col_idx < num_letters_alphabet:
        return get_letter_from_zero_indexed_idx(col_idx)
    last_char = get_letter_from_zero_indexed_idx(col_idx % num_letters_alphabet)
    prefix_str = get_column_alphabetical_index_from_zero_indexed_num(col_idx // num_letters_alphabet)
    return prefix_str + last_char


def get_credentials(scopes: list):
    credentials_file = Path(os.environ['KUTILSPVT']) / 'tester-google-credentials.json'
    if not credentials_file.is_file():
        print('tester-google-credentials.json is not a file')
        raise IOError
    g_credentials = service_account.Credentials.from_service_account_file(credentials_file, scopes=scopes)
    return g_credentials


def get_default_credentials():
    g_scopes = ['https://www.googleapis.com/auth/youtube.readonly',
                "https://www.googleapis.com/auth/spreadsheets.readonly"]
    return get_credentials(g_scopes)


def get_twitter_credentials():
    twt_cred_path = Path(os.environ['KUTILSPVT']) / 'twitter-credentials.json'
    cred_file = open(twt_cred_path)
    twt_creds = json.load(cred_file)
    return twt_creds