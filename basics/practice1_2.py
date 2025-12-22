# Упражнение 4.1 (контрольное). Преобразователь температуры
def fahrenheit(celsius_value):
    return celsius_value * (9 / 5) + 32


def celsius(fahrenheit_value):
    return (fahrenheit_value - 32) * (5 / 9)


print("1: °C -> °F\n2: °F -> °C")
choice = input("Выберите преобразователь (1 или 2): ")

if choice == "1":
    value = float(input("Введите градусы Цельсия: "))
    print(f"{value}°C = {fahrenheit(value):.1f}°F")
elif choice == "2":
    value = float(input("Введите градусы Фаренгейта: "))
    print(f"{value}°F = {celsius(value):.1f}°C")
else:
    print("Неверный выбор")


# Упражнение 4.2 (контрольное). Расчет оплаты счета

def tax(amount):
    return amount * 0.2
# Берем стандартную ставку в 20 % НДС


def tips(amount, tax_value):
    return (amount - tax_value) * 0.1
# Берем стандартную ставку чаевых 10 % НДС
# считаем сумму чаевых без учета НДС (как описано в задании)


amount = float(input("Введите сумму заказа в ресторане: "))
print(f"Сумма заказа составила: {amount:.2f}\nВ том числе НДС: {tax(amount):.2f}"
      f"\nС учетом чаевых в размере 10 % от суммы заказа: {tips(amount, tax(amount)):.2f}"
      f"\nОбщая сумма к оплате составляет: {amount + tips(amount, tax(amount)):.2f}")

