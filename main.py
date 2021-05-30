import google_utils

scopes = "https://www.googleapis.com/auth/spreadsheets"
credentials_filename = "credentials.json"
token_filename = "token.json"
spreedsheet_id = "1YTUhC0HaHSKriLKEeu6Byp_wOsVkJbxeOe1myCOEPjs"
sheet_number = 0


def main():
    spredsheets = google_utils.auth(
        scopes, credentials_filename, token_filename)
    sheet_info = google_utils.get_sheets_info(spredsheets, spreedsheet_id)
    print(sheet_info)


if __name__ == "__main__":
    main()
