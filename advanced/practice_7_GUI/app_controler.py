from navigation import MainWindow
from PySide6.QtWidgets import QMessageBox, QTableWidgetItem


class MyWindow(MainWindow):
    """Наследуем MainWindow и добавляем новые коннекты"""

    def __init__(self, db):
        super().__init__(db)  # ← передаём db родителю
        self.add_custom_handlers()

    def add_custom_handlers(self):
        self.search_by_fmid.ui.search_button.clicked.connect(self.click_search_fmid_button)
        self.search_by_name.ui.search_button.clicked.connect(self.click_search_name_button)
        self.search_by_city_state.ui.search_button.clicked.connect(self.click_search_city_state_button)
        self.search_by_zip.ui.search_button.clicked.connect(self.click_search_zip_button)

        self.search_nearby_fmid.ui.search_button.clicked.connect(self.click_search_fmid_button_nearby)
        self.search_nearby_name.ui.search_button.clicked.connect(self.click_search_name_button_nearby)
        self.search_nearby_city_state.ui.search_button.clicked.connect(self.click_search_city_state_button_nearby)
        self.search_nearby_zip.ui.search_button.clicked.connect(self.click_search_zip_button_nearby)

        self.main_menu.ui.all_market_button.clicked.connect(self.click_search_all_market_button)

        self.market_result.ui.search_button.clicked.connect(self.click_search_detail)
        self.market_result_nearby.ui.search_button.clicked.connect(self.click_search_detail_nearby)
        self.all_markets.ui.search_button.clicked.connect(self.click_search_detail_all_market)

    def click_search_fmid_button(self):
        fmid_text = self.search_by_fmid.ui.fmid_input.text()
        if not fmid_text.isdigit():
            QMessageBox.warning(self, "Ошибка", "Введите корректный FMID.\nFMID не может содержать буквы\nили быть пустым")
            return

        fmid = int(fmid_text)
        result = self.db.search_markets(fmid=fmid)
        if result is None:
            QMessageBox.warning(self, "Ошибка", f"Рынков с FMID: '{fmid}' не найдено")
            return
        self.market_result.display(result)
        self.switch_to_market_result()

    def click_search_name_button(self):
        market_name_text = self.search_by_name.ui.market_name_input.text()
        if not market_name_text:
            QMessageBox.warning(self, "Ошибка", "Введите корректный Market Name.\nMarket Name не может быть пустым")
            return

        result = self.db.search_markets(name=market_name_text)

        if not result:
            QMessageBox.warning(self, "Ошибка", f"Рынков с Market Name: '{market_name_text}' не найдено")
            return
        self.market_result.display(result)
        self.switch_to_market_result()

    def click_search_city_state_button(self):
        city_text = self.search_by_city_state.ui.city_input.text()
        state_text = self.search_by_city_state.ui.state_input.text()

        if not city_text and not state_text:
            QMessageBox.warning(self, "Ошибка", "Введите город или штат.\nХотя бы одно поле должно быть заполнено")
            return

        def is_valid_location(text):
            return all(c.isalpha() or c.isspace() for c in text)

        if city_text and not is_valid_location(city_text):
            QMessageBox.warning(self, "Ошибка", "Город должен содержать только буквы и пробелы")
            return

        if state_text and not is_valid_location(state_text):
            QMessageBox.warning(self, "Ошибка", "Штат должен содержать только буквы и пробелы")
            return

        result = self.db.search_markets(city=city_text, state=state_text)

        if not result:
            QMessageBox.warning(self, "Ошибка", f"Рынков с City '{city_text}' State '{state_text}' не найдено")
            return
        self.market_result.display(result)
        self.switch_to_market_result()

    def click_search_zip_button(self):
        zip_name_text = self.search_by_zip.ui.zip_input.text()
        if not zip_name_text.isdigit():
            QMessageBox.warning(self, "Ошибка", "Введите корректный ZIP.\nZIP не может содержать буквы\nили быть пустым")
            return
        if len(zip_name_text) != 5:
            QMessageBox.warning(self, "Ошибка", "Введите корректный ZIP.\nZIP состоит из 5 цифр")
            return

        result = self.db.search_markets(zip_code=zip_name_text)

        if not result:
            QMessageBox.warning(self, "Ошибка", f"Рынков с ZIP: '{zip_name_text}' не найдено")
            return
        self.market_result.display(result)
        self.switch_to_market_result()

    def click_search_fmid_button_nearby(self):
        fmid_text = self.search_nearby_fmid.ui.fmid_input.text()
        if not fmid_text.isdigit():
            QMessageBox.warning(self, "Ошибка", "Введите корректный FMID.\nFMID не может содержать буквы\nили быть пустым")
            return

        fmid = int(fmid_text)
        result = self.db.search_nearby(fmid=fmid)
        if result is None:
            QMessageBox.warning(self, "Ошибка", f"Рынков с FMID: '{fmid}' не найдено")
            return
        self.market_result_nearby.display_markets(result)
        self.switch_to_market_result_nearby()

    def click_search_name_button_nearby(self):
        market_name_text = self.search_nearby_name.ui.market_name_input.text()
        if not market_name_text:
            QMessageBox.warning(self, "Ошибка", "Введите корректный Market Name.\nMarket Name не может быть пустым")
            return

        result = self.db.search_nearby(name=market_name_text)

        if not result:
            QMessageBox.warning(self, "Ошибка", f"Рынков с Market Name: '{market_name_text}' не найдено")
            return
        self.market_result_nearby.display_markets(result)
        self.switch_to_market_result_nearby()

    def click_search_city_state_button_nearby(self):
        city_text = self.search_nearby_city_state.ui.city_input.text()
        state_text = self.search_nearby_city_state.ui.state_input.text()

        if not city_text and not state_text:
            QMessageBox.warning(self, "Ошибка", "Введите город или штат.\nХотя бы одно поле должно быть заполнено")
            return

        def is_valid_location(text):
            return all(c.isalpha() or c.isspace() for c in text)

        if city_text and not is_valid_location(city_text):
            QMessageBox.warning(self, "Ошибка", "Город должен содержать только буквы и пробелы")
            return

        if state_text and not is_valid_location(state_text):
            QMessageBox.warning(self, "Ошибка", "Штат должен содержать только буквы и пробелы")
            return

        result = self.db.search_nearby(city=city_text, state=state_text)

        if not result:
            QMessageBox.warning(self, "Ошибка", f"Рынков с City '{city_text}' State '{state_text}' не найдено")
            return
        self.market_result_nearby.display_markets(result)
        self.switch_to_market_result_nearby()

    def click_search_zip_button_nearby(self):
        zip_name_text = self.search_nearby_zip.ui.zip_input.text()
        if not zip_name_text.isdigit():
            QMessageBox.warning(self, "Ошибка", "Введите корректный ZIP.\nZIP не может содержать буквы\nили быть пустым")
            return
        if len(zip_name_text) != 5:
            QMessageBox.warning(self, "Ошибка", "Введите корректный ZIP.\nZIP состоит из 5 цифр")
            return

        result = self.db.search_nearby(zip_code=zip_name_text)

        if not result:
            QMessageBox.warning(self, "Ошибка", f"Рынков с ZIP: '{zip_name_text}' не найдено")
            return
        self.market_result_nearby.display_markets(result)
        self.switch_to_market_result_nearby()

    def click_search_all_market_button(self):
        self.all_markets.load_page(0)
        self.switch_to_all_markets()

    def click_search_detail(self):
        row_number = self.market_result.ui.number_field_input.text()
        detail_fmid = self.market_result.ui.output_table_info.item(int(row_number) - 1, 0).text()
        result = self.db.get_market_details(int(detail_fmid))
        self.details.display_market(result)
        self.switch_to_details()

    def click_search_detail_nearby(self):
        row_number = self.market_result_nearby.ui.number_field_input.text()
        detail_fmid = self.market_result_nearby.ui.output_table_info.item(int(row_number) - 1, 0).text()
        result = self.db.get_market_details(int(detail_fmid))
        self.details.display_market(result)
        self.switch_to_details()

    def click_search_detail_all_market(self):
        row_number = self.all_markets.ui.number_field_input.text()
        detail_fmid = self.all_markets.ui.output_table_info.item(int(row_number) - 1, 0).text()
        result = self.db.get_market_details(int(detail_fmid))
        self.details.display_market(result)
        self.switch_to_details()
