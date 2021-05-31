from google_utils import *
from ping import ping_pool
scopes = "https://www.googleapis.com/auth/spreadsheets"
credentials_filename = "credentials.json"
token_filename = "token.json"
spreadsheet_id = "1YTUhC0HaHSKriLKEeu6Byp_wOsVkJbxeOe1myCOEPjs"
sheet_number = 0
first_ip_cell = 'B3'
first_ms_cell = 'C3'
paralel_work = 10


def main():
    spreadsheets = auth(
        scopes,
        credentials_filename,
        token_filename
    )

    sheet_info = get_sheets_info(spreadsheets, spreadsheet_id)
    del_all_conditional_format(
        spreadsheets, spreadsheet_id, sheet_info)
    addFormatting(spreadsheets, spreadsheet_id,sheet_info, first_ms_cell)
    host_list = get_host_list(
        spreadsheets,
        spreadsheet_id,
        first_ip_cell,
        sheet_info
    )

    ping_results = ping_pool(host_list, paralel_work)

    push_result = push_update_values(
        spreadsheets,
        spreadsheet_id,
        first_ms_cell,
        sheet_info,
        ping_results,
    )



if __name__ == "__main__":
    main()
