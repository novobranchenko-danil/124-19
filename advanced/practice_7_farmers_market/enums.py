from enum import IntEnum, StrEnum, Enum


class ReviewsIndex(IntEnum):
    FMID = 0
    MARKET_NAME = 1
    ZIP = 2
    COMMENT = 3
    RATING = 4
    USER = 5
    DATE = 6


class Menu:
    """Все меню приложения"""

    class Main(StrEnum):
        LOGIN_REGISTER = "1"
        MARKETS = "2"
        SEARCH = "3"
        NEARBY = "4"
        HELP = "5"
        EXIT = "q"

    class Search(StrEnum):
        FMID = "1"
        MARKET_NAME = "2"
        CITY_STATE = "3"
        ZIP = "4"
        BACK = "q"

    class Auth(StrEnum):
        REGISTER = "1"
        LOGIN = "2"
        BACK = "q"

    class Pagination(StrEnum):
        NEXT_PAGE = "n"
        PREVIOUS_PAGE = "p"
        BACK = "q"

    class Details(StrEnum):
        COMMENT = "c"
        VIEW_REVIEW = "v"
        DELETE = "d"
        BACK = "q"

    class Reviews(StrEnum):
        DELETE = "d"


class MarketIndex(IntEnum):
    # ===== ОСНОВНАЯ ИНФОРМАЦИЯ =====
    FMID = 0  # ID рынка (уникальный идентификатор)
    MARKET_NAME = 1  # Название рынка

    # ===== СОЦИАЛЬНЫЕ СЕТИ И КОНТАКТЫ =====
    WEBSITE = 2  # Вебсайт
    FACEBOOK = 3  # Facebook
    TWITTER = 4  # Twitter
    YOUTUBE = 5  # YouTube
    OTHER_MEDIA = 6  # Другие медиа

    # ===== АДРЕС =====
    STREET = 7  # Улица
    CITY = 8  # Город
    COUNTY = 9  # Округ
    STATE = 10  # Штат
    ZIP = 11  # Почтовый индекс

    # ===== СЕЗОНЫ РАБОТЫ =====
    SEASON1_DATE = 12  # Даты сезона 1
    SEASON1_TIME = 13  # Время сезона 1
    SEASON2_DATE = 14  # Даты сезона 2
    SEASON2_TIME = 15  # Время сезона 2
    SEASON3_DATE = 16  # Даты сезона 3
    SEASON3_TIME = 17  # Время сезона 3
    SEASON4_DATE = 18  # Даты сезона 4
    SEASON4_TIME = 19  # Время сезона 4

    # ===== ГЕОГРАФИЯ =====
    X = 20  # Координата X (долгота)
    Y = 21  # Координата Y (широта)
    LOCATION = 22  # Локация (описание)

    # ===== МЕТОДЫ ОПЛАТЫ =====
    CREDIT = 23  # Принимают кредитные карты (Y/N)
    WIC = 24  # Принимают WIC (Women, Infants, Children)
    WIC_CASH = 25  # Принимают WIC cash
    SFMNP = 26  # Senior Farmers' Market Nutrition Program
    SNAP = 27  # Принимают SNAP (фуд-стемпы)

    # ===== ОРГАНИЧЕСКИЕ ПРОДУКТЫ =====
    ORGANIC = 28  # Органические продукты (Y/N)

    # ===== ТИПЫ ПРОДУКТОВ =====
    BAKED_GOODS = 29  # Выпечка
    CHEESE = 30  # Сыр
    CRAFTS = 31  # Ремесленные изделия
    FLOWERS = 32  # Цветы
    EGGS = 33  # Яйца
    SEAFOOD = 34  # Морепродукты
    HERBS = 35  # Травы
    VEGETABLES = 36  # Овощи
    HONEY = 37  # Мед
    JAMS = 38  # Варенье, джемы
    MAPLE = 39  # Кленовый сироп
    MEAT = 40  # Мясо
    NURSERY = 41  # Саженцы, рассада
    NUTS = 42  # Орехи
    PLANTS = 43  # Растения
    POULTRY = 44  # Птица
    PREPARED = 45  # Готовая еда
    SOAP = 46  # Мыло
    TREES = 47  # Деревья
    WINE = 48  # Вино
    COFFEE = 49  # Кофе
    BEANS = 50  # Бобы
    FRUITS = 51  # Фрукты
    GRAINS = 52  # Зерновые
    JUICES = 53  # Соки
    MUSHROOMS = 54  # Грибы
    PET_FOOD = 55  # Корм для животных
    TOFU = 56  # Тофу
    WILD_HARVESTED = 57  # Дикорастущие продукты

    # ===== ДАТА ОБНОВЛЕНИЯ =====
    UPDATE_TIME = 58  # Время последнего обновления