import csv
import console_handler as ch
from authorization import Username
from datetime import datetime
import data_handler as dh
from enums import MarketIndex as idx
from enums import ReviewsIndex
import authorization as auth


def get_reviews():
    with open('reviews.csv', 'r', encoding='utf-8') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        next(csv_reader)
        return [[field.strip() for field in row] for row in csv_reader]


def write_comment(market_detail):
    fmid = market_detail[idx.FMID.name]
    market_name = market_detail[idx.MARKET_NAME.name]
    zip = market_detail[idx.ZIP.name]
    date = datetime.now().strftime("%d.%m.%Y %H:%M:%S")

    ch.clear_console()
    ch.print_comment_instructions(fmid, market_name)

    ch.print_comment_prompt()
    comment = input().strip()
    if comment == "q":
        ch.clear_console()
        return

    ch.print_rating_prompt()
    while True:
        rating = input().strip()
        if rating == "q":
            ch.clear_console()
            return
        if not rating.isdigit():
            ch.print_invalid_input()
            continue
        if not (1 <= int(rating) <= 5):
            ch.print_invalid_rating()
            continue

        break

    with open("reviews.csv", "a", newline="", encoding="utf-8") as file:
        writer = csv.writer(file, delimiter=',')
        writer.writerow((fmid, market_name, zip, comment, rating, Username.username, date))

    ch.clear_console()
    ch.print_review_saved()


def get_avg_rating(fmid):
    rating_list = []
    for row in get_reviews():
        if fmid == row[ReviewsIndex.FMID]:
            rating_list.append(int(row[ReviewsIndex.RATING]))
    if rating_list:
        average = sum(rating_list) / len(rating_list)
        return round(average, 1)
    else:
        return


def view_reviews_markets(fmid, market_name):
    ch.clear_console()
    ch.print_view_reviews_prompt(fmid, market_name)
    ch.print_newline()
    review_list = []
    for row in get_reviews():
        if fmid == row[ReviewsIndex.FMID]:
            review_list.append({
                'fmid': row[ReviewsIndex.FMID],
                'market_name': row[ReviewsIndex.MARKET_NAME],
                'zip': row[ReviewsIndex.ZIP],
                'comment': row[ReviewsIndex.COMMENT],
                'rating': row[ReviewsIndex.RATING],
                'user': row[ReviewsIndex.USER],
                'date': row[ReviewsIndex.DATE]
            })
    if review_list:
        review_list.sort(key=lambda x: x['rating'], reverse=True)
        dh.get_page("reviews", markets_base=review_list, page_size=1,
                    len_base=len(review_list), fmid=fmid, market_name=market_name)
    else:
        ch.clear_console()
        ch.print_reviews_not_found()
        ch.print_newline()


def delete_review(market_base, current_page, csv_filename='reviews.csv'):
    if not auth.authorization():
        return False
    if market_base[current_page]['user'] != Username.username:
        ch.clear_console()
        ch.print_delete_review_failed()
        ch.print_newline()
        return False

    review = market_base[current_page]

    del market_base[current_page]

    with open(csv_filename, 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        header = next(reader)
        rows = [row for row in reader
                if not (row[header.index('date')] == review['date']
                        and row[header.index('FMID')] == review['fmid'])]

    with open(csv_filename, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(header)
        writer.writerows(rows)

    return market_base
