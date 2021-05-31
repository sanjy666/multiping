import sys
from google_utils import *
from ping import ping_pool
import configparser
from time import sleep


def read_config(path):
    if not os.path.exists(path):
        retun = 0

    config_file = configparser.ConfigParser()
    config_file.read(path)
    config = {
        'scopes': config_file.get('main', 'scopes'),
        'credentials_filename': config_file.get('main', 'credentials_filename'),
        'token_filename': config_file.get('main', 'token_filename'),
        'spreadsheet_id': config_file.get('main', 'spreadsheet_id'),
        'sheet_number': config_file.get('main', 'sheet_number'),
        'first_ip_cell': config_file.get('main', 'first_ip_cell'),
        'first_ms_cell': config_file.get('main', 'first_ms_cell'),
        'paralel_work': config_file.get('main', 'paralel_work'),
    }

    return config


def main(config):
    scopes = config['scopes']
    credentials_filename = config['credentials_filename']
    token_filename = config['token_filename']
    spreadsheet_id = config['spreadsheet_id']
    sheet_number = int(config['sheet_number'])
    first_ip_cell = config['first_ip_cell']
    first_ms_cell = config['first_ms_cell']
    paralel_work = int(config['paralel_work'])

    spreadsheets = auth(
        scopes,
        credentials_filename,
        token_filename
    )

    sheet_info = get_sheets_info(spreadsheets, spreadsheet_id, sheet_number)

    del_all_conditional_format(
        spreadsheets, spreadsheet_id, sheet_info)

    addFormatting(spreadsheets, spreadsheet_id, sheet_info, first_ms_cell)

    host_list = get_host_list(
        spreadsheets,
        spreadsheet_id,
        first_ip_cell,
        sheet_info
    )

    ping_results = ping_pool(host_list, paralel_work)

    push_update_values(
        spreadsheets,
        spreadsheet_id,
        first_ms_cell,
        sheet_info,
        ping_results,
    )


if __name__ == '__main__':
    config = read_config('config.ini')

    if len(sys.argv) > 2 and sys.argv[1] == '-d':
        while True:
            main(config)
            sleep(int(sys.argv[2]))
    else:
        main(config)
