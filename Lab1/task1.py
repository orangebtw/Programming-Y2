def find_elements(nums: list[int], target: int) -> tuple[int, int]:
    for i in range(len(nums)):
        for j in range(len(nums)):
            if i == j: continue
            if nums[i] + nums[j] == target:
                return (i, j)
    return None

if __name__ == "__main__":
    n = int(input())

    arr: list[int] = list()

    for _ in range(n):
        e = int(input())
        arr.append(e)

    target = int(input())

    result = find_elements(arr, target)
    if result is None:
        print("Не удалось найти элементы дающие в сумме", target)
    else:
        print("Результат: [{}, {}]".format(result[0], result[1]))
