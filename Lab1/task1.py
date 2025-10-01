def find_elements(nums: list[int], target: int) -> list[int]:
    for i in range(len(nums)):
        for j in range(len(nums)):
            if i == j: continue
            if nums[i] + nums[j] == target:
                return [i, j]
    return []

if __name__ == "__main__":
    n = int(input())

    arr: list[int] = list()

    for _ in range(n):
        e = int(input())
        arr.append(e)

    target = int(input())

    result = find_elements(arr, target)
    if len(result) == 0:
        print("Не удалось найти элементы дающие в сумме", target)
    else:
        print("Результат:", result)
