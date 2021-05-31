# multiping
Multi ping tool with gui in google sheet

# Befor install
- Create google project https://developers.google.com/workspace/guides/create-project 
- Create credentials https://developers.google.com/workspace/guides/create-credentials\
- this software use client oauth NOT SERVICE AUTH
- Save user oauth json file NOT USE SERVICE ACCOUNT FILE

# Install

- clone repo

- copy oauth json file in to repo dir and rename it to credentials.json or change you filename config.ini

- install packages
    - pip install google-api-python-client google-auth-httplib2 google-auth-oauthlib oauth2client

- edit config.ini as your need
    - spreadsheet_id : get for spreadsheet url
        - (https://docs.google.com/spreadsheets/d/1YTUhC0HaHSKriLKEeu6Byp_wOsVkJbxeOe1myCOEPjs)
    - sheet_number : change sheet number as it is visible in googlesheet site, started as 0
    - first_ip_cell : B3 аirst ips cell 
    - first_ms_cell : C3 аirst responses ms cell
    - paralel_work : 10 these settings change how much to spawn concurrent cmd pings

# Run
- run one
    -"python main.py"
- run loop 
    -"python main.py -d 30"
    - -d = delay
    - 30 = seconds

# features?
- !!! replace all Conditional Formatting for sheet
