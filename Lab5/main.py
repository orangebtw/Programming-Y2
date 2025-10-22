from timeit import default_timer
from matplotlib import pyplot as plt
import timeit
import functools
import sys

sys.setrecursionlimit(5000)

def cache(func):
    cache = {}
    def wrapper(*args, **kwargs):
        if args in cache:
            return cache[args]
        result = func(*args, **kwargs)
        cache[args] = result
        return result

    return wrapper

def fact_recursive(n: int) -> int:
    if n <= 0: return 1
    return n * fact_recursive(n - 1)

def fact_iterative(n: int) -> int:
    s: int = 1
    for i in range(1, n+1):
        s *= i
    return s

@cache
def fact_recursive_memo(n: int) -> int:
    if n <= 0: return 1
    return n * fact_recursive(n - 1)

@cache
def fact_iterative_memo(n: int) -> int:
    s: int = 1
    for i in range(1, n+1):
        s *= i
    return s

def benchmark(func, data, number=1, repeat=5):
    """Возвращает среднее время выполнения func на наборе data"""
    total = 0
    for n in data:
        # несколько повторов для усреднения
        times = timeit.repeat(functools.partial(func, n), number=number, repeat=repeat)
        total += min(times)  # берём минимальное время из серии
    return total / len(data)

if __name__ == "__main__":
    # test_ns = range(100, 4000, 100)
    test_ns = range(10, 500, 10)
    benchmark_number = 1000
    benchmark_repeat = 1

    res_recursive = []
    res_iterative = []
    res_recursive_memo = []
    res_iterative_memo = []

    print("Тестирование рекурсивной функции без мемоизации...")
    for n in test_ns:
        res_recursive.append(benchmark(fact_recursive, [n], number=benchmark_number, repeat=benchmark_repeat))
    print("Тестирование итерационной функции без мемоизации...")
    for n in test_ns:
        res_iterative.append(benchmark(fact_iterative, [n], number=benchmark_number, repeat=benchmark_repeat))

    print("Тестирование рекурсивной функции с мемоизацией...")
    for n in test_ns:
        res_recursive_memo.append(benchmark(fact_recursive_memo, [n], number=benchmark_number, repeat=benchmark_repeat))

    print("Тестирование итерационной функции с мемоизацией...")
    for n in test_ns:
        res_iterative_memo.append(benchmark(fact_iterative_memo, [n], number=benchmark_number, repeat=benchmark_repeat))

    plt.plot(test_ns, res_recursive, label="Рекурсивный")
    plt.plot(test_ns, res_iterative, label="Итерационный")
    plt.plot(test_ns, res_recursive_memo, label="Рекурсивный (кэш)")
    plt.plot(test_ns, res_iterative_memo, label="Итерационный (кэш)")
    plt.xlabel("n")
    plt.ylabel("Время (сек)")
    plt.legend()
    plt.show()
