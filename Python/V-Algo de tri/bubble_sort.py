def bubble_sort(arr):
    arr = arr.copy()
    n = len(arr)

    yield arr, (-1, -1)

    for i in range(n):
        for j in range(n - i - 1):
            yield arr, (j, j + 1)
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
                yield arr, (j, j + 1)