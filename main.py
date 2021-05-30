from google_utils import *

scopes = "https://www.googleapis.com/auth/spreadsheets"
credentials_filename = "credentials.json"
token_filename = "token.json"
spreedsheet_id = "1YTUhC0HaHSKriLKEeu6Byp_wOsVkJbxeOe1myCOEPjs"
sheet_number = 0
first_ip_cell = 'B3'


def main():
    spredsheets = auth(
        scopes, credentials_filename, token_filename)
    sheet_info = get_sheets_info(spredsheets, spreedsheet_id)
    host_list = get_host_list(
        spredsheets, spreedsheet_id, gen_max_range_str(first_ip_cell, sheet_info))
    print(host_list)


if __name__ == "__main__":
    main()
