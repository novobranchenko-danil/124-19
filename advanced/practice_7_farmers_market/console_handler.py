from csv_utils import State as s
from csv_utils import MarketsIndex as idx


def print_prompt():
    print("🌽🧺 Farmers Market Base 🥕🌻")
    print("-"*29)
    print("  ?. login/register [todo]") # Todo исправить нумерацию
    print("  1. markets")
    print("  2. search")
    print("  3. nearby")
    print("  4. help")
    print("  5. quit")
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


def print_pagination(total_page):
    print(f"\n--- Страница {s.current_page + 1}/{total_page} ---")


def print_pagination_description():
    print("[n] next page  [p] previous page  [q] quit  [number] view market details")  # todo сделать q как в целом завершение программы, а добавить кнопку выход в главное меню соответственно переименовать


def print_market_page(index, market):
    print(f"{index}. {market['name']}")


def print_search_mode():
    print("-" * 50)
    print("SEARCH MARKETS")
    print("-" * 50)
    print("What would you like to search by?")
    print("  [1]. City and State  (e.g., Burlington Vermont)")
    print("  [2]. Zip Code        (e.g., 05401)")
    print("  [q]. Back to main menu")
    print("-" * 50)


def print_market_not_found():
    print("Markets not found")


def details_not_found():
    print("Details not found")


def print_count_market_found_by_city_state(count, city, state):
    if count == 1:
        print(f"{count} market was found in:\nCity: {city} \nState: {state}")
    else:
        print(f"{count} markets were found in:\nCity: {city} \nState: {state}")


def print_count_market_found_by_zip(count, zip):
    if count == 1:
        print(f"{count} market was found in zip {zip}")
    else:
        print(f"{count} markets were found in zip {zip}")


def print_count_market_found_nearby(count, zip):
    if count == 1:
        print(f"{count} market was found nearby zip {zip}")
    else:
        print(f"{count} markets were found nearby zip {zip}")


def print_market_found_nearby(index, market):
    print("-"*50)
    website = market['website'] if market['website'] else "No website"
    print(f"\n{index}. FMID: {market['fmid']}")
    print(f"   Name: {market['name']}")
    print(f"   City: {market['city']}")
    print(f"   State: {market['state']}")
    print(f"   Website: {website}")
    print(f"   ZIP: {market['zip']}")
    print(f"   Distance: {market['distance']} miles")
    print("-"*50)


def print_markets_list(index, market):
    print("-"*50)
    website = market['website'] if market['website'] else "No website"
    print(f"\n{index}. FMID: {market['fmid']}")
    print(f"   Name: {market['name']}")
    'zip' in market and print(f"   ZIP: {market['zip']}")
    'city' in market and print(f"   City: {market['city']}")
    'state' in market and print(f"   State: {market['state']}")
    print(f"   Website: {website}")
    print("-"*50)


def print_back_to_main_menu():
    print("Return to the main menu")


def print_newline():
    print()


def print_continue_request():
    print("Do you want to continue?")
    print("[y] to continue, [q] to quit")


def print_invalid_command():
    print("Invalid command, ignoring")


def print_invalid_zip():
    print("Invalid ZIP code. Must be exactly 5 digits (0-9).\n"
          "Enter zip again or press [q] to return to previous menu")


def print_detail_description():
    print("[q] back to list [c] leave comment")


def print_detail_information(market):
    print(f"Details for market with FMID {market['FMID']}")
    print("-"*74)
    for field in idx:
        field_value = market[field.name] if market[field.name] else "None"
        print(f"{field.name:<15} | {field_value:>55} |")#TODO 55->100
    print("-"*74)

