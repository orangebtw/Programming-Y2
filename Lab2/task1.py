def find_elements(nums: list[int], target: int) -> list[int]:
    for i in range(len(nums)):
        for j in range(len(nums)):
            if i == j:
                continue
            if nums[i] + nums[j] == target:
                return [i, j]
    return []


def find_elements2(nums: list[int], target: int) -> list[int]:
    visited = {}
    for i in range(len(nums)):
        visited[nums[i]] = i
        a = target - nums[i]
        if a in visited:
            return [visited[a], i]
    return []


def main():
    variant = int(input("Вариант алгоритма (0 - первый, 1 - второй): "))

    n = int(input("Кол-во элементов: "))
    arr: list[int] = list()

    for _ in range(n):
        e = int(input())
        arr.append(e)

    target = int(input("Цель: "))

    result = None

    if variant == 0:
        result = find_elements(arr, target)
    elif variant == 1:
        result = find_elements2(arr, target)
    else:
        print("Неизвестный вариант алгоритма:", variant)
        return

    if len(result) == 0:
        print("Не удалось найти элементы дающие в сумме", target)
    else:
        print("Результат:", result)


if __name__ == "__main__":
    main()
