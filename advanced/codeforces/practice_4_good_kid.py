'''
Хороший ребенок
'''
import random
import math

# number_of_list = int(input())
# nested_lists = [[random.randrange(10) for _ in range(random.randint(1, 9))] for _ in range(number_of_list)]
#
# for list in nested_lists:
#     list.sort()
#     list[0] += 1
#     print(math.prod(list))
# потом я понял, что каждое число нужно задавать отдельно вводом с клавиатуры

number_of_list = int(input())
nested_lists = []

for _ in range(number_of_list):
    n = int(input()) # данное значение мы нигде не используем, т.к все равно запишем во вложенный список ровно то кол-во символов которые ввели с клавиатуры (убирая пробелы)
    # можно использовать для проверки кол-ва вводимых значений во вложенный список. чтоб не записать лишнее (указали 5 чисел в списке, а ввели 10. запишет первые 5).
    # но судя по ответу с тестовым сценариям с codeforce такой вариант там не тестировался и тогда действительно n не используется
    numbers = list(map(int, input().split()))
    nested_lists.append(numbers)

# print(nested_lists)

for i in nested_lists:
    i.sort()
    i[0] += 1
    print(math.prod(i))

# print(nested_lists)
