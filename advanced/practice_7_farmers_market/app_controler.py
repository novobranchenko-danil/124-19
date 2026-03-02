from enums import Menu as m
import console_handler as ch
import csv_utils as csv
import authorization as auth
import string
import getpass


def command_processing(command):
    if command == m.Main.LOGIN_REGISTER:
        process_register()

    elif command == m.Main.MARKETS:
        csv.search_all_markets()

    elif command == m.Main.SEARCH:
        process_search(command)

    elif command == m.Main.NEARBY:
        process_search(command, search_type='nearby')

    elif command == m.Main.HELP:
        process_help()

    elif command == m.Main.EXIT:
        process_exit(command)
    else:
        process_invalid_command(command)


def process_search(command, search_type=None):
    ch.clear_console()
    while True:
        ch.search_wrapper_mode(command)
        user_input = input().strip()
        if user_input == m.Search.FMID:
            ch.print_request_fmid()
            user_fmid = input().strip()
            if not user_fmid.isdigit():
                ch.clear_console()
                ch.print_invalid_fmid()
                continue
            process_search_wrapper(user_input, search_type, user_fmid)
        elif user_input == m.Search.MARKET_NAME:
            ch.print_request_market_name()
            user_mn = string.capwords(input().strip())
            process_search_wrapper(user_input, search_type, user_mn)
        elif user_input == m.Search.CITY_STATE:
            ch.print_request_state()
            state = input().strip().title()
            ch.print_request_city()
            city = input().strip().title()
            process_search_wrapper(user_input, search_type, state, city)
        elif user_input == m.Search.ZIP:
            ch.print_request_zip_code()
            zip_code = input().strip()
            if len(zip_code) != 5 or not zip_code.isdigit():
                ch.clear_console()
                ch.print_invalid_zip()
                continue
            process_search_wrapper(user_input, search_type, zip_code)
        elif user_input == m.Search.BACK:
            ch.clear_console()
            break
        else:
            ch.clear_console()
            ch.print_command(user_input)
            ch.print_invalid_command()


def process_search_wrapper(user_input, search_type, *params):
    if user_input == m.Search.FMID:
        if search_type != "nearby":
            csv.search_market_by_params(*params, 'exact', 'fmid')
        else:
            csv.search_nearby_markets(*params, 'exact', 'fmid')

    elif user_input == m.Search.MARKET_NAME:
        if search_type != "nearby":
            csv.search_market_by_params(*params, 'contains', 'market_name')
        else:
            csv.search_nearby_markets(*params, 'contains', 'market_name')

    elif user_input == m.Search.CITY_STATE:
        if search_type != "nearby":
            csv.search_market_by_params(params, 'both', ('state', 'city'))
        else:
            csv.search_nearby_markets(params, 'both', ('state', 'city'))

    elif user_input == m.Search.ZIP:
        if search_type != "nearby":
            csv.search_market_by_params(*params, 'exact', 'zip_code')
        else:
            csv.search_nearby_markets(*params, 'exact', 'zip_code')


def process_register():
    ch.clear_console()
    while True:
        ch.print_log_reg_mode()
        user_input = input().strip()
        if user_input == m.Auth.REGISTER:
            ch.print_login()
            auth.Username.username = input().strip()
            ch.print_password()
            password = getpass.getpass("")
            ch.print_confirm()
            confirm = getpass.getpass("")
            if not auth.register(auth.Username.username, password, confirm):
                continue
        elif user_input == m.Auth.LOGIN:
            ch.print_login()
            auth.Username.username = input().strip()
            ch.print_password()
            password = getpass.getpass("")
            if not auth.login(auth.Username.username, password):
                continue
        elif user_input == m.Auth.BACK:
            ch.clear_console()
            break
        else:
            ch.clear_console()
            ch.print_command(user_input)
            ch.print_invalid_command()


def process_help():
    ch.clear_console()
    ch.print_help()
    ch.print_newline()


def process_exit(command):
    ch.clear_console()
    ch.print_end()
    return command


def process_invalid_command(command):
    ch.clear_console()
    ch.print_command(command)
    ch.print_invalid_command()
    ch.print_newline()
