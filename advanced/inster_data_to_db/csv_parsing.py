import csv


def parse_csv_to_dicts(csv_file):
    """Читает CSV и собирает данные в словари/множества"""

    data = {
        'cities': set(),
        'counties': set(),
        'states': set(),
        'zip_codes': {},  # ключ: zip, значение: (city, county, state, lat, lon)
        'products': set(),
        'services': {'Credit', 'WIC', 'WICcash', 'SFMNP', 'SNAP'},  # базовый набор услуг
        'markets': [],  # список кортежей для Markets
        'market_services': [],  # список (fmid, service_name, is_available)
        'market_products': [],  # список (fmid, product_name, organic)
        'market_contacts': [],  # список (fmid, website, facebook, twitter, youtube, other)
        'market_seasons': [],  # список (fmid, s1date, s1time, s2date, s2time, s3date, s3time, s4date, s4time)

    }

    # Все возможные продукты (Y/N поля в CSV)
    product_fields = [
        'Bakedgoods', 'Cheese', 'Crafts', 'Flowers', 'Eggs', 'Seafood', 'Herbs',
        'Vegetables', 'Honey', 'Jams', 'Maple', 'Meat', 'Nursery', 'Nuts', 'Plants',
        'Poultry', 'Prepared', 'Soap', 'Trees', 'Wine', 'Coffee', 'Beans', 'Fruits',
        'Grains', 'Juices', 'Mushrooms', 'PetFood', 'Tofu', 'WildHarvested', 'Organic'
    ]
    # 'Organic' — особый случай, он в Market_product

    with open(csv_file, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)

        for row in reader:
            # --- 1. Города, округа, штаты ---
            data['cities'].add(row['city'].strip())
            data['counties'].add(row['County'].strip())
            data['states'].add(row['State'].strip())

            # --- 2. ZIP-коды ---
            zip_code = row['zip'].strip()
            if zip_code and zip_code not in data['zip_codes']:
                data['zip_codes'][zip_code] = (
                    row['city'].strip(),
                    row['County'].strip(),
                    row['State'].strip(),
                    row['y'],  # latitude
                    row['x']  # longitude
                )

            # --- 3. Рынки (основная таблица) ---
            market = (
                int(row['FMID']),
                row['MarketName'].strip(),
                zip_code if zip_code else None,
                row['street'].strip() or None,
                None,  # location (можно сгенерировать из координат)
                row['updateTime'].strip() or None
            )
            data['markets'].append(market)

            # --- 4. Контакты ---
            contact = (
                int(row['FMID']),
                row['Website'].strip() or None,
                row['Facebook'].strip() or None,
                row['Twitter'].strip() or None,
                row['Youtube'].strip() or None,
                row['OtherMedia'].strip() or None
            )
            data['market_contacts'].append(contact)

            # --- СЕЗОНЫ (одна строка на FMID) ---
            seasons = (
                int(row['FMID']),
                row.get('Season1Date', '').strip() or None,
                row.get('Season1Time', '').strip() or None,
                row.get('Season2Date', '').strip() or None,
                row.get('Season2Time', '').strip() or None,
                row.get('Season3Date', '').strip() or None,
                row.get('Season3Time', '').strip() or None,
                row.get('Season4Date', '').strip() or None,
                row.get('Season4Time', '').strip() or None
            )
            data['market_seasons'].append(seasons)

            # --- 5. Услуги (Credit, WIC, ...) ---
            for service in ['Credit', 'WIC', 'WICcash', 'SFMNP', 'SNAP']:
                if row.get(service) == 'Y':
                    data['market_services'].append(
                        (int(row['FMID']), service, True)
                    )

            # --- 6. Продукты (все поля с Y/N) ---
            for product in product_fields:
                if row.get(product) == 'Y':
                    data['products'].add(product)
                    # Для Organic отдельный флаг
                    is_organic = (row.get('Organic') == 'Y')
                    data['market_products'].append(
                        (int(row['FMID']), product, is_organic)
                    )
    return data


if __name__ == "__main__":
    data = parse_csv_to_dicts("Export.csv")
    print(data)
