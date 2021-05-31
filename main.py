from google_utils import *
from ping import ping_pool
scopes = "https://www.googleapis.com/auth/spreadsheets"
credentials_filename = "credentials.json"
token_filename = "token.json"
spreedsheet_id = "1YTUhC0HaHSKriLKEeu6Byp_wOsVkJbxeOe1myCOEPjs"
sheet_number = 0
first_ip_cell = 'B3'
first_ms_cell = 'C3'
paralel_work = 10


def main():
    spredsheets = auth(
        scopes,
        credentials_filename,
        token_filename
    )

    sheet_info = get_sheets_info(spredsheets, spreedsheet_id)

    host_list = get_host_list(
        spredsheets,
        spreedsheet_id,
        first_ip_cell,
        sheet_info
    )

    ping_results = ping_pool(host_list, paralel_work)

    push_result = push_update_values(
        spredsheets,
        spreedsheet_id,
        first_ms_cell,
        sheet_info,
        ping_results,
    )

    print(push_result)


if __name__ == "__main__":
    main()
