import sys, os
from PySide6.QtWidgets import QApplication
from database import Database
from app_controler import MyWindow
from dotenv import load_dotenv

load_dotenv()


def main():
    app = QApplication(sys.argv)

    # Подключение к БД — ТОЛЬКО ЗДЕСЬ
    db_config = {
        'host': os.getenv('DB_HOST', 'localhost'),
        'port': int(os.getenv('DB_PORT', 5432)),
        'database': os.getenv('DB_NAME', 'farmers_market'),
        'user': os.getenv('DB_USER', 'username'),
        'password': os.getenv('DB_PASSWORD', 'password')
    }
    db = Database(db_config)

    window = MyWindow(db)
    window.show()

    sys.exit(app.exec())


if __name__ == '__main__':
    main()