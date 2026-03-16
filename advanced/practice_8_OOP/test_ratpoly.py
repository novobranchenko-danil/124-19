import unittest
from ratnum import RatNum
from ratpoly import RatPoly


class TestRatPolyInit(unittest.TestCase):
    """Тесты для конструктора RatPoly"""

    def test_init_int_coeffs(self):
        """Тест создания с int коэффициентами"""
        p = RatPoly([1, 2, 3])
        self.assertEqual(p.get_coeff(0), RatNum(1))
        self.assertEqual(p.get_coeff(1), RatNum(2))
        self.assertEqual(p.get_coeff(2), RatNum(3))
        self.assertEqual(p.degree(), 2)

    def test_init_ratnum_coeffs(self):
        """Тест создания с RatNum коэффициентами"""
        p = RatPoly([RatNum(1,2), RatNum(3,4)])
        self.assertEqual(p.get_coeff(0), RatNum(1,2))
        self.assertEqual(p.get_coeff(1), RatNum(3,4))

    def test_init_trailing_zeros(self):
        """Тест удаления лишних нулей в конце"""
        p = RatPoly([1, 2, 0, 0, 0])
        self.assertEqual(p.degree(), 1)
        self.assertEqual(p.get_coeff(1), RatNum(2))

    def test_init_zero_poly(self):
        """Тест нулевого полинома"""
        p = RatPoly([0])
        self.assertEqual(p.degree(), 0)
        self.assertEqual(p.get_coeff(0), RatNum(0))

    def test_init_nan(self):
        """Тест создания полинома с NaN"""
        p = RatPoly([RatNum(1,0), 2])
        self.assertTrue(p.is_nan())


class TestRatPolyBasic(unittest.TestCase):
    """Тесты базовых методов"""

    def setUp(self):
        self.p1 = RatPoly([1, 2, 3])        # 1 + 2x + 3x²
        self.p2 = RatPoly([RatNum(1,2), 0, RatNum(3,4)])  # 1/2 + 3/4x²
        self.zero = RatPoly([0])

    def test_degree(self):
        """Тест degree()"""
        self.assertEqual(self.p1.degree(), 2)
        self.assertEqual(self.p2.degree(), 2)
        self.assertEqual(self.zero.degree(), 0)

    def test_get_coeff(self):
        """Тест get_coeff()"""
        self.assertEqual(self.p1.get_coeff(0), RatNum(1))
        self.assertEqual(self.p1.get_coeff(1), RatNum(2))
        self.assertEqual(self.p1.get_coeff(2), RatNum(3))
        self.assertEqual(self.p1.get_coeff(5), RatNum(0))  # вне диапазона

    def test_is_nan(self):
        """Тест is_nan()"""
        self.assertFalse(self.p1.is_nan())
        nan_poly = RatPoly([RatNum(1,0), 2])
        self.assertTrue(nan_poly.is_nan())

    def test_scale_coeff(self):
        """Тест scale_coeff()"""
        scaled = self.p1.scale_coeff(2)
        self.assertEqual(scaled.get_coeff(0), RatNum(2))
        self.assertEqual(scaled.get_coeff(1), RatNum(4))
        self.assertEqual(scaled.get_coeff(2), RatNum(6))


class TestRatPolyArithmetic(unittest.TestCase):
    """Тесты арифметических операций"""

    def setUp(self):
        self.p1 = RatPoly([1, 2, 3])        # 1 + 2x + 3x²
        self.p2 = RatPoly([1, 1])           # 1 + x
        self.zero = RatPoly([0])

    def test_neg(self):
        """Тест унарного минуса"""
        neg = -self.p1
        self.assertEqual(neg.get_coeff(0), RatNum(-1))
        self.assertEqual(neg.get_coeff(1), RatNum(-2))
        self.assertEqual(neg.get_coeff(2), RatNum(-3))

    def test_add(self):
        """Тест сложения"""
        # (1 + 2x + 3x²) + (1 + x) = 2 + 3x + 3x²
        result = self.p1 + self.p2
        self.assertEqual(result.get_coeff(0), RatNum(2))
        self.assertEqual(result.get_coeff(1), RatNum(3))
        self.assertEqual(result.get_coeff(2), RatNum(3))

        # с нулём
        self.assertEqual(self.p1 + self.zero, self.p1)

    def test_sub(self):
        """Тест вычитания"""
        # (1 + 2x + 3x²) - (1 + x) = 0 + x + 3x²
        result = self.p1 - self.p2
        self.assertEqual(result.get_coeff(0), RatNum(0))
        self.assertEqual(result.get_coeff(1), RatNum(1))
        self.assertEqual(result.get_coeff(2), RatNum(3))

    def test_mul(self):
        """Тест умножения"""
        # (1 + 2x) * (1 + x) = 1 + 3x + 2x²
        p = RatPoly([1, 2]) * RatPoly([1, 1])
        self.assertEqual(p.get_coeff(0), RatNum(1))
        self.assertEqual(p.get_coeff(1), RatNum(3))
        self.assertEqual(p.get_coeff(2), RatNum(2))

        # умножение на ноль
        self.assertEqual(self.p1 * self.zero, self.zero)

    def test_truediv(self):
        """Тест деления на скаляр"""
        result = self.p1 / 2
        self.assertEqual(result.get_coeff(0), RatNum(1,2))
        self.assertEqual(result.get_coeff(1), RatNum(1))
        self.assertEqual(result.get_coeff(2), RatNum(3,2))

        # деление на ноль
        nan_result = self.p1 / 0
        self.assertTrue(nan_result.is_nan())


class TestRatPolyAnalysis(unittest.TestCase):
    """Тесты аналитических методов"""

    def setUp(self):
        self.p1 = RatPoly([1, 2, 3])        # 1 + 2x + 3x²
        self.p2 = RatPoly([0, 1])           # x

    def test_eval(self):
        """Тест eval()"""
        x = RatNum(2)
        # 1 + 2*2 + 3*4 = 1 + 4 + 12 = 17
        self.assertEqual(self.p1.eval(x), RatNum(17))

        # в нуле
        self.assertEqual(self.p1.eval(RatNum(0)), RatNum(1))

    def test_differentiate(self):
        """Тест differentiate()"""
        # производная 1 + 2x + 3x² = 2 + 6x
        deriv = self.p1.differentiate()
        self.assertEqual(deriv.get_coeff(0), RatNum(2))
        self.assertEqual(deriv.get_coeff(1), RatNum(6))

        # производная x = 1
        self.assertEqual(self.p2.differentiate(), RatPoly([1]))

    def test_anti_differentiate(self):
        """Тест anti_differentiate()"""
        # первообразная 1 + 2x + 3x² = x + x² + x³
        integral = self.p1.anti_differentiate()
        self.assertEqual(integral.get_coeff(1), RatNum(1))   # x
        self.assertEqual(integral.get_coeff(2), RatNum(1))   # x²
        self.assertEqual(integral.get_coeff(3), RatNum(1))   # x³

    def test_integrate(self):
        """Тест integrate()"""
        # ∫₀¹ (1 + 2x + 3x²) dx = [x + x² + x³]₀¹ = 1 + 1 + 1 = 3
        result = self.p1.integrate(0, 1)
        self.assertEqual(result, RatNum(3))


class TestRatPolyStr(unittest.TestCase):
    """Тесты строкового представления"""

    def test_str(self):
        """Тест __str__"""
        self.assertEqual(str(RatPoly([1, 2, 3])), "1 + 2x + 3x^2")
        self.assertEqual(str(RatPoly([-1, -2, -3])), "-1-2x-3x^2")
        self.assertEqual(str(RatPoly([0])), "0")
        self.assertEqual(str(RatPoly([5])), "5")
        self.assertEqual(str(RatPoly([1, 0, 3])), "1 + 3x^2")  # пропуск нулевого члена
        self.assertEqual(str(RatPoly([RatNum(1,2), RatNum(2,3)])), "1/2 + 2/3x")


class TestRatPolyEq(unittest.TestCase):
    """Тесты сравнения"""

    def test_eq(self):
        """Тест __eq__"""
        self.assertTrue(RatPoly([1, 2, 3]) == RatPoly([1, 2, 3]))
        self.assertTrue(RatPoly([1, 2, 0]) == RatPoly([1, 2]))  # одинаковые после удаления нулей
        self.assertFalse(RatPoly([1, 2]) == RatPoly([1, 3]))
        self.assertFalse(RatPoly([1, 2]) == "not a poly")


if __name__ == '__main__':
    unittest.main()