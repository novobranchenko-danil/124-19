def sqrt(number):
    x = 1
    while True:
        oldx = x
        x = (x + number / x) / 2
        if oldx == x:
            print(f"Квадратный корень из {x * x} = {x}")
            break


sqrt(int(input("Введите число для вычисления квадратного корня: ")))
