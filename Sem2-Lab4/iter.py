import math
from typing import Iterable

class FibonacciIter:
    """Обычный итератор, находящий числа в коллекции, состоящие в последовательности фибоначи"""
    
    def __init__(self, container: Iterable[int]):
        self.container = container
        self.index = 0

    def __iter__(self):
        return self

    def __next__(self) -> int:        
        while True:
            if self.index >= len(self.container):
                raise StopIteration

            n = self.container[self.index]
            self.index += 1

            x1 = 5*n*n + 4
            s1 = int(math.sqrt(x1))

            if (s1*s1 == x1):
                return n
            elif n > 0:
                x2 = 5*n*n - 4
                s2 = int(math.sqrt(x2))
                if (s2*s2 == x2):
                    return n
