import console_handler as ch
import csv_utils as csv


def get_page(page_function, markets_base, current_page=0, page_size=10, **kwargs):
    ch.clear_console()
    while True:
        start = current_page * page_size
        end = start + page_size
        page = markets_base[start:end]

        total_page = (len(markets_base) + page_size - 1) // page_size

        if page_function == "markets_list":
            page_markets_list(page, start)

        if page_function == "search" or page_function == "nearby":
            page_search_and_nearby(page_function, page, start, **kwargs)

        if page_function == "reviews":
            page_reviews(page, start, **kwargs)

        ch.print_pagination(total_page, current_page)
        ch.print_pagination_description()

        user_input = input("> ").strip().lower()
        if user_input == 'n' and current_page < total_page - 1:
            ch.clear_console()
            current_page += 1
        elif user_input == 'p' and current_page > 0:
            ch.clear_console()
            current_page -= 1
        elif user_input == 'q':
            ch.clear_console()
            break
        elif user_input.isdigit():
            csv.view_market_details(int(user_input), markets_base)
        else:
            ch.clear_console()
            ch.print_command(user_input)
            ch.print_invalid_command()
            ch.print_newline()


def page_reviews(page, start, **kwargs):
    len_base = kwargs.get('len_base')
    fmid = kwargs.get('fmid')
    market_name = kwargs.get('market_name')

    ch.print_count_market_reviews(len_base, fmid, market_name)
    for i, review in enumerate(page, start=start + 1):
        ch.print_reviews(i, review) # TODO можно так разбить


def page_search_and_nearby(search_type, page, start, **kwargs):
    len_base = kwargs.get('len_base')

    if search_type == "nearby":
        nearby = True
    else:
        nearby = False

    if 'city' in kwargs:
        city = kwargs.get('city')
        state = kwargs.get('state')
        ch.print_count_market_found_by_city_state(len_base, city, state, nearby)
    if 'zip_code' in kwargs:
        zip_code = kwargs.get('zip_code')
        ch.print_count_market_found_by_zip(len_base, zip_code, nearby)
    if 'fmid' in kwargs:
        user_fmid = kwargs.get('fmid')
        ch.print_count_market_found_by_fmid(len_base, user_fmid, nearby)
    if 'market_name' in kwargs:
        user_mn = kwargs.get('market_name')
        ch.print_count_market_found_by_market_name(len_base, user_mn, nearby)
    for i, market in enumerate(page, start=start + 1):
        ch.print_market_list_wrapper(search_type, i, market)


def page_markets_list(page, start):
    for i, market in enumerate(page, start=start + 1):
        ch.print_market_page(i, market)







