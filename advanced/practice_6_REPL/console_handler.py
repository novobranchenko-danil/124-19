def print_prompt():
    print("Command ('loc', 'zip', 'dist', 'end') => ", end='')


def print_end():
    print("Done")


def print_command(command):
    print(command)


def print_request_single_zip():
    print("Enter a ZIP Code to lookup => ", end='')


def print_request_first_zip():
    print("Enter the first ZIP Code => ", end='')


def print_request_second_zip():
    print("Enter the second ZIP Code => ", end='')


def print_location(row: list, dms: list):
    print(f"ZIP code {row[0]} is in {row[3]}, {row[4]}, {row[5]} country,\n"
          f"coordinates: ({dms[0]},{dms[1]})")


def print_distance(first_zip, second_zip, distance):
    print(f"The distance between {first_zip} and {second_zip} is {distance:.2f} miles")


def print_found_zip(city: str, state: str, zip_list: list):
    print(f"The following ZIP Code(s) found for {city.title()}, {state.upper()}: {', '.join(zip_list)}")


def print_request_city():
    print("Enter a city name to lookup => ", end='')


def print_request_state():
    print("Enter the state name to lookup => ", end='')


def print_invalid_zip():
    print("Invalid ZIP code. Must be exactly 5 digits (0-9).\n"
          "Options: Enter ZIP code again | 'return' for main menu | 'end' to exit")


def print_invalid_city_state():
    print("Invalid city/state name. Must contain only letters.\n"
          "Options: Enter again | 'return' for main menu | 'end' to exit")


def print_zip_not_found(*zip):
    print(f"Warning: ZIP code '{zip}' not found.\n"
          f"Options: Enter ZIP code again | 'return' for main menu | 'end' to exit")


def print_city_state_not_found(city: str, state: str):
    print(f"City {city.title()} and/or state {state.upper()} not found in the database.\n"
          f"Options: Enter again | 'return' for main menu | 'end' to exit")


def print_invalid_command():
    print("Invalid command, ignoring")


def print_newline():
    print()
