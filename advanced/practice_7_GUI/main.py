import sys, os
from PySide6.QtWidgets import QApplication
from windows.main_window import MainWindow


def load_styles(app):
    """Загружаем стили для всего приложения"""
    current_dir = os.path.dirname(os.path.abspath(__file__))
    style_path = os.path.join(current_dir, 'resources', 'styles.qss')

    try:
        with open(style_path, 'r', encoding='utf-8') as f:
            app.setStyleSheet(f.read())  # ← применяем ко ВСЕМУ приложению!
        print("Стили загружены")
    except FileNotFoundError:
        print(f"Файл не найден: {style_path}")
    except Exception as e:
        print(f"Ошибка: {e}")


def main():
    # Создаем приложение
    app = QApplication(sys.argv)
    load_styles(app)

    # Создаем главное окно
    window = MainWindow()
    window.show()

    # Запускаем приложение
    return app.exec()


if __name__ == '__main__':
    sys.exit(main())
