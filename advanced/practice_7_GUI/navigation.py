from PySide6.QtWidgets import QMainWindow, QStackedWidget, QTableWidgetItem, QMessageBox
from windows.main_window import Ui_MainWindow as MainWindowUI
from windows.login_register import Ui_MainWindow as LoginRegisterUI
from windows.login import Ui_MainWindow as LoginUI
from windows.register import Ui_MainWindow as RegisterUI

from windows.search import Ui_MainWindow as SearchUI
from windows.search_by_fmid import Ui_MainWindow as SearchByFmidUI
from windows.search_by_market_name import Ui_MainWindow as SearchByNameUI
from windows.search_by_city_state import Ui_MainWindow as SearchByCityStateUI
from windows.search_by_zip import Ui_MainWindow as SearchByZipUI

from windows.search_nearby import Ui_MainWindow as SearchNearbyUI
from windows.search_nearby_fmid import Ui_MainWindow as SearchNearbyFmidUI
from windows.search_nearby_market_name import Ui_MainWindow as SearchNearbyNameUI
from windows.search_nearby_city_state import Ui_MainWindow as SearchNearbyCityStateUI
from windows.search_nearby_zip import Ui_MainWindow as SearchNearbyZipUI

from windows.search_all_market import Ui_MainWindow as AllMarketsUI
from windows.market_result import Ui_MainWindow as MarketResultUI
from windows.market_result_nearby import Ui_MainWindow as MarketResultNearbyUI

from windows.details import Ui_MainWindow as DetailsUI
from windows.leave_review import Ui_MainWindow as LeaveReviewUI
from windows.view_reviews import Ui_MainWindow as ViewReviewsUI
from windows.help import Ui_MainWindow as HelpUI


class MainWindow(QMainWindow):
    def __init__(self, db):
        super().__init__()

        self.last_window = None

        self.setWindowTitle("Farmers Market Base")
        self.setGeometry(100, 100, 500, 754)
        self.setMinimumSize(500, 700)

        # бд
        self.db = db

        # Стек для переключения окон
        self.stack = QStackedWidget()
        self.setCentralWidget(self.stack)

        # Создаём виджеты (каждый со своим UI)
        self.main_menu = MainMenuWidget()
        self.login_register = LoginRegisterWidget()
        self.login = LoginWidget()
        self.register = RegisterWidget()
        self.search = SearchWidget()
        self.search_by_fmid = SearchByFmidWidget()
        self.search_by_name = SearchByNameWidget()
        self.search_by_city_state = SearchByCityStateWidget()
        self.search_by_zip = SearchByZipWidget()
        self.search_nearby = SearchNearbyWidget()
        self.all_markets = AllMarketsWidget(self.db)
        self.market_result = MarketResultWidget()
        self.market_result_nearby = MarketResultNearbyWidget()
        self.details = DetailsWidget()
        self.leave_review = LeaveReviewWidget()
        self.view_reviews = ViewReviewsWidget()
        self.help = HelpWidget()
        self.search_nearby_fmid = SearchNearbyFmidWidget()
        self.search_nearby_name = SearchNearbyNameWidget()
        self.search_nearby_city_state = SearchNearbyCityStateWidget()
        self.search_nearby_zip = SearchNearbyZipWidget()

        # Добавляем в стек
        self.stack.addWidget(self.main_menu)
        self.stack.addWidget(self.login_register)
        self.stack.addWidget(self.login)
        self.stack.addWidget(self.register)
        self.stack.addWidget(self.search)
        self.stack.addWidget(self.search_by_fmid)
        self.stack.addWidget(self.search_by_name)
        self.stack.addWidget(self.search_by_city_state)
        self.stack.addWidget(self.search_by_zip)
        self.stack.addWidget(self.search_nearby)
        self.stack.addWidget(self.all_markets)
        self.stack.addWidget(self.market_result)
        self.stack.addWidget(self.market_result_nearby)
        self.stack.addWidget(self.details)
        self.stack.addWidget(self.leave_review)
        self.stack.addWidget(self.view_reviews)
        self.stack.addWidget(self.help)
        self.stack.addWidget(self.search_nearby_fmid)
        self.stack.addWidget(self.search_nearby_name)
        self.stack.addWidget(self.search_nearby_city_state)
        self.stack.addWidget(self.search_nearby_zip)

        # Подключаем навигацию
        self.main_menu.ui.login_register_button.clicked.connect(self.switch_to_login_register)
        self.main_menu.ui.search_button.clicked.connect(self.switch_to_search)
        self.main_menu.ui.search_nearby_button.clicked.connect(self.switch_to_search_nearby)
        self.main_menu.ui.help_button.clicked.connect(self.switch_to_help)
        self.main_menu.ui.quit_button.clicked.connect(self.close)

        self.login_register.ui.login_button.clicked.connect(self.switch_to_login)
        self.login_register.ui.register_button.clicked.connect(self.switch_to_register)
        self.login_register.ui.back_button.clicked.connect(self.switch_to_main_menu)

        self.login.ui.back_button.clicked.connect(self.switch_to_login_register)
        self.register.ui.back_button.clicked.connect(self.switch_to_login_register)

        self.search.ui.back_button.clicked.connect(self.switch_to_main_menu)
        self.search_by_fmid.ui.back_button.clicked.connect(self.switch_to_search)
        self.search_by_name.ui.back_button.clicked.connect(self.switch_to_search)
        self.search_by_city_state.ui.back_button.clicked.connect(self.switch_to_search)
        self.search_by_zip.ui.back_button.clicked.connect(self.switch_to_search)

        self.search_nearby.ui.back_button.clicked.connect(self.switch_to_main_menu)
        self.search_nearby_fmid.ui.back_button.clicked.connect(self.switch_to_search_nearby)
        self.search_nearby_name.ui.back_button.clicked.connect(self.switch_to_search_nearby)
        self.search_nearby_city_state.ui.back_button.clicked.connect(self.switch_to_search_nearby)
        self.search_nearby_zip.ui.back_button.clicked.connect(self.switch_to_search_nearby)

        self.all_markets.ui.back_button.clicked.connect(self.switch_to_main_menu)
        self.market_result.ui.back_button.clicked.connect(self.switch_to_search)
        self.market_result_nearby.ui.back_button.clicked.connect(self.switch_to_search_nearby)
        self.details.ui.back_button.clicked.connect(self.go_back)
        self.leave_review.ui.back_button.clicked.connect(self.switch_to_details)
        self.view_reviews.ui.back_button.clicked.connect(self.switch_to_details)
        self.help.ui.back_button.clicked.connect(self.switch_to_main_menu)

        # Поисковые кнопки search
        self.search.ui.fmid_button.clicked.connect(self.switch_to_search_by_fmid)
        self.search.ui.market_name_button.clicked.connect(self.switch_to_search_by_name)
        self.search.ui.city_state_button.clicked.connect(self.switch_to_search_by_city_state)
        self.search.ui.zip_button.clicked.connect(self.switch_to_search_by_zip)

        # Поисковые кнопки search nearby
        self.search_nearby.ui.fmid_button.clicked.connect(self.switch_to_search_nearby_fmid)
        self.search_nearby.ui.market_name_button.clicked.connect(self.switch_to_search_nearby_name)
        self.search_nearby.ui.city_state_button.clicked.connect(self.switch_to_search_nearby_city_state)
        self.search_nearby.ui.zip_button.clicked.connect(self.switch_to_search_nearby_zip)

        # Показываем главное меню
        self.switch_to_main_menu()

    # === Методы навигации ===

    def switch_to_main_menu(self):
        self.stack.setCurrentWidget(self.main_menu)

    def switch_to_login_register(self):
        self.stack.setCurrentWidget(self.login_register)

    def switch_to_login(self):
        self.stack.setCurrentWidget(self.login)

    def switch_to_register(self):
        self.stack.setCurrentWidget(self.register)

    def switch_to_search(self):
        self.stack.setCurrentWidget(self.search)

    def switch_to_search_by_fmid(self):
        self.stack.setCurrentWidget(self.search_by_fmid)

    def switch_to_search_by_name(self):
        self.stack.setCurrentWidget(self.search_by_name)

    def switch_to_search_by_city_state(self):
        self.stack.setCurrentWidget(self.search_by_city_state)

    def switch_to_search_by_zip(self):
        self.stack.setCurrentWidget(self.search_by_zip)

    def switch_to_search_nearby(self):
        self.stack.setCurrentWidget(self.search_nearby)

    def switch_to_search_nearby_fmid(self):
        self.stack.setCurrentWidget(self.search_nearby_fmid)

    def switch_to_search_nearby_name(self):
        self.stack.setCurrentWidget(self.search_nearby_name)

    def switch_to_search_nearby_city_state(self):
        self.stack.setCurrentWidget(self.search_nearby_city_state)

    def switch_to_search_nearby_zip(self):
        self.stack.setCurrentWidget(self.search_nearby_zip)

    def switch_to_all_markets(self):
        self.stack.setCurrentWidget(self.all_markets)

    def switch_to_market_result(self):
        self.stack.setCurrentWidget(self.market_result)

    def switch_to_market_result_nearby(self):
        self.stack.setCurrentWidget(self.market_result_nearby)

    def switch_to_details(self):
        self.last_window = self.stack.currentWidget()
        self.stack.setCurrentWidget(self.details)

    def switch_to_leave_review(self):
        self.stack.setCurrentWidget(self.leave_review)

    def switch_to_view_reviews(self):
        self.stack.setCurrentWidget(self.view_reviews)

    def switch_to_help(self):
        self.stack.setCurrentWidget(self.help)

    def go_back(self):
        if self.last_window:
            self.stack.setCurrentWidget(self.last_window)
            self.last_window = None
        else:
            self.switch_to_main_menu()


# === Классы-обёртки для UI (только чтобы добавить кнопки) ===
class MainMenuWidget(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = MainWindowUI()
        self.ui.setupUi(self)


class LoginRegisterWidget(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = LoginRegisterUI()
        self.ui.setupUi(self)


class LoginWidget(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = LoginUI()
        self.ui.setupUi(self)


class RegisterWidget(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = RegisterUI()
        self.ui.setupUi(self)


class SearchWidget(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = SearchUI()
        self.ui.setupUi(self)


class SearchByFmidWidget(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = SearchByFmidUI()
        self.ui.setupUi(self)


class SearchByNameWidget(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = SearchByNameUI()
        self.ui.setupUi(self)


class SearchByCityStateWidget(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = SearchByCityStateUI()
        self.ui.setupUi(self)


class SearchByZipWidget(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = SearchByZipUI()
        self.ui.setupUi(self)


class SearchNearbyFmidWidget(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = SearchNearbyFmidUI()
        self.ui.setupUi(self)


class SearchNearbyNameWidget(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = SearchNearbyNameUI()
        self.ui.setupUi(self)


class SearchNearbyCityStateWidget(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = SearchNearbyCityStateUI()
        self.ui.setupUi(self)


class SearchNearbyZipWidget(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = SearchNearbyZipUI()
        self.ui.setupUi(self)


class SearchNearbyWidget(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = SearchNearbyUI()
        self.ui.setupUi(self)


class AllMarketsWidget(QMainWindow):
    def __init__(self, db):
        super().__init__()
        self.ui = AllMarketsUI()
        self.ui.setupUi(self)
        self.db = db
        self.current_page = 0
        self.total_pages = 0

        # Подключаем кнопки
        self.ui.back_page_button.clicked.connect(self.prev_page)
        self.ui.next_page_button.clicked.connect(self.next_page)

    def load_page(self, page=0):
        """Загружает страницу из БД"""
        self.current_page = page
        markets, total = self.db.get_all_markets(page, per_page=10)
        self.total_pages = (total + 9) // 10

        if not markets:
            return

        # Берём ключи из первого рынка
        keys = list(markets[0].keys())

        # Настраиваем таблицу
        self.ui.output_table_info.setRowCount(len(markets))
        self.ui.output_table_info.setColumnCount(len(keys))
        self.ui.output_table_info.setHorizontalHeaderLabels(keys)

        # Заполняем таблицу
        for row, market in enumerate(markets):
            for col, key in enumerate(keys):
                value = market.get(key)

                if key == 'avg_rating':
                    value = f"{value:.1f}" if value else "None"
                elif value is None:
                    value = "None"

                self.ui.output_table_info.setItem(row, col, QTableWidgetItem(str(value)))
        self.ui.output_table_info.resizeColumnsToContents()

        # Обновляем пагинацию
        self.ui.pagination_info.setText(f"Страница {page + 1} из {self.total_pages}")
        self.ui.back_page_button.setEnabled(page > 0)
        self.ui.next_page_button.setEnabled(page + 1 < self.total_pages)

    def prev_page(self):
        self.load_page(self.current_page - 1)

    def next_page(self):
        self.load_page(self.current_page + 1)


class MarketResultWidget(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = MarketResultUI()
        self.ui.setupUi(self)

    def display(self, data):
        """
        Универсальный метод: принимает либо один словарь, либо список словарей
        """
        if isinstance(data, dict):
            self.display_market(data)
        elif isinstance(data, list):
            self.display_markets(data)
        else:
            print(f"Ошибка: неизвестный тип данных {type(data)}")

    def display_market(self, market):
        """Отображает один рынок в таблице"""
        keys = market.keys()
        self.ui.output_table_info.setRowCount(1)
        self.ui.output_table_info.setColumnCount(len(market))
        self.ui.output_table_info.setHorizontalHeaderLabels(keys)
        for col, key in enumerate(keys):
            value = market.get(key)
            if key == 'fmid':
                value = str(value)
            elif key == 'avg_rating':
                value = f"{value:.1f}" if value else "None"
            elif key == 'website':
                value = value or "None"
            elif value is None:
                value = "None"
            self.ui.output_table_info.setItem(0, col, QTableWidgetItem(str(value)))
        self.ui.output_table_info.resizeColumnsToContents()

    def display_markets(self, markets):
        """Отображает список рынков в таблице"""
        if not markets:
            return
        keys = markets[0].keys()
        self.ui.output_table_info.setRowCount(len(markets))
        self.ui.output_table_info.setColumnCount(len(keys))
        self.ui.output_table_info.setHorizontalHeaderLabels(keys)
        for row, market in enumerate(markets):
            for col, key in enumerate(keys):
                value = market.get(key)
                if key == 'fmid':
                    value = str(value)
                elif key == 'avg_rating':
                    value = f"{value:.1f}" if value else "None"
                elif key == 'website':
                    value = value or "None"
                elif value is None:
                    value = "None"
                self.ui.output_table_info.setItem(row, col, QTableWidgetItem(str(value)))
        self.ui.output_table_info.resizeColumnsToContents()


class MarketResultNearbyWidget(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = MarketResultNearbyUI()
        self.ui.setupUi(self)

    def display_markets(self, markets):
        """Отображает список рынков в таблице"""
        if not markets:
            return
        keys = markets[0].keys()
        self.ui.output_table_info.setRowCount(len(markets))
        self.ui.output_table_info.setColumnCount(len(keys))
        self.ui.output_table_info.setHorizontalHeaderLabels(keys)
        for row, market in enumerate(markets):
            for col, key in enumerate(keys):
                value = market.get(key)
                if key == 'fmid':
                    value = str(value)
                elif key == 'avg_rating':
                    value = f"{value:.1f}" if value else "None"
                elif key == 'website':
                    value = value or "None"
                elif value is None:
                    value = "None"
                self.ui.output_table_info.setItem(row, col, QTableWidgetItem(str(value)))
        self.ui.output_table_info.resizeColumnsToContents()


class DetailsWidget(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = DetailsUI()
        self.ui.setupUi(self)

    def display_market(self, market):
        """Отображает один рынок в таблице"""
        keys = market.keys()
        self.ui.output_table_info.setRowCount(len(market))
        self.ui.output_table_info.setColumnCount(1)
        self.ui.output_table_info.setVerticalHeaderLabels(keys)
        self.ui.output_table_info.setHorizontalHeaderLabels([f"FMID: {market['fmid']}"])

        for col, key in enumerate(keys):
            value = market.get(key)
            if key == 'fmid':
                value = str(value)
            elif key == 'avg_rating':
                value = f"{value:.1f}" if value else "нет оценок"
            elif key == 'website':
                value = value or "нет данных"
            elif value is None:
                value = "None"
            self.ui.output_table_info.setItem(0, col, QTableWidgetItem(str(value)))
        self.ui.output_table_info.resizeColumnsToContents()


class LeaveReviewWidget(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = LeaveReviewUI()
        self.ui.setupUi(self)
        self.ui.output_table_info.setPlaceholderText("Введите ваш комментарий...")


class ViewReviewsWidget(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = ViewReviewsUI()
        self.ui.setupUi(self)


class HelpWidget(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = HelpUI()
        self.parent = None
        self.ui.setupUi(self)
        self.ui.description_text.setHtml("""
        <h2>Help</h2>
        <p>This application is designed for searching farmers' markets.</p>
        <h3>Features:</h3>
        <ul>
            <li>View all markets</li>
            <li>Search by FMID, name, city/state, ZIP</li>
            <li>Search for markets nearby within a 30-mile radius from the initial parameter</li>
            <li>View detailed market information</li>
            <li>Leave reviews</li>
        </ul>
        """)

    def set_parent(self, parent):
        self.parent = parent
