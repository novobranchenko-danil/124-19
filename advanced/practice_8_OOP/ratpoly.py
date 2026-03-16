from ratnum import RatNum


class RatPoly:
    """
    Класс, представляющий полином с рациональными коэффициентами.

    Поля представления (representation fields):
        _coeffs: list[RatNum] - список коэффициентов, где индекс = степень
        Например, [a₀, a₁, a₂] представляет a₀ + a₁x + a₂x²

    Инвариант представления (representation invariant):
        1. Если полином нулевой, _coeffs = [RatNum(0)]
        2. Старший коэффициент (последний в списке) != 0
        3. Нет лишних нулей в конце (последний коэффициент всегда ненулевой)

    Функция абстракции (abstraction function):
        AF(p) = Σ p._coeffs[i] * xⁱ, где i от 0 до len(p._coeffs)-1
        Если полином нулевой, это просто 0
    """

    def __init__(self, coeffs):
        """
        Создаёт полином из списка коэффициентов.

        Поля представления:
            _coeffs: list[RatNum] - коэффициенты, где индекс = степень

        Инвариант представления:
            1. Если полином нулевой, _coeffs = [RatNum(0)]
            2. Старший коэффициент (последний) != 0
            3. Нет лишних нулей в конце

        Функция абстракции:
            AF(self) = Σ self._coeffs[i] * xⁱ

        @requires:
            coeffs - список из int или RatNum

        @modifies:
            Создаёт новый объект RatPoly

        @effects:
            Создаёт полином, удаляя лишние нулевые коэффициенты
            Все int преобразуются в RatNum

        @throws:
            TypeError если элемент не int и не RatNum

        @returns:
            None
        """
        # Преобразуем int в RatNum где нужно
        normalized = []
        for c in coeffs:
            if isinstance(c, int):
                normalized.append(RatNum(c))
            elif isinstance(c, RatNum):
                normalized.append(c)
            else:
                raise TypeError("Coefficients must be int or RatNum")

        # Удаляем нули в конце (лишние старшие коэффициенты)
        while len(normalized) > 1 and normalized[-1] == RatNum(0):
            normalized.pop()

        # Если после удаления остался только ноль
        if len(normalized) == 1 and normalized[0] == RatNum(0):
            self._coeffs = [RatNum(0)]
        else:
            self._coeffs = normalized

    def __neg__(self) -> 'RatPoly':
        """
        Возвращает полином с противоположными знаками коэффициентов.

        @requires:
            None

        @modifies:
            None

        @effects:
            Возвращает новый полином -self
            Если self содержит NaN, результат NaN

        @throws:
            None

        @returns:
            RatPoly - аддитивная инверсия
        """
        new_coeffs = [-c for c in self._coeffs]
        return RatPoly(new_coeffs)

    def __str__(self) -> str:
        """
        Возвращает строковое представление полинома.

        @requires:
            None

        @modifies:
            None

        @effects:
            Форматирует полином в строку вида "3x^2 + 1/2x - 5"
            Для NaN возвращает "NaN"
            Для нуля возвращает "0"

        @throws:
            None

        @returns:
            str - строковое представление
        """
        if self.is_nan():
            return "NaN"

        if len(self._coeffs) == 1 and self._coeffs[0] == RatNum(0):
            return "0"

        terms = []
        for i, coeff in enumerate(self._coeffs):
            if coeff == RatNum(0):
                continue

            # Форматируем коэффициент
            if i == 0:
                # Свободный член
                terms.append(str(coeff))
            elif i == 1:
                # x¹
                if coeff == RatNum(1):
                    terms.append("x")
                elif coeff == RatNum(-1):
                    terms.append("-x")
                else:
                    terms.append(f"{coeff}x")
            else:
                # xⁿ
                if coeff == RatNum(1):
                    terms.append(f"x^{i}")
                elif coeff == RatNum(-1):
                    terms.append(f"-x^{i}")
                else:
                    terms.append(f"{coeff}x^{i}")

        # Собираем строку с правильными знаками
        result = terms[0]
        for term in terms[1:]:
            if term[0] == '-':
                result += term
            else:
                result += " + " + term

        return result

    def __eq__(self, other) -> bool:
        """
        Проверяет равенство двух полиномов.

        @requires:
            None

        @modifies:
            None

        @effects:
            Сравнивает все коэффициенты
            Два NaN-полинома считаются равными

        @throws:
            None

        @returns:
            bool - True если полиномы равны
        """
        if not isinstance(other, RatPoly):
            return False

        if self.is_nan() and other.is_nan():
            return True

        if self.is_nan() or other.is_nan():
            return False

        # Сравниваем коэффициенты
        max_len = max(len(self._coeffs), len(other._coeffs))
        for i in range(max_len):
            if self.get_coeff(i) != other.get_coeff(i):
                return False

        return True

    def __hash__(self) -> int:
        """
        Возвращает хэш полинома.

        @requires:
            None

        @modifies:
            None

        @effects:
            Вычисляет хэш на основе кортежа коэффициентов
            Все NaN имеют одинаковый хэш

        @throws:
            None

        @returns:
            int - хэш-значение
        """
        if self.is_nan():
            return hash(('NaN',))

        return hash(tuple(self._coeffs))

    def __add__(self, other: 'RatPoly') -> 'RatPoly':
        """
        Складывает два полинома.

        @requires:
            other является экземпляром RatPoly

        @modifies:
            None

        @effects:
            Возвращает новый полином, равный self + other
            Складывает коэффициенты при одинаковых степенях
            Если self или other содержит NaN, результат NaN

        @throws:
            TypeError если other не RatPoly

        @returns:
            RatPoly - сумма полиномов
        """
        if not isinstance(other, RatPoly):
            raise TypeError("Can only add RatPoly")

        if self.is_nan() or other.is_nan():
            # Создаём NaN-полином (один коэффициент NaN)
            return RatPoly([RatNum(1, 0)])

        # Определяем максимальную степень
        max_deg = max(len(self._coeffs), len(other._coeffs))

        # Складываем коэффициенты
        new_coeffs = []
        for i in range(max_deg):
            c1 = self.get_coeff(i)
            c2 = other.get_coeff(i)
            new_coeffs.append(c1 + c2)

        return RatPoly(new_coeffs)

    def __sub__(self, other: 'RatPoly') -> 'RatPoly':
        """
        Вычитает другой полином из текущего.

        @requires:
            other является экземпляром RatPoly

        @modifies:
            None

        @effects:
            Возвращает новый полином, равный self - other
            self - other = self + (-other)
            Если self или other содержит NaN, результат NaN

        @throws:
            TypeError если other не RatPoly

        @returns:
            RatPoly - разность полиномов
        """
        if not isinstance(other, RatPoly):
            raise TypeError("Can only subtract RatPoly")

        if self.is_nan() or other.is_nan():
            return RatPoly([RatNum(1, 0)])

        # self - other = self + (-other)
        return self + (-other)

    def __mul__(self, other: 'RatPoly') -> 'RatPoly':
        """
        Умножает два полинома.

        @requires:
            other является экземпляром RatPoly

        @modifies:
            None

        @effects:
            Возвращает новый полином, равный self * other
            Выполняет свёртку коэффициентов
            Если self или other содержит NaN, результат NaN

        @throws:
            TypeError если other не RatPoly

        @returns:
            RatPoly - произведение полиномов
        """
        if not isinstance(other, RatPoly):
            raise TypeError("Can only multiply RatPoly")

        if self.is_nan() or other.is_nan():
            return RatPoly([RatNum(1, 0)])

        # Результирующая степень = сумма степеней
        result_deg = self.degree() + other.degree()
        result = [RatNum(0) for _ in range(result_deg + 1)]

        # Свёртка
        for i, ci in enumerate(self._coeffs):
            for j, cj in enumerate(other._coeffs):
                result[i + j] = result[i + j] + (ci * cj)

        return RatPoly(result)

    def __truediv__(self, divisor):
        """
        Делит полином на скаляр.

        @requires:
            divisor - int или RatNum

        @modifies:
            None

        @effects:
            Возвращает новый полином, равный self / divisor
            Делит каждый коэффициент на divisor
            Если divisor == 0, возвращает NaN
            Если self содержит NaN, результат NaN

        @throws:
            TypeError если divisor не int и не RatNum

        @returns:
            RatPoly - частное от деления на скаляр
        """
        # Преобразуем int в RatNum если нужно
        if isinstance(divisor, int):
            divisor = RatNum(divisor)

        if not isinstance(divisor, RatNum):
            raise TypeError("Can only divide by int or RatNum")

        if self.is_nan() or divisor.is_nan():
            return RatPoly([RatNum(1, 0)])

        # Деление на ноль
        if divisor == RatNum(0):
            return RatPoly([RatNum(1, 0)])

        # Делим каждый коэффициент
        new_coeffs = [c / divisor for c in self._coeffs]

        return RatPoly(new_coeffs)

    def degree(self) -> int:
        """
        Возвращает степень полинома.

        @requires:
            None

        @modifies:
            None

        @effects:
            Определяет наибольшую степень с ненулевым коэффициентом
            Для нулевого полинома возвращает 0

        @throws:
            None

        @returns:
            int - степень полинома
        """
        return len(self._coeffs) - 1

    def get_coeff(self, deg: int) -> 'RatNum':
        """
        Возвращает коэффициент при заданной степени.

        @requires:
            deg >= 0

        @modifies:
            None

        @effects:
            Возвращает коэффициент при x^deg
            Если deg больше степени полинома, возвращает 0

        @throws:
            ValueError если deg < 0

        @returns:
            RatNum - коэффициент при x^deg
        """
        if deg < 0:
            raise ValueError("Degree cannot be negative")

        if deg >= len(self._coeffs):
            return RatNum(0)

        return self._coeffs[deg]

    def is_nan(self) -> bool:
        """
        Проверяет, содержит ли полином NaN.

        @requires:
            None

        @modifies:
            None

        @effects:
            Проверяет все коэффициенты на NaN
            Если хотя бы один коэффициент NaN, возвращает True

        @throws:
            None

        @returns:
            bool - True если полином содержит NaN
        """
        for c in self._coeffs:
            if c.is_nan():
                return True
        return False

    def scale_coeff(self, factor):
        """
        Умножает все коэффициенты на заданный множитель.

        @requires:
            factor - int или RatNum

        @modifies:
            None

        @effects:
            Возвращает новый полином с коэффициентами,
            умноженными на factor
            Если полином содержит NaN, результат NaN

        @throws:
            TypeError если factor не int и не RatNum

        @returns:
            RatPoly - масштабированный полином
        """
        # Преобразуем int в RatNum если нужно
        if isinstance(factor, int):
            factor = RatNum(factor)

        if not isinstance(factor, RatNum):
            raise TypeError("Factor must be int or RatNum")

        # Умножаем каждый коэффициент
        new_coeffs = [c * factor for c in self._coeffs]

        return RatPoly(new_coeffs)

    def eval(self, x):
        """
        Вычисляет значение полинома в точке x.

        @requires:
            x - int или RatNum

        @modifies:
            None

        @effects:
            Вычисляет P(x) по схеме Горнера
            Если полином или x содержит NaN, возвращает NaN

        @throws:
            TypeError если x не int и не RatNum

        @returns:
            RatNum - значение полинома в точке x
        """
        # Преобразуем int в RatNum если нужно
        if isinstance(x, int):
            x = RatNum(x)

        if not isinstance(x, RatNum):
            raise TypeError("x must be int or RatNum")

        if self.is_nan() or x.is_nan():
            return RatNum(1, 0)  # NaN

        # Вычисляем по схеме Горнера (эффективнее)
        # a₀ + x*(a₁ + x*(a₂ + ...))
        result = RatNum(0)
        for coeff in reversed(self._coeffs):
            result = result * x + coeff

        return result

    def differentiate(self) -> 'RatPoly':
        """
        Возвращает производную полинома.

        @requires:
            None

        @modifies:
            None

        @effects:
            Вычисляет производную: d/dx (aₙxⁿ) = n * aₙ * xⁿ⁻¹
            Для нулевого полинома возвращает [0]
            Если полином содержит NaN, результат NaN

        @throws:
            None

        @returns:
            RatPoly - производная полинома
        """
        if self.is_nan():
            return RatPoly([RatNum(1, 0)])

        if self.degree() == 0:
            # Производная константы = 0
            return RatPoly([0])

        new_coeffs = []
        for i in range(1, len(self._coeffs)):
            # Коэффициент при x^(i-1) в производной = i * aᵢ
            coeff = self._coeffs[i] * RatNum(i)
            new_coeffs.append(coeff)

        return RatPoly(new_coeffs)

    def anti_differentiate(self) -> 'RatPoly':
        """
        Возвращает первообразную полинома (без константы).

        @requires:
            None

        @modifies:
            None

        @effects:
            Вычисляет неопределённый интеграл: ∫ aₙxⁿ dx = aₙ/(n+1) * xⁿ⁺¹
            Константа интегрирования = 0
            Если полином содержит NaN, результат NaN

        @throws:
            None

        @returns:
            RatPoly - первообразная полинома
        """
        if self.is_nan():
            return RatPoly([RatNum(1, 0)])

        new_coeffs = [RatNum(0)]  # постоянный член (будет 0)

        for i, coeff in enumerate(self._coeffs):
            # ∫ aᵢ xⁱ dx = aᵢ/(i+1) * xⁱ⁺¹
            new_coeff = coeff / RatNum(i + 1)
            new_coeffs.append(new_coeff)

        return RatPoly(new_coeffs)

    def integrate(self, a, b):
        """
        Вычисляет определённый интеграл от a до b.

        @requires:
            a, b - int или RatNum

        @modifies:
            None

        @effects:
            Вычисляет ∫ₐᵇ P(x) dx = F(b) - F(a), где F - первообразная
            Если полином или пределы содержат NaN, возвращает NaN

        @throws:
            TypeError если a или b не int и не RatNum

        @returns:
            RatNum - значение определённого интеграла
        """
        # Преобразуем int в RatNum если нужно
        if isinstance(a, int):
            a = RatNum(a)
        if isinstance(b, int):
            b = RatNum(b)

        if self.is_nan() or a.is_nan() or b.is_nan():
            return RatNum(1, 0)  # NaN

        # Берём первообразную
        F = self.anti_differentiate()

        # ∫ₐᵇ P(x) dx = F(b) - F(a)
        return F.eval(b) - F.eval(a)