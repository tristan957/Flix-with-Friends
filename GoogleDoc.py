import httplib2
import os
import xlwt
import xlrd
from xlutils.copy import copy

from Database import Database
from apiclient import discovery
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage


try:
    import argparse
    flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
except ImportError:
    flags = None

# Creds stored at ~/.credentials/sheets.googleapis.flix-with-friends.json
SCOPES = 'https://www.googleapis.com/auth/spreadsheets'
CLIENT_SECRET_FILE = 'client_secret.json'
APPLICATION_NAME = 'Flix with Friends'


def get_credentials():
    """Gets valid user credentials from storage.

    If nothing has been stored, or if the stored credentials are invalid,
    the OAuth2 flow is completed to obtain the new credentials.

    Returns:
        Credentials, the obtained credential.
    """
    home_dir = os.path.expanduser('~')
    credential_dir = os.path.join(home_dir, '.credentials')
    if not os.path.exists(credential_dir):
        os.makedirs(credential_dir)
    credential_path = os.path.join(credential_dir,
                                   'sheets.googleapis.flix-with-friends.json')

    store = Storage(credential_path)
    credentials = store.get()
    if not credentials or credentials.invalid:
        flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
        flow.user_agent = APPLICATION_NAME
        if flags:
            credentials = tools.run_flow(flow, store, flags)
        else: # Needed only for compatibility with Python 2.6
            credentials = tools.run(flow, store)
        print('Storing credentials to ' + credential_path)
    return credentials


def get_google_doc():
    # Run Google OAuth2
    credentials = get_credentials()
    http = credentials.authorize(httplib2.Http())
    discoveryUrl = ('https://sheets.googleapis.com/$discovery/rest?'
                    'version=v4')
    service = discovery.build('sheets', 'v4', http=http,
                              discoveryServiceUrl=discoveryUrl)

    # Pull data from the Google Sheet
    spreadsheetId = '1JpaDABfhpMfeNMayt1xaEyxbpA369Ze3_UjKCJvNX8c'
    rangeName = 'Sheet1!A:I'
    result = service.spreadsheets().values().get(
        spreadsheetId=spreadsheetId, range=rangeName).execute()
    values = result.get('values', [])

    # Add values to the Excel sheet
    book = xlwt.Workbook(encoding="utf-8")
    sheet1 = book.add_sheet("Sheet 1")
    if not values:
        print('No data found.')
    else:
        i = 0
        for row in values:
            sheet1.write(i, 0, row[0])
            sheet1.write(i, 1, row[1])
            sheet1.write(i, 2, row[2])
            sheet1.write(i, 3, row[3])
            sheet1.write(i, 4, row[4])
            sheet1.write(i, 5, row[5])
            sheet1.write(i, 6, row[6])
            sheet1.write(i, 7, row[7])
            sheet1.write(i, 8, row[8])
            i += 1

    book.save("GoogleDocDB.xlsx")
    Database.location = "GoogleDocDB.xlsx"


def upload_google_doc():
    # Run Google OAuth2
    credentials = get_credentials()
    http = credentials.authorize(httplib2.Http())
    discoveryUrl = ('https://sheets.googleapis.com/$discovery/rest?'
                    'version=v4')
    service = discovery.build('sheets', 'v4', http=http,
                              discoveryServiceUrl=discoveryUrl)

    spreadsheetId = '1OPg5wtyTFglYPGNYug4hDbHGGfo_yP9HOMRVjT29Lf8'

    # Open the Excel sheet to read in data
    workbook = xlrd.open_workbook('GoogleDocDB.xlsx', on_demand=True)
    worksheet = workbook.sheet_by_index(0)

    # transform the workbook to a 2D list
    values = []
    for row in range(worksheet.nrows):
        elm = []
        for col in range(worksheet.ncols):
            elm.append(worksheet.cell_value(row, col))
        values.append(elm)

    # Upload values to the Google Sheet
    body = {
      'values': values
    }
    range_name = 'Sheet1!A1'
    result = service.spreadsheets().values().update(
        spreadsheetId=spreadsheetId, range=range_name,
        valueInputOption='RAW', body=body).execute()


def main():
    # get_google_doc()
    # db = Database(Database.location)

    upload_google_doc()


if __name__ == '__main__':
    main()
