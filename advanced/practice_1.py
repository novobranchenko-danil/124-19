import math as m


def user_input(): # создаем функцию для ввода пользовательских значений
    distance_to_water = convert_yard_to_mile(float(input("Введите кратчайшее расстояние между спасателем и кромкой воды, d₁ (ярды) => "))) # сразу конвертирум в мили
    distance_water_to_shore = convert_foot_to_mile(float(input("Введите кратчайшее расстояние от утопающего до берега, d₂ (футы) => "))) # сразу конвертирум в мили
    lateral_displacement = convert_yard_to_mile(float(input("Введите боковое смещение между спасателем и утопающим, h (ярды) => "))) # сразу конвертирум в мили
    sand_ms = float(input("Введите скорость движения спасателя по песку, v_sand (мили в час) => "))
    factor = float(input("Введите коэффициент замедления спасателя при движении в воде, n => "))
    movement_direction = float(input("Введите направление движения спасателя по песку, θ₁ (градусы) => "))
    return (distance_to_water, distance_water_to_shore, lateral_displacement, sand_ms, factor, movement_direction) # возвращаем в виде кортежа


def convert_foot_to_mile(foot): # создаем функцию для конвертации футов в мили
    return foot / 5280


def convert_yard_to_mile(yard): # создаем функцию для конвертации ярдов в мили
    return yard / 1760


def time_calculate(): # функция которая производит расчет по формуле
    user_data = user_input() # можно было вернуть значения не в виде кортежа, а по переменным, а тут их обозначит в
    # соответствии с вводимыми значениями (d1, d2, h, v_sand, n, тета1, но т.к я с кортежами мало работал решил поэксперементировать)
    x = (user_data[0] * m.tan(m.radians(user_data[5]))) # чтобы не создавать лишних функций переводим градусы в радианы с помощью библиотеки math
    l_1 = m.sqrt(x ** 2 + user_data[0] ** 2)
    l_2 = m.sqrt((user_data[2] - x) ** 2 + user_data[1] ** 2)
    t = (1 / user_data[3]) * (l_1 + user_data[4] * l_2)
    return user_data[5], t # тут вернул без кортежа


def convert_hour_to_sec(hour): # переводим часы в секунды. изначально не работало, т.к забыл об этом
    return hour * 3600


def main():
    direction, t = time_calculate()
    print(t)
    print(f"Если спасатель начнёт движение под углом θ₁, равным {int(direction)} градусам, он достигнет утопащего через {convert_hour_to_sec(t):.1f} секунды")


if __name__ == "__main__":
    main()
