import google_utils

scopes = "https://www.googleapis.com/auth/spreadsheets"
credentials_filename = "credentials.json"
token_filename = "token.json"

def main():
    spredsheets = google_utils.auth(scopes, credentials_filename, token_filename)
    print(spredsheets)


if __name__ == "__main__":
    main()