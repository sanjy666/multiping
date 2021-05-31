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
        obj: Google spreadsheet object
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


def get_sheets_info(spreadsheets, spreadsheets_id, sheet_number):
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
    if 'conditionalFormats' not in spreadsheets['sheets'][sheet_number].keys():
        conditional_formats = []
    else:
        conditional_formats = spreadsheets['sheets'][sheet_number]['conditionalFormats']

    sheet_info = {
        'sheet_id': properties['sheetId'],
        'title': properties['title'],
        'row_count': properties['gridProperties']['rowCount'],
        'conditional_formats': conditional_formats,
    }

    return sheet_info


def get_host_list(spreadsheets, spreadsheets_id, start_cell, sheet_info):
    """Get host list from sheet in range

    Args:
        spreadsheets (obj):
            spregseets obj from auth func
        spreadsheets_id (str):
            spreadsheet id
        range (str):
            range aka "Sheet1!A1:B1"

    Returns:
        list of lists: [[0.0.0.0],[1.1.1.1]]
        why list of lists?
        this is native response from google api,
        for compatibility with other functions,
        and for future to send more values in requests
    """
    range = gen_max_range_str(start_cell, sheet_info)
    result = spreadsheets.values().get(
        spreadsheetId=spreadsheets_id,
        range=range,
        majorDimension='ROWS'
    ).execute()
    values = result.get('values')
    return values


def split_cell_name(cell):
    """
    Split cell 
    """
    letters = cell[
        int(cell.find(cell[0])):
        int(cell.rfind(
            cell[0]) + 1):
    ]

    numbers = cell[
        (cell.rfind(cell[0])) + 1:
        len(cell)
    ]
    return [letters, int(numbers)]


def gen_max_range_str(start_cell, sheet_info):
    """Make googlesheet range string from start_cell to sheet_info['row_count'] like "Sheet1!A1:B1"

    Args:
        start_cell (string):
            first cell name
        sheet_info (dict):
            dict generated from get_sheets_info()

    Returns:
        string:
            aka "Sheet1!A1:B1"
    """
    letters = split_cell_name(start_cell)[0]
    range = sheet_info['title'] + "!" + start_cell + \
        ":" + letters + str(sheet_info['row_count'])
    return range


def push_update_values(sheet, spreadsheet_id, first_ms_cell, sheet_info, values):
    total_cell = sheet_info['row_count']
    # last cell offset aka C3 = number 2 cell (0 = B1, 1 = B2)
    last_cell = total_cell - (split_cell_name(first_ms_cell)[1] - 1)

    # append void values for replace old not valid cells
    for i in range(len(values), last_cell):
        values.append([''])

    ranges = gen_max_range_str(first_ms_cell, sheet_info)

    result = sheet.values().batchUpdate(
        spreadsheetId=spreadsheet_id,
        body={
            "valueInputOption": "USER_ENTERED",
            "data": [
                {
                    "range": ranges,
                    "majorDimension": "ROWS",
                    "values": values
                }
            ]
        }
    ).execute()
    return result


def del_all_conditional_format(spreadsheets, spreadsheet_id, sheet_info):
    indexCount = len(sheet_info['conditional_formats'])

    if indexCount == 0:
        return

    requests = []

    delRequest = {
        "deleteConditionalFormatRule":
        {
            "sheetId": sheet_info['sheet_id'],
            "index": 0,
        }
    }

    for i in range(0, indexCount):
        requests.append(delRequest)

    body = {
        'requests': requests
    }

    result = spreadsheets.batchUpdate(
        spreadsheetId=spreadsheet_id,
        body=body,
    ).execute()

    return result


def a1_to_num(cell_letters):
    dictionary = {
        'A': '0', 'B': '1', 'C': '2', 'D': '3', 'E': '4', 'F': '5', 'G': '6',
        'H': '7', 'I': '8', 'J': '9', 'K': '10', 'L': '11', 'M': '12', 'N': '13',
        'O': '14', 'P': '15', 'Q': '16', 'R': '17', 'S': '18', 'T': '19', 'U': '20',
        'V': '21', 'W': '22', 'X': '23', 'Y': '24', 'Z': '25',
    }
    table = cell_letters.maketrans(dictionary)
    if len(cell_letters) > 1:
        print('AA format not support')
        return -1
    else:
        return int(cell_letters.translate(table))

def addFormatting(spreadsheets, spreadsheet_id, sheet_info, first_ms_cell):
    col_litters = split_cell_name(first_ms_cell)[0]
    col_num = a1_to_num(col_litters)
    range = {
        'sheetId': sheet_info['sheet_id'],
        "startRowIndex": split_cell_name(first_ms_cell)[1] - 1,
        "endRowIndex": sheet_info['row_count'],
        "startColumnIndex": col_num,
        "endColumnIndex": col_num + 1
    }
    spreadsheets.batchUpdate(
        spreadsheetId=spreadsheet_id,
        body={
            "requests": [{
                'addConditionalFormatRule': {
                    'rule': {
                        'ranges': range,
                        'booleanRule': {
                            'condition': {
                                'type': 'TEXT_EQ',
                                'values': [{
                                    "userEnteredValue": 'n/a'
                                }]
                            },
                            "format": {
                                "backgroundColor": {
                                    "red": 1
                                }
                            }
                        }
                    },
                    'index': 0
                }
            }, {
                'addConditionalFormatRule': {
                    'rule': {
                        'ranges': range,
                        'booleanRule': {
                            'condition': {
                                'type': 'NUMBER_LESS_THAN_EQ',
                                'values': [{
                                    "userEnteredValue": "200"
                                }]
                            },
                            "format": {
                                "backgroundColor": {
                                    "green": 1
                                }
                            }
                        }
                    },
                    'index': 1
                }
            }, {
                'addConditionalFormatRule': {
                    'rule': {
                        'ranges': range,
                        'booleanRule': {
                            'condition': {
                                'type': 'NUMBER_GREATER',
                                'values': [{
                                    "userEnteredValue": "200"
                                }]
                            },
                            'format': {
                                'backgroundColor': {
                                    'red': 1,
                                    'green': 1
                                }
                            }
                        }
                    },
                    'index': 2
                }
            }]
        }
    ).execute()
