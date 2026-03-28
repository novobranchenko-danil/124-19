import psycopg2
from psycopg2.extras import RealDictCursor
from typing import List, Dict, Any, Optional, Tuple


class Database:
    """Класс для работы с базой данных фермерских рынков"""

    def __init__(self, config: Dict[str, str]):

        self.config = config
        self.conn = None

    def connect(self):
        """Устанавливает соединение с БД"""
        if not self.conn or self.conn.closed:
            self.conn = psycopg2.connect(**self.config)
        return self.conn

    def close(self):
        """Закрывает соединение"""
        if self.conn and not self.conn.closed:
            self.conn.close()

    def _execute(self, query: str, params: tuple = None, fetch_one: bool = False) -> Any:
        """Выполняет запрос и возвращает результат"""
        with self.connect() as conn:
            with conn.cursor(cursor_factory=RealDictCursor) as cursor:
                cursor.execute(query, params or ())
                if fetch_one:
                    return cursor.fetchone()
                return cursor.fetchall()

    # =========================================================
    # 1. ВСЕ РЫНКИ (постранично, 10 на страницу)
    # =========================================================

    def get_all_markets(self, page: int = 0, per_page: int = 10) -> Tuple[List[Dict], int]:
        """
        Возвращает список рынков и общее количество
        page: номер страницы (0 - первая)
        per_page: 10 на страницу

        Поля: fmid, market_name, avg_rating
        """
        offset = page * per_page

        total = self._execute("SELECT COUNT(*) as count FROM markets", fetch_one=True)['count']

        query = """
            SELECT 
                m.fmid,
                m.market_name,
                COALESCE(AVG(r.rating), NULL) as avg_rating
            FROM markets m
            LEFT JOIN reviews r ON m.fmid = r.fmid
            GROUP BY m.fmid, m.market_name
            ORDER BY m.fmid
            LIMIT %s OFFSET %s
        """
        markets = self._execute(query, (per_page, offset))

        return markets, total

    # =========================================================
    # 2. ДЕТАЛИЗАЦИЯ (все поля по конкретному рынку)
    # =========================================================

    def get_market_details(self, fmid: int) -> Optional[Dict]:
        """Все поля по конкретному рынку"""
        query = """
            SELECT 
                m.fmid,
                m.market_name,
                c.city_name as city,
                s.state_name as state,
                co.county_name as county,
                z.zip,
                m.street,
                m.location,
                z.latitude,
                z.longitude,
                mc.website,
                mc.facebook,
                mc.twitter,
                mc.youtube,
                mc.other_media,
                ms.season1_date,
                ms.season1_time,
                ms.season2_date,
                ms.season2_time,
                ms.season3_date,
                ms.season3_time,
                ms.season4_date,
                ms.season4_time,
                m.update_time,
                COALESCE(AVG(r.rating), NULL) as avg_rating
            FROM markets m
            LEFT JOIN zip_codes z ON m.zip = z.zip
            LEFT JOIN city c ON z.city_id = c.city_id
            LEFT JOIN county co ON z.county_id = co.county_id
            LEFT JOIN state s ON z.state_id = s.state_id
            LEFT JOIN market_contacts mc ON m.fmid = mc.fmid
            LEFT JOIN market_seasons ms ON m.fmid = ms.fmid
            LEFT JOIN reviews r ON m.fmid = r.fmid
            WHERE m.fmid = %s
            GROUP BY m.fmid, z.zip, c.city_name, co.county_name, s.state_name,
                     mc.website, mc.facebook, mc.twitter, mc.youtube, mc.other_media,
                     ms.season1_date, ms.season1_time, ms.season2_date, ms.season2_time,
                     ms.season3_date, ms.season3_time, ms.season4_date, ms.season4_time
        """
        return self._execute(query, (fmid,), fetch_one=True)

    # =========================================================
    # 3. ОТЗЫВЫ (постранично, 1 отзыв на страницу)
    # =========================================================

    def get_reviews(self, fmid: int, page: int = 0, per_page: int = 1) -> Tuple[List[Dict], int]:
        """
        Возвращает отзывы о рынке и общее количество
        page: номер страницы (0 - первая)
        per_page: 1 отзыв на страницу

        Поля: fmid, market_name, zip, comment, rating, username, review_date
        """
        offset = page * per_page

        total = self._execute(
            "SELECT COUNT(*) as count FROM reviews WHERE fmid = %s",
            (fmid,), fetch_one=True
        )['count']

        query = """
            SELECT 
                r.fmid,
                m.market_name,
                z.zip,
                r.comment,
                r.rating,
                r.username,
                r.review_date
            FROM reviews r
            JOIN markets m ON r.fmid = m.fmid
            LEFT JOIN zip_codes z ON m.zip = z.zip
            WHERE r.fmid = %s
            ORDER BY r.review_date DESC
            LIMIT %s OFFSET %s
        """
        reviews = self._execute(query, (fmid, per_page, offset))

        return reviews, total

    # =========================================================
    # 8. ДОБАВЛЕНИЕ ОТЗЫВА
    # =========================================================

    def add_review(self, fmid: int, username: str, rating: int, comment: str) -> bool:
        """Добавляет отзыв о рынке"""
        try:
            with self.connect() as conn:
                with conn.cursor() as cursor:
                    cursor.execute("""
                        INSERT INTO reviews (fmid, username, rating, comment, review_date)
                        VALUES (%s, %s, %s, %s, CURRENT_TIMESTAMP)
                    """, (fmid, username, rating, comment))
                    conn.commit()
                    return True
        except Exception as e:
            print(f"Ошибка при добавлении отзыва: {e}")
            if self.conn:
                self.conn.rollback()
            return False

    # =========================================================
    # 8. поиск nearby универсальный
    # =========================================================

    def search_nearby(self, fmid: int = None, name: str = None,
                      city: str = None, state: str = None,
                      zip_code: str = None, radius_miles: int = 30) -> List[Dict]:
        """
        Поиск рынков в радиусе radius_miles миль от указанной точки.
        Точка задаётся одним из параметров:
            - fmid: FMID рынка
            - zip_code: ZIP-код
            - name: название рынка (первый найденный)
            - city + state: город и штат

        Возвращает список рынков с полями:
            fmid, market_name, state, city, zip, website, avg_rating, distance
        """

        # Определяем CTE в зависимости от параметра
        if fmid is not None:
            center_cte = """
                WITH center AS (
                    SELECT z.latitude AS lat, z.longitude AS lon
                    FROM markets m
                    JOIN zip_codes z ON m.zip = z.zip
                    WHERE m.fmid = %s
                )
            """
            center_params = [fmid]

        elif zip_code is not None:
            center_cte = """
                WITH center AS (
                    SELECT latitude AS lat, longitude AS lon
                    FROM zip_codes
                    WHERE zip = %s
                )
            """
            center_params = [zip_code]

        elif name is not None:
            center_cte = """
                WITH center AS (
                    SELECT z.latitude AS lat, z.longitude AS lon
                    FROM markets m
                    JOIN zip_codes z ON m.zip = z.zip
                    WHERE m.market_name ILIKE %s
                    LIMIT 1
                )
            """
            center_params = [f'%{name}%']

        elif city is not None and state is not None:
            center_cte = """
                WITH center AS (
                    SELECT z.latitude AS lat, z.longitude AS lon
                    FROM zip_codes z
                    JOIN city c ON z.city_id = c.city_id
                    JOIN state s ON z.state_id = s.state_id
                    WHERE c.city_name ILIKE %s AND s.state_name ILIKE %s
                    LIMIT 1
                )
            """
            center_params = [f'%{city}%', f'%{state}%']

        else:
            raise ValueError(
                "Должен быть указан один из параметров: fmid, zip_code, name, или city+state")

        # Основной запрос
        query = center_cte + """
            SELECT 
                m.fmid,
                m.market_name,
                s.state_name as state,
                c.city_name as city,
                z.zip,
                mc.website,
                COALESCE(AVG(r.rating), NULL) as avg_rating,
                ROUND((
                    3959 * acos(
                        cos(radians(center.lat)) * cos(radians(z.latitude)) *
                        cos(radians(z.longitude) - radians(center.lon)) +
                        sin(radians(center.lat)) * sin(radians(z.latitude))
                    )
                )::numeric, 2) AS distance
            FROM markets m
            JOIN zip_codes z ON m.zip = z.zip
            CROSS JOIN center
            LEFT JOIN city c ON z.city_id = c.city_id
            LEFT JOIN state s ON z.state_id = s.state_id
            LEFT JOIN market_contacts mc ON m.fmid = mc.fmid
            LEFT JOIN reviews r ON m.fmid = r.fmid
            WHERE 
                3959 * acos(
                    cos(radians(center.lat)) * cos(radians(z.latitude)) *
                    cos(radians(z.longitude) - radians(center.lon)) +
                    sin(radians(center.lat)) * sin(radians(z.latitude))
                ) <= %s
            GROUP BY m.fmid, s.state_name, c.city_name, z.zip, mc.website, 
                     z.latitude, z.longitude, center.lat, center.lon
            ORDER BY distance
        """

        params = center_params + [radius_miles]
        return self._execute(query, tuple(params))

    def search_markets(self, fmid: int = None, name: str = None,
                       city: str = None, state: str = None,
                       zip_code: str = None) -> List[Dict]:
        """
        Универсальный поиск рынков по одному из параметров:
            - fmid: точное совпадение (возвращает 1 рынок)
            - name: частичное совпадение по названию
            - city + state: поиск по городу и/или штату
            - zip_code: точное совпадение по ZIP

        Возвращает список рынков с полями:
            fmid, market_name, state, city, zip, website, avg_rating
        """
        where_clauses = []
        params = []

        # Определяем тип поиска
        if fmid is not None:
            where_clauses.append("m.fmid = %s")
            params.append(fmid)

        elif name is not None:
            where_clauses.append("m.market_name ILIKE %s")
            params.append(f'%{name}%')

        elif zip_code is not None:
            where_clauses.append("m.zip = %s")
            params.append(zip_code)

        elif city is not None or state is not None:
            if city:
                where_clauses.append("c.city_name ILIKE %s")
                params.append(f'%{city}%')
            if state:
                where_clauses.append("s.state_name ILIKE %s")
                params.append(f'%{state}%')

        else:
            raise ValueError("Должен быть указан хотя бы один параметр поиска")

        where_sql = " AND ".join(where_clauses)

        query = f"""
            SELECT 
                m.fmid,
                m.market_name,
                s.state_name as state,
                c.city_name as city,
                z.zip,
                mc.website,
                COALESCE(AVG(r.rating), NULL) as avg_rating
            FROM markets m
            LEFT JOIN zip_codes z ON m.zip = z.zip
            LEFT JOIN city c ON z.city_id = c.city_id
            LEFT JOIN state s ON z.state_id = s.state_id
            LEFT JOIN market_contacts mc ON m.fmid = mc.fmid
            LEFT JOIN reviews r ON m.fmid = r.fmid
            WHERE {where_sql}
            GROUP BY m.fmid, s.state_name, c.city_name, z.zip, mc.website
            ORDER BY m.market_name
        """

        # Для поиска по FMID может быть только один результат
        if fmid is not None:
            return self._execute(query, tuple(params), fetch_one=True)
        return self._execute(query, tuple(params))
