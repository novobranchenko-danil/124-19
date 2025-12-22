'''Упражнение 1. Базовое применение модуля random'''
#
import random
# print(random.random()) # Случайное float: 0.0 <= x < 1.0
# print(random.uniform(2.5, 10.0)) # Случайное float: 2.5 <= x < 10.0
# # Укажите для uniform целые границы и проверьте какой тип числа возвращается.
# # print(random.uniform(2, 10)) # Случайное float: 2 <= x < 10
#
# print(random.randrange(10)) # целое число от 0 до 10 включительно
# print(random.randrange(0, 101, 2)) # Четное целое число от 0 до 100 включительно
# # Измените третий параметр на 3 или 4 – определите какого характера получается число?
# # print(random.randrange(0, 101, 3)) # Нечетное целое число от 0 до 100 включительно
# print(random.randint(1, 21)) # целое число в диапазоне 1 <= N <= 21

'''Задание 2 (контрольное)'''
# Создайте список случайных вещественных чисел от 0 до 1 размером на усмотрение пользователя. Вывод реализуйте на свое усмотрение.
float_list = [random.uniform(0, 1) for i in range(10)]
print(float_list)


'''Упражнение 2. Функции для работы с коллекциями'''

# import random
# print(random.choice([1, 2, 3, 4, 5, 6, 7, 8, 9, 10]))
#
# print(random.choices(['red', 'black', 'green'], [18, 18, 2], k=6))
# # Измените параметры так, чтобы элемент 'green' гарантированно не попал бы
# # в итоговый список.
# # print(random.choices(['red', 'black', 'green'], [18, 18, 0], k=6))
#
# print(random.sample([1, 2, 3, 4, 5, 6, 7, 8, 9, 10], 5))
#
# numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
# random.shuffle(numbers)
# print(numbers)

'''Упражнение 3. Расчет основных характеристик описательной статистики'''

# import statistics
# li = [1, 2, 3, 3, 2, 2, 2, 1]
# print ("The average of list values is : ",end="")
# print (statistics.mean(li))
#
#
# # importing the statistics module
# from statistics import median
# # Importing fractions module as fr
# from fractions import Fraction as fr
# # tuple of positive integer numbers
# data1 = (2, 3, 4, 5, 7, 9, 11)
# # tuple of floating point values
# data2 = (2.4, 5.1, 6.7, 8.9)
# # tuple of fractional numbers
# data3 = (fr(1, 2), fr(44, 12),
# fr(10, 3), fr(2, 3))
# # tuple of a set of negative integers
# data4 = (-5, -1, -12, -19, -3)
# # tuple of set of positive
# # and negative integers
# data5 = (-1, -2, -3, -4, 4, 3, 2, 1)
# # Printing the median of above datasets
# print("Median of data-set 1 is % s" % (median(data1)))
# print("Median of data-set 2 is % s" % (median(data2)))
# print("Median of data-set 3 is % s" % (median(data3)))
# print("Median of data-set 4 is % s" % (median(data4)))
# print("Median of data-set 5 is % s" % (median(data5)))

# from statistics import mode
# # Importing fractions module as fr
# # Enables to calculate harmonic_mean of a set in Fraction
# from fractions import Fraction as fr
# # tuple of positive integer numbers
# data1 = (2, 3, 3, 4, 5, 5, 5, 5, 6, 6, 6, 7)
# # tuple of a set of floating point values
# data2 = (2.4, 1.3, 1.3, 1.3, 2.4, 4.6)
# # tuple of a set of fractional numbers
# data3 = (fr(1, 2), fr(1, 2), fr(10, 3), fr(2, 3))
# # tuple of a set of negative integers
# data4 = (-1, -2, -2, -2, -7, -7, -9)
# # tuple of strings
# data5 = ("red", "blue", "black", "blue", "black", "black", "brown")
# # Printing out the mode of the above data-sets
# print("Mode of data set 1 is % s" % (mode(data1)))
# print("Mode of data set 2 is % s" % (mode(data2)))
# print("Mode of data set 3 is % s" % (mode(data3)))
# print("Mode of data set 4 is % s" % (mode(data4)))
# print("Mode of data set 5 is % s" % (mode(data5)))

# from statistics import stdev
# # importing fractions as parameter values
# from fractions import Fraction as fr
# # creating a varying range of sample sets
# # numbers are spread apart but not very much
# sample1 = (1, 2, 5, 4, 8, 9, 12)
# # tuple of a set of negative integers
# sample2 = (-2, -4, -3, -1, -5, -6)
# # tuple of a set of positive and negative numbers
# # data-points are spread apart considerably
# sample3 = (-9, -1, -0, 2, 1, 3, 4, 19)
# # tuple of a set of floating point values
# sample4 = (1.23, 1.45, 2.1, 2.2, 1.9)
# # Print the standard deviation of
# # following sample sets of observations
# print("The Standard Deviation of Sample1 is % s"
# % (stdev(sample1)))
# print("The Standard Deviation of Sample2 is % s"
# % (stdev(sample2)))
# print("The Standard Deviation of Sample3 is % s"
# % (stdev(sample3)))
# print("The Standard Deviation of Sample4 is % s"
# % (stdev(sample4)))


'''Упражнение 4. (контрольное) Обработка данных измерений датчика'''
# Напишите программу, в которой сымитируйте работу датчика измерения температуры,
# вариант заполнения случайными значениями температуры на ваше усмотрение, объем измерений 100.
# Реализуйте подсчет для набора температур среднего значения, медианы (median), моды
# и стандартного отклонения (stdev), предварительно импортировав соответствующие модули.
import statistics

sensor = {
    "model" : "BSC",                    # название модели
    "measures" : (20, 7),               # размеры модели
    "accuracy" : 0.1,                   # точность\погрешность измерения
    "temp_permission" : (-40, 125),     # допустимый температурный диапазон
    "temp_list" : []                    # список зафиксированной температуры
}
#print(sensor)

sensor["temp_list"].extend(random.uniform(-40.0, 125.0) for _ in range(1, 101))
#print(sensor)

print(f"The average of list values is: {statistics.mean(sensor['temp_list'])}")
print(f"Median of Sensor {sensor['model']} temp_list is: {statistics.median(sensor['temp_list'])}")
print(f"Mode of Sensor {sensor['model']} temp_list is: {statistics.mode(sensor['temp_list'])}")
print(f"The Standard Deviation of Sensor {sensor['model']} temp_list is: {statistics.stdev(sensor['temp_list'])}")

