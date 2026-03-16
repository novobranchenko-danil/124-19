class Fibo:
    """
    Итератор, перечисляющий числа Фибоначчи.

    Последовательность: 0, 1, 1, 2, 3, 5, 8, 13, ...

    @requires:
        None

    @modifies:
        Создаёт новый объект Fibo

    @effects:
        Устанавливает начальные значения: a = 0, b = 1
    """

    def __init__(self):
        """
        Инициализирует итератор чисел Фибоначчи.

        @requires:
            None

        @modifies:
            Создаёт новый объект Fibo

        @effects:
            Устанавливает начальные значения: a = 0, b = 1
        """
        self._a = 0
        self._b = 1

    def __iter__(self):
        """
        Возвращает сам итератор.

        @requires:
            None

        @modifies:
            None

        @returns:
            self - итератор
        """
        return self

    def __next__(self):
        """
        Возвращает следующее число Фибоначчи.

        @requires:
            None

        @modifies:
            Обновляет внутреннее состояние (a, b)

        @returns:
            int - следующее число Фибоначчи
        """
        result = self._a
        self._a, self._b = self._b, self._a + self._b
        return result


def integers():
    """
    Генератор, перечисляющий все неотрицательные целые числа.

    Последовательность: 0, 1, 2, 3, 4, ...

    @requires:
        None

    @yields:
        int - следующее неотрицательное целое число
    """
    i = 0
    while True:
        yield i
        i += 1


def primes():
    """
    Генератор, перечисляющий все простые числа.

    Последовательность: 2, 3, 5, 7, 11, 13, 17, ...

    @requires:
        None

    @yields:
        int - следующее простое число
    """
    primes_list = []
    n = 2

    while True:
        is_prime = True
        for p in primes_list:
            if p * p > n:
                break
            if n % p == 0:
                is_prime = False
                break

        if is_prime:
            primes_list.append(n)
            yield n

        n += 1


if __name__ == "__main__":
    print("=== Fibo ===")
    fib = Fibo()
    for _ in range(10):
        print(next(fib), end=" ")
    print()

    print("\n=== integers ===")
    ints = integers()
    for _ in range(10):
        print(next(ints), end=" ")
    print()

    print("\n=== primes ===")
    prime_gen = primes()
    for _ in range(10):
        print(next(prime_gen), end=" ")
    print()
