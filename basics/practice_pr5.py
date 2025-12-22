'''Упражнение 1. Использование списков'''

# fruits = ['Apple', 'Grape', 'Peach', 'Banan', 'Orange']
# print(fruits[0]) # нумерация начинается с нуля
# print(fruits[1])
# print(fruits[4])
# print(fruits[-1])
# fruits[0] = 'Watermelon'
# fruits[3] = 'Lemon'
# fruits.append('Banan')
#
# if 'Apple' in fruits:
#     print('В списке есть элемент Apple')
# else:
#     print('В списке нет элемента Apple')
#
# print(fruits)

'''Упражнение 2. Получение требуемых данных'''

# s = 'ab12c59p7dq'
# digits = []
# for symbol in s:
#     if '1234567890'.find(symbol) != -1:
#         digits.append(int(symbol))
# print(digits)


'''Упражнение 3. Применение словаря для хранения данных'''

# user1 = {'firstname': 'Ivan', 'lastname':'Петров','age': 19}
# print(user1)
# fname = input('Enter your firstname: ')
# lname = input('Enter your lastname: ')
# age = int(input('Enter your age: '))
# user2 = dict(firstname=fname, lastname=lname, age=age)
# print(user2)
# users = []
# users.append(user1)
# users.append(user2)
# print(users)

'''Упражнение 4.1 (контрольное) Объем продаж'''
# Напишите программу, которая будет запрашивать у пользователя значения
# продаж магазина за каждый день недели и сохранять их в виде списка. Примените
# цикл, чтобы вычислить общий объем продаж за неделю и показать результат. Затем
# программа должна вывести на экран все введенные пользователем числа в порядке
# возрастания – по одному значению в строке. Используйте для сортировки либо
# метод sort, либо функцию sorted.

week = ["Понедельник", "Вторник", "Среда", "Четверг", "Пятница", "Суббота", "Воскресенье"]
day_sales = [int(input(f"Введите сумму продаж за {day}: ")) for day in week]
print(f"Сумма продаж за неделю: {sum(day_sales)}")
print(*sorted(day_sales), sep="\n")

'''Упражнение 4.2 (контрольное) Форматирование по уровню'''
# Напишите программу, в которой создайте список случайно сгенерированных
# чисел от 1 до 100. На основе этого списка создайте второй, который будет содержать
# слова “High” ("высокий”) или “Low” ("низкий") в зависимости от того, больше или
# меньше соответствующее число исходного списка некого порогового значения
# (само значение порога должно вводится пользователем).

import random

numbers = random.sample(range(1, 101), 10)
print(numbers)
comparison = int(input("Введите пороговое значение: "))
conditions = ["higt" if num > comparison else "low" for num in numbers]
print(conditions)
