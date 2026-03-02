import csv
import console_handler as ch
import data_handler as dh
import authorization as auth
import utils as u
import reviews as rw
from enums import MarketIndex as idx


def read_csv_file():
    with open('Export.csv') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        next(csv_reader)
        markets_info = [[field.strip() for field in row] for row in csv_reader]
    return markets_info


def search_market_by_params(search_value, search_type, search_field):
    """
    Поиск рынков по заданным параметрам.

    Args:
        search_value (str or tuple): Значение для поиска:
            - str: для exact/contains (zip, fmid, market_name)
            - tuple: для both (city, state)
        search_type (str): Тип поиска:
            - "exact": точное совпадение
            - "contains": частичное совпадение
            - "both": поиск по двум полям (город + штат)
        search_field (str or tuple): Поле(я) для поиска:
            - str: для exact/contains ("fmid", "zip_code", "market_name")
            - tuple: для both ("state", "city")
    """

    results = []
    field_map = {
        'fmid': idx.FMID,
        'zip_code': idx.ZIP,
        'market_name': idx.MARKET_NAME,
        'state': idx.STATE,
        'city': idx.CITY
    }

    for market in markets_db:
        if search_type == "exact":
            match = market[field_map[search_field]] == search_value
        elif search_type == "contains":
            match = search_value in market[field_map[search_field]]
        elif search_type == "both":
            state, city = search_value
            match = market[field_map[search_field[0]]] == state and market[field_map[search_field[1]]] == city
        else:
            match = False

        if match:
            results.append({
                'fmid': market[idx.FMID],
                'market_name': market[idx.MARKET_NAME],
                'state': market[idx.STATE],
                'city': market[idx.CITY],
                'zip': market[idx.ZIP],
                'website': market[idx.WEBSITE],
                'avg.rating': rw.get_avg_rating(market[idx.FMID])
            })

    if not results:
        ch.clear_console()
        ch.print_market_not_found()
        return

    kwargs = {'len_base': len(results)}
    if search_field == 'fmid':
        kwargs['fmid'] = search_value
        results.sort(key=lambda x: x['fmid'])
    elif search_field == 'market_name':
        kwargs['market_name'] = search_value
        results.sort(key=lambda x: x['market_name'])
    elif search_field == 'zip_code':
        kwargs['zip_code'] = search_value
        results.sort(key=lambda x: x['zip'])
    else:
        kwargs['state'] = state
        kwargs['city'] = city
        results.sort(key=lambda x: x['state'])

    dh.get_page("search", markets_base=results, **kwargs, page_size=5)


def search_nearby_markets(search_value, search_type, search_field, max_miles=30):
    """
    Поиск рынков по заданным параметрам.

    Args:
        search_value (str or tuple): Значение для поиска:
            - str: для exact/contains (zip, fmid, market_name)
            - tuple: для both (city, state)
        search_type (str): Тип поиска:
            - "exact": точное совпадение
            - "contains": частичное совпадение
            - "both": поиск по двум полям (город + штат)
        search_field (str or tuple): Поле(я) для поиска:
            - str: для exact/contains ("fmid", "zip_code", "market_name")
            - tuple: для both ("state", "city")
    """

    results = []
    center_market = None
    field_map = {
        'fmid': idx.FMID,
        'zip_code': idx.ZIP,
        'market_name': idx.MARKET_NAME,
        'state': idx.STATE,
        'city': idx.CITY
    }

    for market in markets_db:
        if search_type == "exact":
            if market[field_map[search_field]] == search_value:
                center_market = market
                break
        elif search_type == "contains":
            if search_value in market[field_map[search_field]]:
                center_market = market
                break
        elif search_type == "both":
            state, city = search_value
            if market[field_map[search_field[0]]] == state and market[field_map[search_field[1]]] == city:
                center_market = market
                break

    if not center_market:
        ch.clear_console()
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
                'market_name': market[idx.MARKET_NAME],
                'city': market[idx.CITY],
                'state': market[idx.STATE],
                'website': market[idx.WEBSITE],
                'zip': market[idx.ZIP],
                'distance': round(distance, 1),
                'avg.rating': rw.get_avg_rating(market[idx.FMID])
            })

    kwargs = {'len_base': len(results)}
    if search_field == 'fmid':
        kwargs['fmid'] = search_value
    elif search_field == 'market_name':
        kwargs['market_name'] = search_value
    elif search_field == 'zip_code':
        kwargs['zip_code'] = search_value
    else:
        kwargs['state'] = state
        kwargs['city'] = city

    results.sort(key=lambda x: x['distance'])
    dh.get_page("nearby", markets_base=results, **kwargs, page_size=5)


def view_market_details(user_cmd, markets_base):
    ch.clear_console()
    results = {}
    while True:
        for market in markets_db:
            if market[idx.FMID] == markets_base[user_cmd - 1]['fmid']:
                for field in idx:
                    results[field.name] = market[field.value]
                break
        if not results:
            ch.details_not_found()
        else:
            average_rating = rw.get_avg_rating(results[idx.FMID.name])
            ch.print_detail_information(results, average_rating)
            ch.print_detail_description()
            user_input = input("> ")
            if user_input == "q":
                ch.clear_console()
                break
            elif user_input == "c":
                if not auth.authorization():
                    continue
                rw.write_comment(results)
            elif user_input == "v":
                rw.view_reviews_markets(results[idx.FMID.name], results[idx.MARKET_NAME.name])
            else:
                ch.clear_console()
                ch.print_command(user_input)
                ch.print_invalid_command()
                ch.print_newline()


def search_all_markets():
    results = []
    for market in markets_db:
        if not market[idx.MARKET_NAME]:
            continue
        results.append({
            'fmid': market[idx.FMID],
            'name': market[idx.MARKET_NAME],
            'avg.rating': rw.get_avg_rating(market[idx.FMID])
        })
    results.sort(key=lambda x: x['name'])
    dh.get_page("markets_list", markets_base=results, page_size=30)


markets_db = read_csv_file()
