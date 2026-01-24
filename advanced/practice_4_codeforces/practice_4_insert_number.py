'''
Вставь цифру
'''


import random

number_of_list = int(input())
for _ in range(number_of_list):
    len_and_digit = list(map(int, input().split()))
    # print(len_and_digit)
    # n = len_and_digit[0]
    # number = random.randint(10 ** (n - 1), 10 ** n - 1) # из текста задания я подумал, что числа нужно сгенерить, а
    # # видимо нужно использовать тот набор данных, который указан на сайте
    # print(number)
    # str_number = str(number)
    str_number = input()
    for i, ch in enumerate(str_number):
        if int(ch) < len_and_digit[1]:
            print(int((str_number[:i]) + str(len_and_digit[1]) + str_number[i:]))
            break
    else:
        print(int(str_number + str(len_and_digit[1])))
