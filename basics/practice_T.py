input_number = input("Введите номер билета: ")
if len(input_number) != 6 or not input_number.isdigit():
    print("Ошибка. Нужно ввести 6 цифр")
else:
    int_number = [int(i) for i in input_number]
    print("Ваш билет счастливый!") if sum(int_number[:3]) == sum(int_number[3:]) else print("Ваш билет не счастливый.")

