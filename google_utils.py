import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials


def auth(scopes, credentials_filename, token_filename):
    """Auth in to google api and refresh token file

    Args:
        scopes (string): scopes url
        credentials_filename (srting): credentials filename
        token_filename (string): token filename

    Returns:
        obj: Google spredsheet object
    """

    creds = None

    if os.path.exists(token_filename):
        creds = Credentials.from_authorized_user_file(token_filename, [scopes])

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                credentials_filename, [scopes])
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open(token_filename, 'w') as token:
            token.write(creds.to_json())

    service = build('sheets', 'v4', credentials=creds)

    return service.spreadsheets()


def get_sheets_info(spreadsheets, spreadsheets_id, sheet_number=0):
    """Get sheet info 

    Args:
        spreadsheets (sting): Obj from auth finction.
        spreadsheets_id (string): Spreedsheets id.
        sheet_number (int, optional): Sheet number from spreedsheets.
            As is displayed in google sheets in the browser starting from 0.
            Defaults to 0.

    Returns:
        [dict]: Return dictionary with format:
                'sheet_id': unic sheet id.
                'title': sheet title.
                'row_count': total row coun.
                'conditional_formats': conditional formats.
    """
    spreadsheets = spreadsheets.get(spreadsheetId=spreadsheets_id).execute()

    properties = spreadsheets['sheets'][sheet_number]['properties']
    conditional_formats = spreadsheets['sheets'][sheet_number]['conditionalFormats']

    sheet_info = {
        'sheet_id': properties['sheetId'],
        'title': properties['title'],
        'row_count': properties['gridProperties']['rowCount'],
        'conditional_formats': conditional_formats,
    }

    return sheet_info
