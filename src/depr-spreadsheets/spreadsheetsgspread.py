import gspread
import src.private.credentials as c, src.private.testdata as t

gc = gspread.service_account(c.google_credentials_path)

sh = gc.open_by_key(t.testsheet_id)



