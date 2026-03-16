import math


class RatNum:
    def __init__(self, numerator, denominator=1):
        """
           Создаёт рациональное число numerator/denominator.

           Поля представления:
               _is_nan: bool - флаг NaN
               _num: int - числитель (если не NaN)
               _den: int - знаменатель (если не NaN)

           Инвариант представления:
               1. Если _is_nan == True: _num и _den не используются
               2. Если _is_nan == False:
                  - _den > 0
                  - gcd(|_num|, _den) == 1
                  - знак числа в _num

           Функция абстракции:
               AF(self) = NaN если _is_nan, иначе _num / _den

           @requires:
               denominator != 0 для создания обычного числа
               (если denominator == 0, создаётся NaN)

           @modifies:
               Создаёт новый объект RatNum

           @effects:
               Создаёт рациональное число в сокращённом виде
               Знак числа переносится в числитель
               Если denominator == 0, создаёт NaN

           @throws:
               None

           @returns:
               None
           """
        # Если знаменатель 0 - это NaN
        if denominator == 0:
            self._is_nan = True
            self._num = 0
            self._den = 0
            return

        self._is_nan = False

        # Приводим знак в числитель
        if denominator < 0:
            numerator = -numerator
            denominator = -denominator

        # Сокращаем дробь
        g = math.gcd(abs(numerator), denominator)
        self._num = numerator // g
        self._den = denominator // g

    def __str__(self) -> str:
        """
        Возвращает строковое представление числа.

        @requires:
            None

        @modifies:
            None

        @effects:
            Форматирует число в строку:
            "NaN" для NaN
            "0" для нуля
            "n" для целых чисел
            "n/d" для дробей

        @throws:
            None

        @returns:
            str - строковое представление
        """
        if self.is_nan():
            return "NaN"
        if self._num == 0:
            return "0"
        if self._den == 1:
            return str(self._num)
        return f"{self._num}/{self._den}"

    def __eq__(self, other) -> bool:
        """
        Проверяет равенство двух объектов.

        @requires:
            None

        @modifies:
            None

        @effects:
            Сравнивает текущее число с другим объектом
            NaN равен только NaN

        @throws:
            None

        @returns:
            bool - True если объекты равны, иначе False
        """
        if not isinstance(other, RatNum):
            return False

        if self.is_nan():
            return other.is_nan()

        if other.is_nan():
            return False

        return self._num == other._num and self._den == other._den

    def __neg__(self) -> 'RatNum':
        """
        Возвращает число с противоположным знаком.

        @requires:
            None

        @modifies:
            None

        @effects:
            Возвращает новое число, равное -self
            Если self NaN, результат NaN

        @throws:
            None

        @returns:
            RatNum - аддитивная инверсия
        """
        if self.is_nan():
            return RatNum(1, 0)  # NaN

        return RatNum(-self._num, self._den)

    def __add__(self, other: 'RatNum') -> 'RatNum':
        """
        Складывает два рациональных числа.

        @requires:
            other является экземпляром RatNum

        @modifies:
            None

        @effects:
            Возвращает новое число, равное self + other
            Если self или other NaN, результат NaN

        @throws:
            TypeError если other не RatNum

        @returns:
            RatNum - сумма чисел
        """
        if not isinstance(other, RatNum):
            raise TypeError("Can only add RatNum")

        if self.is_nan() or other.is_nan():
            return RatNum(1, 0)  # NaN

        # a/b + c/d = (a*d + c*b) / (b*d)
        new_num = self._num * other._den + other._num * self._den
        new_den = self._den * other._den

        return RatNum(new_num, new_den)

    def __sub__(self, other: 'RatNum') -> 'RatNum':
        """
        Вычитает другое число из текущего.

        @requires:
            other является экземпляром RatNum

        @modifies:
            None

        @effects:
            Возвращает новое число, равное self - other
            Если self или other NaN, результат NaN

        @throws:
            TypeError если other не RatNum

        @returns:
            RatNum - разность чисел
        """
        if not isinstance(other, RatNum):
            raise TypeError("Can only subtract RatNum")

        if self.is_nan() or other.is_nan():
            return RatNum(1, 0)  # NaN

        # a/b - c/d = (a*d - c*b) / (b*d)
        new_num = self._num * other._den - other._num * self._den
        new_den = self._den * other._den

        return RatNum(new_num, new_den)

    def __mul__(self, other: 'RatNum') -> 'RatNum':
        """
        Умножает два рациональных числа.

        @requires:
            other является экземпляром RatNum

        @modifies:
            None

        @effects:
            Возвращает новое число, равное self * other
            Если self или other NaN, результат NaN

        @throws:
            TypeError если other не RatNum

        @returns:
            RatNum - произведение чисел
        """
        if not isinstance(other, RatNum):
            raise TypeError("Can only multiply RatNum")

        if self.is_nan() or other.is_nan():
            return RatNum(1, 0)  # NaN

        # (a/b) * (c/d) = (a*c) / (b*d)
        new_num = self._num * other._num
        new_den = self._den * other._den

        return RatNum(new_num, new_den)

    def __truediv__(self, other: 'RatNum') -> 'RatNum':
        """
        Делит текущее число на другое.

        @requires:
            other является экземпляром RatNum

        @modifies:
            None

        @effects:
            Возвращает новое число, равное self / other
            Если self или other NaN, результат NaN
            Если other == 0, результат NaN

        @throws:
            TypeError если other не RatNum

        @returns:
            RatNum - частное чисел
        """
        if not isinstance(other, RatNum):
            raise TypeError("Can only divide by RatNum")

        if self.is_nan() or other.is_nan():
            return RatNum(1, 0)  # NaN

        # Деление на ноль даёт NaN
        if other._num == 0:
            return RatNum(1, 0)  # NaN

        # (a/b) / (c/d) = (a*d) / (b*c)
        new_num = self._num * other._den
        new_den = self._den * other._num

        return RatNum(new_num, new_den)

    def __hash__(self) -> int:
        """
        Возвращает хэш числа для использования в словарях.

        @requires:
            None

        @modifies:
            None

        @effects:
            Вычисляет хэш на основе числителя и знаменателя
            Все NaN имеют одинаковый хэш

        @throws:
            None

        @returns:
            int - хэш-значение
        """
        if self.is_nan():
            return hash(('NaN',))
        return hash((self._num, self._den))

    @property
    def numerator(self):
        return self._num

    @property
    def denominator(self):
        return self._den

    def is_nan(self) -> bool:
        """
        Проверяет, является ли число NaN.

        @requires:
            None

        @modifies:
            None

        @effects:
            Определяет, является ли текущее число специальным значением NaN

        @throws:
            None

        @returns:
            bool - True если число NaN, иначе False
        """
        return self._is_nan

    def is_positive(self) -> bool:
        """
        Проверяет, является ли число положительным.

        @requires:
            not self.is_nan()

        @modifies:
            None

        @effects:
            Проверяет, больше ли число нуля

        @throws:
            ValueError если число NaN

        @returns:
            bool - True если число > 0, иначе False
        """
        if self.is_nan():
            raise ValueError("Cannot check sign of NaN")
        return self._num > 0

    def is_negative(self) -> bool:
        """
        Проверяет, является ли число отрицательным.

        @requires:
            not self.is_nan()

        @modifies:
            None

        @effects:
            Проверяет, меньше ли число нуля

        @throws:
            ValueError если число NaN

        @returns:
            bool - True если число < 0, иначе False
        """
        if self.is_nan():
            raise ValueError("Cannot check sign of NaN")
        return self._num < 0

    def compare_to(self, other: 'RatNum') -> int:
        """
        Сравнивает текущее число с другим.

        @requires:
            other является экземпляром RatNum

        @modifies:
            None

        @effects:
            Сравнивает два рациональных числа.
            NaN считается больше любого обычного числа.
            NaN равен только NaN.

        @throws:
            TypeError если other не RatNum

        @returns:
            int - -1 если self < other
                   0 если self == other
                   1 если self > other
        """
        if not isinstance(other, RatNum):
            raise TypeError("Can only compare with RatNum")

        # Случаи с NaN
        if self.is_nan() and other.is_nan():
            return 0
        if self.is_nan():
            return 1  # NaN больше любого числа
        if other.is_nan():
            return -1  # Любое число меньше NaN

        # Сравниваем обычные числа: a/b ? c/d
        # Приводим к общему знаменателю: a*d ? c*b
        left = self._num * other._den
        right = other._num * self._den

        if left < right:
            return -1
        elif left > right:
            return 1
        else:
            return 0

    def float_value(self) -> float:
        """
        Преобразует число в float.

        @requires:
            None

        @modifies:
            None

        @effects:
            Возвращает приближение рационального числа в виде float
            Для NaN возвращает float('nan')

        @throws:
            None

        @returns:
            float - число с плавающей точкой
        """
        if self.is_nan():
            return float('nan')
        return self._num / self._den

    def int_value(self) -> int:
        """
        Возвращает целую часть числа (отбрасывая дробную).

        @requires:
            None

        @modifies:
            None

        @effects:
            Возвращает целую часть числа (floor division)
            Для NaN возвращает 0

        @throws:
            None

        @returns:
            int - целая часть числа
        """
        if self.is_nan():
            return 0
        return int(self._num / self._den)