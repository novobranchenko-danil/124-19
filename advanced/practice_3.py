'''
Перепишите код из Задания 2, используя циклы для подбора оптимального значения угла, под которым необходимо начать
движение спасателя.
Решите данную задачу аналитически (выведите формулу зависимости угла от остальных параметров) и сравните её решение с
решением, полученным числовым способом при помощи вашей программы.

Касаемо аналитического решения я нашел, что тут в теории подойдет Закон Снеллиуса, но я запутался в формулах и в том,
какие из наших значений к чему относятся. Другое решение я не нашел
'''

import math as m
import numpy as np

VALIDATIONS = {
    "d1": lambda x: x and
                    not any(char.isalpha() for char in x) and
                    float(x) >= 0,         # Для d1: проверка, что x >= 0, не содержит букв, не пустое значение
    "d2": lambda x: x and
                    not any(char.isalpha() for char in x) and
                    float(x) > 0,          # Для d2: проверка, что x > 0, не содержит букв, не пустое значение
    "h": lambda x: x and
                   not any(char.isalpha() for char in x) and
                   float(x) >= 0,          # Для h: проверка, что х >= 0, не содержит букв, не пустое значение
    'v_sand': lambda x: x and
                        not any(char.isalpha() for char in x) and
                        float(x) > 0,      # Для v_sand: проверка, что x > 0, не содержит букв, не пустое значение
    'n': lambda x: x and
                   not any(char.isalpha() for char in x) and
                   float(x) > 0,           # Для n: проверка, что x > 0, не содержит букв, не пустое значение
    'theta1': lambda x: x and
                        not any(char.isalpha() for char in x) and
                        0 <= float(x) <= 90 # Для theta1: проверка, что x от 0 до 90, не содержит букв, не пустое значение
}


def user_input(): # создаем функцию для ввода пользовательских значений
    while True:
        print("=== Ввод данных для расчета времени спасения ===")
        d1 = input("Введите кратчайшее расстояние между спасателем и кромкой воды, d₁ (ярды) => ")
        d2 = input("Введите кратчайшее расстояние от утопающего до берега, d₂ (футы) => ")
        h = input("Введите боковое смещение между спасателем и утопающим, h (ярды) => ")
        v_sand = input("Введите скорость движения спасателя по песку, v_sand (мили в час) => ")
        n = input("Введите коэффициент замедления спасателя при движении в воде, n => ")
        theta1 = input("Введите направление движения спасателя по песку, θ₁ (градусы) => ")

        all_inputs = [
            ('d1', d1), ('d2', d2), ('h', h),
            ('v_sand', v_sand), ('n', n), ('theta1', theta1)
        ]

        for name, value in all_inputs:
            if not VALIDATIONS[name](value):
                print("=" * 50, end="\n"
                      f"Ошибка: недопустимое значение {name} = {value}.\n"
                      f"Значение не может быть пустым или содержать буквы.\n"
                      f"А так же направление движения спасателя песку (θ₁) должно быть в диапазона от 0 до 90 градусов\n"
                      f"Пожалуйста, введите числовые значения снова:\n\n",)
                break
        else:
            return float(d1), float(d2), float(h), float(v_sand), float(n), float(theta1) # возвращаем в виде кортежа


def convert_foot_to_mile(foot): # создаем функцию для конвертации футов в мили
    return foot / 5280


def convert_yard_to_mile(yard): # создаем функцию для конвертации ярдов в мили
    return yard / 1760


def x_calculate(d1, theta1):
    # x = convert_yard_to_mile(d1) * m.tan(m.radians(theta1)) # для отладки
    # print(f"x = {x}")
    return convert_yard_to_mile(d1) * m.tan(m.radians(theta1)) # чтобы не создавать лишних функций переводим градусы в радианы с помощью библиотеки math


def l1_calculate(x, d1):
    # l1 = m.sqrt(x ** 2 + convert_yard_to_mile(d1) ** 2) # для отладки
    # print(f"l1 = {l1}")
    return m.sqrt(x ** 2 + convert_yard_to_mile(d1) ** 2)


def l2_calculate(h, x, d2):
    # l2 = m.sqrt((convert_yard_to_mile(h) - x) ** 2 + convert_foot_to_mile(d2) ** 2) # для отладки
    # print(f"l2 = {l2}")
    return m.sqrt((convert_yard_to_mile(h) - x) ** 2 + convert_foot_to_mile(d2) ** 2)


def time_calculate(l_1, l_2, v_sand, n):
    t = (1 / v_sand) * (l_1 + n * l_2)
    t_sec = convert_hour_to_sec(t)
    # print(f"t_sec = {t_sec}") # для отладки
    return t_sec


def convert_hour_to_sec(hour):
    return hour * 3600


def brute_search(d1, d2, h, v_sand, n): # подбираем угол theta с помощью перебора
    best_theta = 0.0
    best_time = float('inf')

    for theta in np.arange(0, 90.1, 0.1):
        x = x_calculate(d1, theta)
        l_1 = l1_calculate(x, d1)
        l_2 = l2_calculate(h, x, d2)
        current_time = time_calculate(l_1, l_2, v_sand, n)
        if current_time < best_time:
            best_time = current_time
            best_theta = theta
    return best_time, best_theta


def main():
    d1, d2, h, v_sand, n, theta1 = user_input()
    x = x_calculate(d1, theta1)
    l_1 = l1_calculate(x, d1)
    l_2 = l2_calculate(h, x, d2)
    t = time_calculate(l_1, l_2, v_sand, n)
    best_time, best_theta = brute_search(d1, d2, h, v_sand, n)
    print(f"Если спасатель начнёт движение под углом θ₁, равным {int(theta1)} градусам, он достигнет утопающего через {t:.1f} секунды")
    print("=" * 50)
    print(f"Лучшие показатели будут если спасатель начнет движение под углом θ₁, равным {int(best_theta)} градусам, "
          f"тогда он достигнет утопающего через {best_time:.1f} секунды")


def unit_test():
    d1, d2, h, v_sand, n, theta1 = 8, 10, 50, 5, 2, 39.413

    passed = 0
    failed = 0
    tests = 0

    print("=" * 50)
    print("Запуск модульных тестов...")

    '''Тест на проверку значения "х"'''
    expected_x = 0.003735405962476625
    actual_x = x_calculate(d1, theta1)
    # print(actual_x) # для отладки
    if expected_x == actual_x:
        passed += 1
        tests += 1
        print("Test passed!")
    else:
        failed += 1
        tests += 1
        print("Test failed.")

    '''Тест на проверку значения "l_1"'''
    expected_l1 = 0.005883401629100235
    actual_l1 = l1_calculate(actual_x, d1)
    # print(actual_l1) # для отладки
    if expected_l1 == actual_l1:
        passed += 1
        tests += 1
        print("Test passed!")
    else:
        failed += 1
        tests += 1
        print("Test failed.")

    '''Тест на проверку значения "l_2"'''
    extected_l2 = 0.02474626709774013
    actual_l2 = l2_calculate(h, actual_x, d2)
    # print(actual_l2) # для отладки
    if extected_l2 == actual_l2:
        passed += 1
        tests += 1
        print("Test passed!")
    else:
        failed += 1
        tests += 1
        print("Test failed.")

    '''Тест на проверку значения "t"'''
    expected_t = 39.87067379369796
    actual_t = time_calculate(actual_l1, actual_l2, v_sand, n)
    # print(actual_t) # для отладки
    if expected_t == actual_t:
        passed += 1
        tests += 1
        print("Test passed!")
    else:
        failed += 1
        tests += 1
        print("Test failed.")

    '''Тест на сравнение того, что методом подбора θ₁ мы спасаем утопающего за меньшее время'''
    standart_time = 39.87067379369796
    best_time = brute_search(d1, d2, h, v_sand, n)
    if standart_time > best_time[0]:
        passed += 1
        tests += 1
        print("Test passed!")
    else:
        failed += 1
        tests += 1
        print("Test failed.")
    print(f"Всего тестов: {tests}\nУспешных тестов: {passed}\nНеуспешных тестов: {failed}")


if __name__ == "__main__":
    main()
    unit_test()


