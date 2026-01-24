import sys
import zip_util
import utils as u
import console_handler as ch
zip_codes = zip_util.read_zip_all()


def get_loc_info(command):
    '''
    @requires: command is string user input
               zip_codes is list of available ZIP code records
               u.dd_to_dms, ch.* functions available
    @modifies: None
    @effects:  prompts user for ZIP code, validates, searches database,
               displays location info or error messages
               handles 'end'/'return' special commands
    @returns:  None
    '''

    ch.print_command(command)
    while True:
        ch.print_request_single_zip()
        zip = input()
        ch.print_command(zip)

        if u.handle_special_commands(zip.lower()):
            ch.print_newline()
            return

        if len(zip) != 5 or not zip.isdigit():
            ch.print_invalid_zip()
            continue

        for row in zip_codes:
            if zip == row[0]:
                dms = u.dd_to_dms(row[1], row[2])
                ch.print_location(row, dms)
                ch.print_newline()
                return

        ch.print_zip_not_found(zip)


def get_zip_info(command):
    '''
    @requires: command is string user input
               zip_codes is list of available ZIP code records
               u.handle_special_commands, ch.* functions available
    @modifies: None
    @effects:  prompts for city and state, validates input,
               searches for matching ZIP codes, displays results or errors
               handles 'end'/'return' special commands
    @returns:  None
    '''
    ch.print_command(command)
    while True:
        ch.print_request_city()
        city = input()
        ch.print_command(city)
        if u.handle_special_commands(city.lower()):
            ch.print_newline()
            return

        ch.print_request_state()
        state = input()
        ch.print_command(state)
        if u.handle_special_commands(state.lower()):
            ch.print_newline()
            return

        if not city.isalpha() or not state.isalpha():
            ch.print_invalid_city_state()
            continue

        zip_list = [row[0] for row in zip_codes
                    if city.lower() == row[3].lower() and state.upper() == row[4]]

        if zip_list:
            ch.print_found_zip(city, state, zip_list)
            ch.print_newline()
            return

        ch.print_city_state_not_found(city, state)


def get_dist_info(command):
    '''
    @requires: command is string user input
               zip_codes is list of available ZIP code records
               u.get_distance, u.handle_special_commands, ch.* available
    @modifies: None
    @effects:  prompts for two ZIP codes, validates, searches coordinates,
               calculates and displays distance between them
               handles 'end'/'return' special commands
    @returns:  None
    '''
    ch.print_command(command)
    while True:
        found_first = found_second = False
        ch.print_request_first_zip()
        first_zip = input()
        ch.print_command(first_zip)
        if u.handle_special_commands(first_zip.lower()):
            ch.print_newline()
            return

        ch.print_request_second_zip()
        second_zip = input()
        ch.print_command(second_zip)
        if u.handle_special_commands(second_zip.lower()):
            ch.print_newline()
            return

        if len(first_zip) != 5 or not first_zip.isdigit():
            ch.print_invalid_zip()
            continue

        if len(second_zip) != 5 or not second_zip.isdigit():
            ch.print_invalid_zip()
            continue

        for row in zip_codes:
            if first_zip == row[0]:
                lat1, lon1 = row[1], row[2]
                found_first = True
            if second_zip == row[0]:
                lat2, lon2 = row[1], row[2]
                found_second = True
            if found_first and found_second:
                distance = u.get_distance(lat1, lon1, lat2, lon2)
                ch.print_distance(first_zip, second_zip, distance)
                ch.print_newline()
                return

        if not found_first or not found_second:
            ch.print_zip_not_found(first_zip, second_zip)
            continue




