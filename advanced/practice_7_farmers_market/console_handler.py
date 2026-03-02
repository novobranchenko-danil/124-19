from csv_utils import idx as idx
from reviews import ReviewsIndex as r_idx
from enums import Menu as m
import os
import platform


def print_prompt():
    print("🌽🧺 Farmers Market Base 🥕🌻")
    print("-"*29)
    print("  1. login/register")
    print("  2. markets")
    print("  3. search")
    print("  4. nearby")
    print("  5. help")
    print("  q. quit")
    print("-"*29)
    print("> ", end='')


def print_end():
    corn = r'''
___________________1¶1¶1
___________________¶111¶1
_________________1¶11¶11¶¶
________________¶¶¶1¶¶¶1¶¶¶
________________111111111111
_______________1¶¶¶1¶¶¶11¶¶¶
______________1¶¶¶11¶¶¶11¶¶¶1
_______________¶11111111111¶1
______________¶¶¶¶11¶¶¶11¶¶¶¶
______________111111111111111
___1¶¶¶¶¶¶¶¶_1¶¶¶¶1¶¶¶¶¶1¶¶¶¶1__¶¶¶¶¶¶¶¶
_______11¶¶¶__1111_11111_111¶1__¶¶¶1
______1111¶¶_¶¶¶¶¶1¶¶¶¶¶1¶¶¶¶¶__1111¶¶1
___1¶¶¶¶¶111_1¶111_11111111¶11¶¶¶¶¶¶¶¶¶¶1
__¶¶¶¶11111__¶¶¶¶¶1¶¶¶¶¶1¶¶11¶¶¶¶¶¶¶¶¶¶¶¶¶1
_¶¶¶¶¶¶¶¶¶¶¶1_1¶¶¶_11111_1_1¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶
¶¶¶¶¶¶¶¶¶¶¶¶¶1_¶¶¶1¶¶¶¶¶1_1¶¶¶¶¶111111¶¶¶¶¶¶1
1________1¶¶¶¶1_¶¶_111¶1_1¶¶¶¶111________1¶¶¶
___________¶¶¶¶_¶¶1¶¶¶¶¶_¶¶¶11¶¶1___________¶
___________1¶¶¶¶_¶_11¶¶_1¶¶_1¶¶¶
____________¶¶¶¶_¶11¶¶¶_¶¶_1¶¶¶¶
____________¶¶¶¶1_11¶¶_¶¶11¶¶¶¶1
____________¶¶¶¶¶_11¶11¶11¶¶¶¶¶
____________1¶¶¶¶1_1¶_¶¶1¶¶¶¶¶¶
_____________¶¶¶¶¶_111¶1¶¶¶¶¶¶1
_____________¶¶¶¶¶___¶¶¶¶¶¶¶¶¶
______________¶¶¶¶1_¶¶¶¶¶¶¶¶¶¶
______________¶¶¶¶¶1¶¶¶¶¶¶¶¶¶
_______________¶¶¶¶¶¶¶¶¶¶¶¶¶¶
_______________1¶¶¶¶¶¶¶¶¶¶¶¶
________________1¶¶¶¶¶¶¶¶¶¶
_________________1¶¶¶¶¶¶¶1
___________________¶¶¶¶¶
'''
    corn_lines = corn.strip('\n').split('\n')
    max_width = max(len(line) for line in corn_lines)
    text = "Good Bye!"
    text_padding = (max_width - len(text)) // 2
    print(' ' * text_padding + text)
    print('\033[93m' + corn + '\033[0m')


def print_command(command):
    print(f"Input command: {command}")


def print_help():
    print("-" * 50)
    print("AVAILABLE COMMANDS:")
    print("-" * 50)
    print("  1. login/register       – sign in or create new account")
    print("  2. markets              – show all markets (paginated)")
    print("  3. search               – search by city & state or zip code")
    print("  4. nearby               – search within radius (zip + miles)")
    print("  5. help                 – show this help")
    print("  q. quit                 – exit program")
    print("-" * 50)


def print_pagination(total_page, current_page):
    print(f"\n--- Страница {current_page + 1}/{total_page} ---")


def print_pagination_description():
    print("[n] next page  [p] previous page  [q] to return to previous menu  [number] view market details")


def print_market_page(index, market):
    indent = " " * (4 - len(str(index)))  # для индексов до 999
    print(f"{index}.{indent} {market['name']:<85} (Avg.rating {market['avg.rating']})")

def print_search_mode():
    print("-" * 50)
    print("Search markets")
    print("-" * 50)
    print("What would you like to search by?\n")
    print("  1. FMID            (e.g., 1010972)")
    print("  2. Market name     (e.g., Fifth Street Farmers' Market)")
    print("  3. State and City  (e.g., Vermont, Burlington)")
    print("  4. Zip Code        (e.g., 05401)")
    print("  q. Back to main menu")
    print("-" * 50)
    print("> ", end='')


def print_log_reg_mode():
    print("-" * 50)
    print("login/register")
    print("-" * 50)
    print("What would you like to do?\n")
    print("  [1]. Register")
    print("  [2]. Login")
    print("  [q]. Back to main menu")
    print("-" * 50)
    print("> ", end='')


def print_nearby_mod():
    print("-" * 50)
    print("Search market nearby")
    print("-" * 50)
    print("Find farmers markets within 30 miles from:")
    print("Select search method:\n")
    print("  1. By FMID         - exact match (e.g., 1010972)")
    print("                       finds markets near that specific market")
    print("  2. By market name  - partial match (e.g., 'Street')")
    print("                       finds FIRST matching market,")
    print("                       then shows other markets within 30 miles")
    print("  3. By state+city   - finds markets in that city")
    print("                       returns FIRST market found,")
    print("                       then shows other markets within 30 miles")
    print("                       (e.g., Vermont, Burlington)")
    print("  4. By zip code     - finds markets in that area")
    print("                       returns ALL markets in that zip,")
    print("                       then shows markets within 30 miles from each")
    print("                       (e.g., 05401)")
    print("  q. Back to main menu")
    print("-" * 50)
    print("> ", end='')


def print_market_not_found():
    print("Markets not found")


def details_not_found():
    print("Details not found")


def print_count_market_found_by_city_state(count, city, state, nearby=False):
    if nearby:
        if count == 1:
            print(f"{count} market was found nearby:\nState: {state} \nCity: {city}")
        else:
            print(f"{count} markets were found nearby:\nState: {state} \nCity: {city}")
    else:
        if count == 1:
            print(f"{count} market was found in:\nState: {state} \nCity: {city}")
        else:
            print(f"{count} markets were found in:\nState: {state} \nCity: {city}")


def print_count_market_found_by_zip(count, zip, nearby=False):
    if nearby:
        if count == 1:
            print(f"{count} market was found nearby zip {zip}")
        else:
            print(f"{count} markets were found nearby zip {zip}")
    else:
        if count == 1:
            print(f"{count} market was found in zip {zip}")
        else:
            print(f"{count} markets were found in zip {zip}")


def print_count_market_found_by_fmid(count, fmid, nearby=False):
    if nearby:
        if count == 1:
            print(f"{count} market was found nearby FMID {fmid}")
        else:
            print(f"{count} markets were found nearby FMID {fmid}")
    else:
        if count == 1:
            print(f"{count} market was found with FMID {fmid}")
        else:
            print(f"{count} markets were found with FMID {fmid}")


def print_count_market_found_by_market_name(count, market_name, nearby=False):
    if nearby:
        if count == 1:
            print(f"{count} market was found nearby market with name: '{market_name}'")
        else:
            print(f"{count} markets were found nearby market with name: '{market_name}'")
    else:
        if count == 1:
            print(f"{count} market was found with market name: '{market_name}'")
        else:
            print(f"{count} markets were found with market name: '{market_name}'")


def print_count_market_reviews(count, fmid, market_name):
    if count == 1:
        print(f"{count} review was found for {market_name}, FMID {fmid}")
    else:
        print(f"{count} reviews were found for {market_name}, FMID {fmid}")


def print_market_found_nearby(index, market):
    print("-"*65)
    website = market['website'] if market['website'] else "No website"
    print(f"{index}. FMID: {market['fmid']}")
    indent = len(f"{index}.")
    print(f"{' ' * indent} Name: {market['market_name']}")
    print(f"{' ' * indent} City: {market['city']}")
    print(f"{' ' * indent} State: {market['state']}")
    print(f"{' ' * indent} Website: {website}")
    print(f"{' ' * indent} ZIP: {market['zip']}")
    print(f"{' ' * indent} Distance: {market['distance']} miles")
    print(f"{' ' * indent} Avg. rating: {market['avg.rating']}")
    print("-"*65)


def print_markets_list(index, market):
    print("-" * 65)
    website = market['website'] if market['website'] else "No website"
    # Первая строка
    print(f"{index}. FMID: {market['fmid']}")
    indent = len(f"{index}.")
    print(f"{' ' * indent} Name: {market['market_name']}")
    print(f"{' ' * indent} State: {market['state']}")
    print(f"{' ' * indent} City: {market['city']}")
    print(f"{' ' * indent} ZIP: {market['zip']}")
    print(f"{' ' * indent} Website: {website}")
    print(f"{' ' * indent} Avg. rating: {market['avg.rating']}")
    print("-" * 65)


def print_newline():
    print()


def print_invalid_command():
    print("Invalid command, ignoring")


def print_invalid_zip():
    print("Invalid ZIP code. Must be exactly 5 digits (0-9).")


def print_invalid_fmid():
    print("Invalid FMID. Must be exactly digits (0-9).")


def print_detail_description():
    print("[q] back to list [c] leave comment [v] view reviews")


def print_detail_information(market, avg_rating):
    print(f"Details for market with FMID {market['FMID']}. Avg.rating: {avg_rating}")
    print("-"*129)
    for field in idx:
        field_value = market[field.name] if market[field.name] else "None"
        print(f"{field.name:<15} | {field_value:>110} |")
    print("-"*129)


def print_login():
    print("Enter username: ", end='')


def print_password():
    print("Enter password: ", end='', flush=True)


def print_confirm():
    print("Confirm password: ", end='', flush=True)


def print_password_dont_match():
    print("Passwords don't match!")
    print("Please try again")


def print_registration_success():
    print("Registration successful!")


def print_user_exists():
    print("User with this name already exists!")
    print("Please choose another username or login.")


def print_login_welcome(username):
    print(f"Welcome, {username}")


def print_invalid_credentials():
    print("Invalid username or password")
    print("Please try again.")


def print_user_not_found():
    print("User not found")
    print("Please check username or register.")


def print_authorization_failed():
    print("Authorization failed")
    print("Please use register or login in main menu to continue")


def print_not_logged_in():
    print("Please use login in main menu to continue")


def print_comment_instructions(fmid, market_name):
    print(f"You can leave a review for {market_name} with FMID {fmid}.")
    print("Write your comment (optional) and give a rating (1-5 stars, required).")
    print("Enter [q] for return to previous menu\n")


def print_comment_prompt():
    print("Write your comment (optional, press Enter to skip): ", end='')


def print_rating_prompt():
    print("Rate this market (1-5 stars): ", end='')


def print_invalid_rating():
    print("Please enter a number between 1 and 5: ", end='')


def print_invalid_input():
    print("Invalid input. Please enter a number: ", end='')


def print_review_saved():
    print("Thank you! Your review has been saved.\n")


def print_view_reviews_prompt(market_name, fmid):
    print(f"Reviews for {market_name} with FMID {fmid}")


def print_reviews(index, review):
    print("-" * 72)
    first_field = list(r_idx)[0]
    first_value = review[first_field.name.lower()]
    print(f"{index}. {first_field.name:<13} | {first_value:>50}")
    indent = len(f"{index}.")
    for field in list(r_idx)[1:]:
        field_value = review[field.name.lower()] if review[field.name.lower()] else "None"
        print(f"{' ' * indent} {field.name:<13} | {field_value:>50}")
    print("-" * 72)


def print_reviews_not_found():
    print("Reviews not found")


def print_return_to_previous_menu():
    print("Enter [q] for return to previous menu")
    print("> ", end='')


def print_request_fmid():
    print("Enter FMID: ", end='')


def print_request_market_name():
    print("Enter market name: ", end='')


def print_request_zip_code():
    print("Enter ZIP: ", end='')


def print_request_state():
    print("Enter state: ", end='')


def print_request_city():
    print("Enter city: ", end='')


def search_wrapper_mode(command):
    if command == m.Main.SEARCH:
        print_search_mode()
    elif command == m.Main.NEARBY:
        print_nearby_mod()


def print_market_list_wrapper(search_type, i, market):
    if search_type == "nearby":
        print_market_found_nearby(i, market)
    else:
        print_markets_list(i, market)


def clear_console():
    current_os = platform.system()
    if current_os == "Windows":
        os.system('cls')
    else:
        os.system('clear')
