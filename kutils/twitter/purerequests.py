from googleapiclient.discovery import build
from google.oauth2 import service_account
import kutils.sheets.sheetfunctions as shf
from urllib.parse import urlparse
from kutils.utils import get_default_credentials
from urllib.parse import urlparse

"""
Stripped down tester file for features to be implemented in fansites.py
"""

# RV Fansite sheet & ranges
sheet_id = '18UdgCmsV2AISuM47wVJ1-w2jRrjWlFP_xiKc2EcBUV4'
sheet_ranges = ['Irene!C:C', 'Seulgi!C:C', 'Wendy!C:C', 'Joy!C:C', 'Yeri!C:C', 'Group / Multi!C:C']

creds = get_default_credentials()
sheets = build('sheets', "v4", credentials=creds)
