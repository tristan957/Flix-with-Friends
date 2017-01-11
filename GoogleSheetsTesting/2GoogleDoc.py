import gspread
from oauth2client.service_account import ServiceAccountCredentials


scope = "https://spreadsheets.google.com/feeds"
credentials = ServiceAccountCredentials.from_json_keyfile_name('My Project-cc695971ece1.json', scope)
gs = gspread.authorize(credentials)

gsheet = gs.open("testing")
