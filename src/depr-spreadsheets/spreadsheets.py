import requests
from pprint import pprint
import src.private.credentials as c, src.private.testdata as t

an_id = t.testsheet_id
api_key = c.google_api_key
range = "Irene!C1:C2"

url = f"https://sheets.googleapis.com/v4/spreadsheets/{an_id}/values:batchGet/?ranges={range}&valueRenderOption=UNFORMATTED_VALUE&key={api_key}"
url_data = requests.get(url)
json = url_data.json()
pprint(json)