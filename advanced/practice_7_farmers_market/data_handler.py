from csv_utils import read_csv_file
from csv_utils import MarketsIndex as idx
from csv_utils import State as s
import utils as u
import console_handler as ch
markets_db = read_csv_file()


def get_page(print_function, markets_base, **kwargs): # todo подумать как разбить на более мелкие
    s.current_page = 0 # todo возможно нам класс и не нужен этот? просто сюда перенести все, до начала цикла
    while True:
        u.clear_console()

        start = s.current_page * s.page_size # TODO добавить возможность в консоли менять отображение записей на странице из ряда стандартных значений
        end = start + s.page_size
        page = markets_base[start:end]

        total_page = (len(markets_base) + s.page_size - 1) // s.page_size

        if 'len_base' in kwargs:
            len_base = kwargs.get('len_base')

        if print_function == "print_market_page":
            for i, market in enumerate(page, start=start+1):
                ch.print_market_page(i, market) # TODO добавить еще вывод отзывов и рейтингов
        if print_function == "print_market_found_nearby":
            zip_code = kwargs.get('zip_code')
            ch.print_count_market_found_nearby(len_base, zip_code)
            for i, market in enumerate(page, start=start+1):
                ch.print_market_found_nearby(i, market)
        if print_function == "print_markets_list":
            if 'city' in kwargs:
                city = kwargs.get('city')
                state = kwargs.get('state')
                ch.print_count_market_found_by_city_state(len_base, city, state)
            if 'zip_code' in kwargs:
                zip_code = kwargs.get('zip_code')
                ch.print_count_market_found_by_zip(len_base, zip_code)
            for i, market in enumerate(page, start=start+1):
                ch.print_markets_list(i, market)

        ch.print_pagination(total_page)
        ch.print_pagination_description()

        user_cmd = input("> ").strip().lower()
        if user_cmd == 'n' and s.current_page < total_page - 1: # todo добавить валидацию команд
            s.current_page += 1
        elif user_cmd == 'p' and s.current_page > 0:
            s.current_page -= 1
        elif user_cmd == 'q':
            u.clear_console()
            break  # TODO добавить возможность навигации к конкретной странице?
        elif user_cmd.isdigit():
            view_market_details(int(user_cmd), markets_base)


def search_by_city_state(city, state):
    results = []
    for market in markets_db:
        if market[idx.CITY] == city and market[idx.STATE] == state:
            results.append({
                'fmid': market[idx.FMID],
                'name': market[idx.MARKET_NAME],
                'zip': market[idx.ZIP],
                'website': market[idx.WEBSITE] # TODO наверное и сюда включить отзывы и рейтинги
            })
    if not results:
        ch.print_market_not_found()
    else:
        get_page("print_markets_list", markets_base=results, len_base=len(results), city=city, state=state)


def search_by_zip(zip_code):
    results = []
    for market in markets_db:
        if market[idx.ZIP] == zip_code:
            results.append({
                'fmid': market[idx.FMID],
                'name': market[idx.MARKET_NAME],
                'city': market[idx.CITY],
                'state': market[idx.STATE],
                'website': market[idx.WEBSITE] # TODO наверное и сюда включить отзывы и рейтинги
            })
    if not results:
        ch.print_market_not_found()
    else:
        get_page("print_markets_list", markets_base=results, len_base=len(results), zip_code=zip_code)


def search_nearby_markets(zip_code, max_miles=30):
    results = []
    center_market = None
    for market in markets_db:
        if market[idx.ZIP] == zip_code:
            center_market = market
            break
    if not center_market:
        ch.print_market_not_found()
        return

    center_lat = float(center_market[idx.Y])
    center_lon = float(center_market[idx.X])

    for market in markets_db:
        if not market[idx.Y] or not market[idx.X]:
            continue

        market_lat = float(market[idx.Y])
        market_lon = float(market[idx.X])

        distance = u.get_distance(center_lat, center_lon, market_lat, market_lon)

        if distance <= max_miles:
            results.append({
                'fmid': market[idx.FMID],
                'name': market[idx.MARKET_NAME],
                'city': market[idx.CITY],
                'state': market[idx.STATE],
                'website': market[idx.WEBSITE],
                'zip': market[idx.ZIP],
                'distance': round(distance, 1)
            })

    results.sort(key=lambda x: x['distance'])
    get_page("print_market_found_nearby", markets_base=results, len_base=len(results), zip_code=zip_code)


def view_market_details(user_cmd, markets_base):
    u.clear_console()
    results = {}
    while True:
        for market in markets_db:
            if market[idx.FMID] == markets_base[user_cmd-1]['fmid']:
                for field in idx:
                    results[field.name] = market[field.value]
                break
        if not results:
            ch.details_not_found()
        else:
            ch.print_detail_information(results)
            ch.print_detail_description()
            user_input = input("> ")
            if user_input == "q":
                break
            if user_cmd == "c":
                break # TODO доделать


def search_all_markets():
    results = []
    for market in markets_db:
        if not market[idx.MARKET_NAME]:
            continue
        results.append({
            'name': market[idx.MARKET_NAME],
            'fmid': market[idx.FMID]
        })
    results.sort(key=lambda x: x['name'])
    get_page("print_market_page", markets_base=results)
