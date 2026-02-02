import math

class FibonacciGetItem:
    def __init__(self, container):
        self.data = [x for x in container if self._is_fib(x)]

    def _is_fib(self, n):
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

    def __getitem__(self, index):
        if index >= len(self.data):
            raise IndexError
        return self.data[index]

