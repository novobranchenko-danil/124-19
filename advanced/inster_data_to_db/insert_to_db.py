import psycopg2
from psycopg2.extras import execute_values
from csv_parsing import *


def insert_data_to_db(data, db_config):
    """
    Вставляет данные из словаря data в базу PostgreSQL
    db_config: словарь с параметрами подключения
    """

    # Подключаемся к БД
    conn = psycopg2.connect(**db_config)
    cursor = conn.cursor()
    cursor.execute("SET datestyle = 'ISO, MDY';")

    try:
        # =====================================================
        # 1. Заполняем справочники (города, округа, штаты)
        # =====================================================
        print("Заполняем города...")
        for city in data['cities']:
            cursor.execute(
                "INSERT INTO City (city_name) VALUES (%s) ON CONFLICT (city_name) DO NOTHING",
                (city,)
            )

        print("Заполняем округа...")
        for county in data['counties']:
            cursor.execute(
                "INSERT INTO County (county_name) VALUES (%s) ON CONFLICT (county_name) DO NOTHING",
                (county,)
            )

        print("Заполняем штаты...")
        for state in data['states']:
            cursor.execute(
                "INSERT INTO State (state_name) VALUES (%s) ON CONFLICT (state_name) DO NOTHING",
                (state,)
            )

        # Сохраняем, чтобы получить ID для следующих шагов
        conn.commit()

        # =====================================================
        # 2. Получаем ID для городов/округов/штатов (кешируем)
        # =====================================================
        print("Кешируем ID справочников...")

        # Города
        city_cache = {}
        cursor.execute("SELECT city_id, city_name FROM City")
        for city_id, city_name in cursor.fetchall():
            city_cache[city_name] = city_id

        # Округа
        county_cache = {}
        cursor.execute("SELECT county_id, county_name FROM County")
        for county_id, county_name in cursor.fetchall():
            county_cache[county_name] = county_id

        # Штаты
        state_cache = {}
        cursor.execute("SELECT state_id, state_name FROM State")
        for state_id, state_name in cursor.fetchall():
            state_cache[state_name] = state_id

        # =====================================================
        # 3. Заполняем Zip_codes
        # =====================================================
        print("Заполняем почтовые индексы...")
        zip_data = []
        for zip_code, (city_name, county_name, state_name, lat, lon) in data['zip_codes'].items():
            zip_data.append((
                zip_code,
                city_cache[city_name],
                county_cache[county_name],
                state_cache[state_name],
                float(lat) if lat else None,
                float(lon) if lon else None
            ))

        execute_values(
            cursor,
            """
            INSERT INTO Zip_codes (zip, city_id, county_id, state_id, latitude, longitude)
            VALUES %s
            ON CONFLICT (zip) DO NOTHING
            """,
            zip_data
        )

        # =====================================================
        # 4. Заполняем Markets
        # =====================================================
        print("Заполняем рынки...")
        market_data = [
            (fmid, name, zip_code, street, location, update_time)
            for fmid, name, zip_code, street, location, update_time in data['markets']
        ]

        execute_values(
            cursor,
            """
            INSERT INTO Markets (fmid, market_name, zip, street, location, update_time)
            VALUES %s
            ON CONFLICT (fmid) DO NOTHING
            """,
            market_data
        )

        # =====================================================
        # 5. Заполняем Market_contacts
        # =====================================================
        print("Заполняем контакты...")
        contacts_data = [
            (fmid, website, fb, twitter, youtube, other)
            for fmid, website, fb, twitter, youtube, other in data['market_contacts']
        ]

        execute_values(
            cursor,
            """
            INSERT INTO Market_contacts (fmid, website, facebook, twitter, youtube, other_media)
            VALUES %s
            ON CONFLICT (fmid) DO NOTHING
            """,
            contacts_data
        )

        # =====================================================
        # 6. Заполняем Services (справочник услуг)
        # =====================================================
        print("Заполняем услуги...")
        for service in data['services']:
            cursor.execute(
                "INSERT INTO Services (service_name) VALUES (%s) ON CONFLICT (service_name) DO NOTHING",
                (service,)
            )

        # Кешируем ID услуг
        service_cache = {}
        cursor.execute("SELECT service_id, service_name FROM Services")
        for service_id, service_name in cursor.fetchall():
            service_cache[service_name] = service_id

        # =====================================================
        # 7. Заполняем Market_services
        # =====================================================
        print("Заполняем связи рынков с услугами...")
        market_service_data = [
            (fmid, service_cache[service_name], available)
            for fmid, service_name, available in data['market_services']
        ]

        execute_values(
            cursor,
            """
            INSERT INTO Market_services (fmid, service_id, is_available)
            VALUES %s
            ON CONFLICT (fmid, service_id) DO NOTHING
            """,
            market_service_data
        )

        # =====================================================
        # 8. Заполняем Product_type (справочник продуктов)
        # =====================================================
        print("Заполняем продукты...")
        # Сначала категории (если их нет)
        categories = ['food', 'beverages', 'crafts', 'plants']
        category_cache = {}
        for cat in categories:
            cursor.execute(
                "INSERT INTO Product_category (category_name) VALUES (%s) ON CONFLICT (category_name) DO NOTHING",
                (cat,)
            )

        cursor.execute("SELECT category_id, category_name FROM Product_category")
        for cat_id, cat_name in cursor.fetchall():
            category_cache[cat_name] = cat_id

        # Вставляем продукты (все в food для простоты)
        for product in data['products']:
            cursor.execute(
                """
                INSERT INTO Product_type (product_name, localized_name, category_id)
                VALUES (%s, %s, %s)
                ON CONFLICT (product_name) DO NOTHING
                """,
                (product, None, category_cache['food'])
            )

        # Кешируем ID продуктов
        product_cache = {}
        cursor.execute("SELECT product_id, product_name FROM Product_type")
        for prod_id, prod_name in cursor.fetchall():
            product_cache[prod_name] = prod_id

        # =====================================================
        # 9. Заполняем Market_product
        # =====================================================
        print("Заполняем связи рынков с продуктами...")
        market_product_data = [
            (fmid, product_cache[product_name], is_organic)
            for fmid, product_name, is_organic in data['market_products']
        ]

        execute_values(
            cursor,
            """
            INSERT INTO Market_product (fmid, product_id, is_organic)
            VALUES %s
            ON CONFLICT (fmid, product_id) DO NOTHING
            """,
            market_product_data
        )

        # =====================================================
        # 10. Заполняем Market_seasons
        # =====================================================
        print("Заполняем сезоны...")
        execute_values(
            cursor,
            """
            INSERT INTO Market_seasons (
                fmid, season1_date, season1_time, season2_date, season2_time,
                season3_date, season3_time, season4_date, season4_time
            )
            VALUES %s
            ON CONFLICT (fmid) DO NOTHING
            """,
            data['market_seasons']
        )

        # Сохраняем все изменения
        conn.commit()
        print(f"✅ Данные успешно загружены!")

        # Статистика
        cursor.execute("SELECT COUNT(*) FROM Markets")
        markets_count = cursor.fetchone()[0]
        print(f"📊 Загружено рынков: {markets_count}")

    except Exception as e:
        conn.rollback()
        print(f"❌ Ошибка: {e}")
        raise
    finally:
        cursor.close()
        conn.close()


# =====================================================
# Использование
# =====================================================
if __name__ == "__main__":
    # Сначала парсим CSV
    csv_file = "Export.csv"
    data = parse_csv_to_dicts(csv_file)

    print(f"Найдено в CSV:")
    print(f"- Городов: {len(data['cities'])}")
    print(f"- Рынков: {len(data['markets'])}")
    print(f"- Продуктов: {len(data['products'])}")
    print()

    # Настройки подключения к PostgreSQL
    db_config = {
        'host': 'localhost',
        'port': 5432,
        'database': 'farmers_market',
        'user': 'mugiwara',  # твой пользователь
        'password': 'pMeowth1cat'  # введи свой пароль
    }

    # Загружаем данные в БД
    insert_data_to_db(data, db_config)
