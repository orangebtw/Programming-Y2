import functools

def my_genn():
    """Сопрограмма"""

    while True:
        number_of_fib_elem = yield
    
        l = []
        
        a = -1
        b = 1
        for _ in range(number_of_fib_elem):
            c = a + b
            a = b
            b = c
            l.append(c)
        
        yield l

def fib_coroutine(g):
    @functools.wraps(g)
    def inner(*args, **kwargs):
        gen = g(*args, **kwargs)
        gen.send(None)
        return gen
    return inner
