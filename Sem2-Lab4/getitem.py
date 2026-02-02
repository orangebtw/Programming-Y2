import math
from typing import Iterable

class FibonacciGetItem:
    """Упрощённый итератор, находящий числа в коллекции, состоящие в последовательности фибоначи"""
    
    def __init__(self, container: Iterable[int]):
        self.data = [x for x in container if self._is_fib(x)]

    def _is_fib(self, n: int) -> bool:
        """Вспомогательная функция для проверки, что число состоит в последовательности фибоначи"""
        
        # A number, n, is a Fibonacci number if and only if one or both of the expressions (5 * n² + 4) or (5 * n² - 4) results in a perfect square.
        x1 = 5*n*n + 4
        s1 = int(math.sqrt(x1))

        if (s1*s1 == x1):
            return True
        elif n > 0:
            x2 = 5*n*n - 4
            s2 = int(math.sqrt(x2))
            if (s2*s2 == x2):
                return True
        
        return False

    def __getitem__(self, index: int):
        if index >= len(self.data):
            raise IndexError
        return self.data[index]

