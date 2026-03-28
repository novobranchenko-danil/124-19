import os
import subprocess


def run_pyside6_uic(input_file, output_file):
    """Запускает pyside6-uic для одного файла"""
    # Используем двойные кавычки вокруг путей
    cmd = f'pyside6-uic "{input_file}" -o "{output_file}"'
    print(f"➡️  {cmd}")
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"❌ Ошибка: {result.stderr}")
        return False
    print(f"✅ {os.path.basename(output_file)}")
    return True


def main():
    # Проверяем, что мы в правильной папке
    script_dir = os.path.dirname(os.path.abspath(__file__))
    ui_dir = os.path.join(script_dir, "resources", "ui")
    windows_dir = os.path.join(script_dir, "windows")

    # Создаём папку windows, если её нет
    if not os.path.exists(windows_dir):
        os.makedirs(windows_dir)
        print(f"📁 Создана папка: {windows_dir}")

    # Проверяем, что папка с ui файлами существует
    if not os.path.exists(ui_dir):
        print(f"❌ Папка не найдена: {ui_dir}")
        return

    # Список всех .ui файлов
    ui_files = [
        ("details.ui", "details.py"),
        ("help.ui", "help.py"),
        ("leave_review.ui", "leave_review.py"),
        ("login.ui", "login.py"),
        ("login_register.ui", "login_register.py"),
        ("main_window.ui", "main_window.py"),
        ("market_result.ui", "market_result.py"),
        ("market_result_nearby.ui", "market_result_nearby.py"),
        ("register.ui", "register.py"),
        ("search.ui", "search.py"),
        ("search_all_market.ui", "search_all_market.py"),
        ("search_by_city_state.ui", "search_by_city_state.py"),
        ("search_by_fmid.ui", "search_by_fmid.py"),
        ("search_by_market_name.ui", "search_by_market_name.py"),
        ("search_by_zip.ui", "search_by_zip.py"),
        ("search_nearby.ui", "search_nearby.py"),
        ("search_nearby_city_state.ui", "search_nearby_city_state.py"),
        ("search_nearby_fmid.ui", "search_nearby_fmid.py"),
        ("search_nearby_market_name.ui", "search_nearby_market_name.py"),
        ("search_nearby_zip.ui", "search_nearby_zip.py"),
        ("view_reviews.ui", "view_reviews.py"),
    ]

    print("\n" + "=" * 50)
    print("🔧 Генерация UI файлов")
    print("=" * 50)

    success_count = 0
    for ui_file, py_file in ui_files:
        input_path = os.path.join(ui_dir, ui_file)
        output_path = os.path.join(windows_dir, py_file)

        if not os.path.exists(input_path):
            print(f"⚠️  Файл не найден: {ui_file}")
            continue

        if run_pyside6_uic(input_path, output_path):
            success_count += 1

    print("=" * 50)
    print(f"✅ Готово! Сгенерировано {success_count} из {len(ui_files)} файлов")
    print("=" * 50)


if __name__ == "__main__":
    main()