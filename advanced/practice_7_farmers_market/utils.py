import sys
import os
import platform
import console_handler as ch
import data_handler as dh
from csv_utils import State as s
from csv_utils import MarketsIndex as idx
from math import radians, sin, cos, sqrt, asin


def handle_special_commands(command): # TODO перенести q в command processing , а end сделать общим для каждого блока для полного выхода из программы?
    if command == "end" or command == "q":
        clear_console()
        ch.print_end()
        sys.exit()


def clear_console(): # todo перенести в console handler? подумать как назвать
    current_os = platform.system()
    if current_os == "Windows":
        os.system('cls')
    else:
        os.system('clear')


def command_processing(command): # TODO разнести каждлую комманду в отдельную функцию
    if command == 'help' or command == "4":
        clear_console()
        ch.print_command("help [4]") # todo сделать класс с индексами меню. чтобы не передавать явно название выбранного пункта, чтобы все менялось в одном месте
        ch.print_help()
        ch.print_newline()

    elif command == "markets" or command == "1":
        clear_console()
        ch.print_command("markets [1]")
        dh.search_all_markets()
    elif command == "search" or command == "2": # TODO ДОБАВИТЬ ПОИСК ПО ЛЮБОМУ ПУНКТУ МЕНЮ!
        clear_console()
        ch.print_command("search [2]")
        while True:
            ch.print_search_mode()
            user_input = input("> ").strip()
            if user_input == "1": # todo лучше сначала штат потом город
                city = input("Enter city: ").strip().title()
                state = input("Enter state: ").strip().title() # TODO тут тоже q?
                clear_console()
                dh.search_by_city_state(city, state)
                break
            elif user_input == "2":
                while True:
                    zip = input("Enter zip: ").strip()
                    if zip == "q":
                        clear_console()
                        break
                    elif len(zip) != 5 or not zip.isdigit(): # TODO добавить описание для q
                        clear_console()
                        ch.print_invalid_zip()
                        continue
                    clear_console()
                    dh.search_by_zip(zip)
                    break
                break # TODO добавить возможность выхода в main menu с любого места и выключения программы?
            elif user_input == "q":
                clear_console() # TODO все эти clear console вынести в следующие за ними функции?
                ch.print_back_to_main_menu()
                break
            else:
                clear_console()
                ch.print_invalid_command()
                continue

    elif command == "nearby" or command == "3": # TODO ДОБАВИТЬ ПОИСК ПО ЛЮБОМУ ПУНКТУ МЕНЮ + радиус задается пользователем (и писать стандартное значение)!
        ch.print_command("nearby [3]")
        while True:
            zip = input("Enter zip: ").strip() # todo подумать вынести ли принт отдельно и тут оставить только инпут?
            if zip == "q":
                clear_console()
                break
            elif len(zip) != 5 or not zip.isdigit(): # TODO добавить описание для q на этом уровне
                clear_console()
                ch.print_invalid_zip()
                continue
            clear_console()
            dh.search_nearby_markets(zip)
            break

    else:
        clear_console()
        ch.print_command(command)
        ch.print_invalid_command()
        ch.print_newline()


def get_distance(lat1, lon1, lat2, lon2):
    '''
    @requires: lat1, lon1, lat2, lon2 are float coordinates in decimal degrees
               uses Haversine formula for spherical Earth
    @modifies: None
    @effects:  calculates great-circle distance between two geographic points
    @returns:  float distance in miles (Earth radius = 3959 miles)
    '''
    R = 3959
    lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
    c = 2 * asin(sqrt(a))
    return R * c

