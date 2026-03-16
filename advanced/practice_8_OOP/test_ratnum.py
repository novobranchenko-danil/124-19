import unittest
from ratnum import RatNum


class TestRatNumInit(unittest.TestCase):
    """Тесты для конструктора RatNum"""

    def test_init_normal(self):
        """Тест создания обычной дроби"""
        r = RatNum(3, 4)
        self.assertEqual(r.numerator, 3)
        self.assertEqual(r.denominator, 4)
        self.assertFalse(r.is_nan())

    def test_init_integer(self):
        """Тест создания целого числа"""
        r = RatNum(5)
        self.assertEqual(r.numerator, 5)
        self.assertEqual(r.denominator, 1)

    def test_init_negative_numerator(self):
        """Тест с отрицательным числителем"""
        r = RatNum(-3, 4)
        self.assertEqual(r.numerator, -3)
        self.assertEqual(r.denominator, 4)

    def test_init_negative_denominator(self):
        """Тест с отрицательным знаменателем (знак должен переноситься)"""
        r = RatNum(3, -4)
        self.assertEqual(r.numerator, -3)
        self.assertEqual(r.denominator, 4)

    def test_init_both_negative(self):
        """Тест с двумя отрицательными"""
        r = RatNum(-3, -4)
        self.assertEqual(r.numerator, 3)
        self.assertEqual(r.denominator, 4)

    def test_init_reduction(self):
        """Тест сокращения дроби"""
        r = RatNum(6, 8)
        self.assertEqual(r.numerator, 3)
        self.assertEqual(r.denominator, 4)

    def test_init_reduction_negative(self):
        """Тест сокращения отрицательной дроби"""
        r = RatNum(-6, 8)
        self.assertEqual(r.numerator, -3)
        self.assertEqual(r.denominator, 4)

    def test_init_zero(self):
        """Тест нуля"""
        r = RatNum(0, 5)
        self.assertEqual(r.numerator, 0)
        self.assertEqual(r.denominator, 1)

    def test_init_nan(self):
        """Тест создания NaN"""
        r = RatNum(1, 0)
        self.assertTrue(r.is_nan())


class TestRatNumProperties(unittest.TestCase):
    """Тесты для свойств и методов проверки"""

    def setUp(self):
        """Подготовка данных для тестов"""
        self.nan = RatNum(1, 0)
        self.zero = RatNum(0)
        self.positive = RatNum(3, 4)
        self.negative = RatNum(-5, 2)
        self.integer = RatNum(7)

    def test_is_nan(self):
        """Тест is_nan()"""
        self.assertTrue(self.nan.is_nan())
        self.assertFalse(self.zero.is_nan())
        self.assertFalse(self.positive.is_nan())

    def test_is_positive(self):
        """Тест is_positive()"""
        self.assertTrue(self.positive.is_positive())
        self.assertFalse(self.negative.is_positive())
        self.assertFalse(self.zero.is_positive())

        with self.assertRaises(ValueError):
            self.nan.is_positive()

    def test_is_negative(self):
        """Тест is_negative()"""
        self.assertTrue(self.negative.is_negative())
        self.assertFalse(self.positive.is_negative())
        self.assertFalse(self.zero.is_negative())

        with self.assertRaises(ValueError):
            self.nan.is_negative()

    def test_float_value(self):
        """Тест float_value()"""
        self.assertEqual(self.positive.float_value(), 0.75)
        self.assertEqual(self.negative.float_value(), -2.5)
        self.assertEqual(self.zero.float_value(), 0.0)

        import math
        self.assertTrue(math.isnan(self.nan.float_value()))

    def test_int_value(self):
        """Тест int_value()"""
        self.assertEqual(self.positive.int_value(), 0)  # 3/4 = 0
        self.assertEqual(self.negative.int_value(), -2)  # -5/2 = -2
        self.assertEqual(self.zero.int_value(), 0)
        self.assertEqual(self.integer.int_value(), 7)
        self.assertEqual(self.nan.int_value(), 0)


class TestRatNumComparison(unittest.TestCase):
    """Тесты для сравнения чисел"""

    def setUp(self):
        self.a = RatNum(3, 4)  # 0.75
        self.b = RatNum(1, 2)  # 0.5
        self.c = RatNum(-3, 4)  # -0.75
        self.nan = RatNum(1, 0)

    def test_compare_to(self):
        """Тест compare_to()"""
        self.assertEqual(self.a.compare_to(self.b), 1)  # 0.75 > 0.5
        self.assertEqual(self.b.compare_to(self.a), -1)  # 0.5 < 0.75
        self.assertEqual(self.a.compare_to(self.a), 0)  # равные

        # Сравнение с NaN
        self.assertEqual(self.nan.compare_to(self.a), 1)  # NaN > число
        self.assertEqual(self.a.compare_to(self.nan), -1)  # число < NaN
        self.assertEqual(self.nan.compare_to(self.nan), 0)  # NaN == NaN

    def test_eq(self):
        """Тест __eq__"""
        self.assertTrue(RatNum(3, 4) == RatNum(6, 8))  # сокращённые равны
        self.assertTrue(RatNum(1, 0) == RatNum(2, 0))  # NaN == NaN
        self.assertFalse(RatNum(3, 4) == RatNum(1, 2))
        self.assertFalse(RatNum(3, 4) == "not a number")


class TestRatNumArithmetic(unittest.TestCase):
    """Тесты для арифметических операций"""

    def setUp(self):
        self.a = RatNum(3, 4)  # 3/4
        self.b = RatNum(1, 2)  # 1/2
        self.c = RatNum(-5, 2)  # -5/2
        self.zero = RatNum(0)
        self.nan = RatNum(1, 0)

    def test_neg(self):
        """Тест унарного минуса"""
        self.assertEqual(-self.a, RatNum(-3, 4))
        self.assertEqual(-self.c, RatNum(5, 2))
        self.assertEqual(-self.zero, RatNum(0))
        self.assertTrue((-self.nan).is_nan())

    def test_add(self):
        """Тест сложения"""
        # 3/4 + 1/2 = 5/4
        self.assertEqual(self.a + self.b, RatNum(5, 4))
        # 3/4 + (-5/2) = 3/4 - 10/4 = -7/4
        self.assertEqual(self.a + self.c, RatNum(-7, 4))
        # с нулём
        self.assertEqual(self.a + self.zero, self.a)
        # с NaN
        self.assertTrue((self.a + self.nan).is_nan())
        self.assertTrue((self.nan + self.a).is_nan())

    def test_sub(self):
        """Тест вычитания"""
        # 3/4 - 1/2 = 1/4
        self.assertEqual(self.a - self.b, RatNum(1, 4))
        # 3/4 - (-5/2) = 3/4 + 10/4 = 13/4
        self.assertEqual(self.a - self.c, RatNum(13, 4))
        # с NaN
        self.assertTrue((self.a - self.nan).is_nan())

    def test_mul(self):
        """Тест умножения"""
        # 3/4 * 1/2 = 3/8
        self.assertEqual(self.a * self.b, RatNum(3, 8))
        # 3/4 * (-5/2) = -15/8
        self.assertEqual(self.a * self.c, RatNum(-15, 8))
        # умножение на ноль
        self.assertEqual(self.a * self.zero, RatNum(0))
        # с NaN
        self.assertTrue((self.a * self.nan).is_nan())

    def test_truediv(self):
        """Тест деления"""
        # (3/4) / (1/2) = (3/4) * (2/1) = 6/4 = 3/2
        self.assertEqual(self.a / self.b, RatNum(3, 2))
        # (3/4) / (-5/2) = -6/20 = -3/10
        self.assertEqual(self.a / self.c, RatNum(-3, 10))
        # деление на ноль даёт NaN
        self.assertTrue((self.a / RatNum(0)).is_nan())
        # с NaN
        self.assertTrue((self.a / self.nan).is_nan())


class TestRatNumStr(unittest.TestCase):
    """Тесты строкового представления"""

    def test_str(self):
        """Тест __str__"""
        self.assertEqual(str(RatNum(3, 4)), "3/4")
        self.assertEqual(str(RatNum(5)), "5")
        self.assertEqual(str(RatNum(0)), "0")
        self.assertEqual(str(RatNum(-3, 4)), "-3/4")
        self.assertEqual(str(RatNum(1, 0)), "NaN")


if __name__ == '__main__':
    unittest.main()