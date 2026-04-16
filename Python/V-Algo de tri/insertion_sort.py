def insertion_sort(arr):
    arr = arr.copy()

    yield arr, (-1, -1)

    for i in range(1, len(arr)):
        key = arr[i]
        j = i - 1

        while j >= 0 and arr[j] > key:
            yield arr, (j, j + 1)
            arr[j + 1] = arr[j]
            j -= 1
            yield arr, (j, j + 1)

        arr[j + 1] = key
        yield arr, (j + 1, i)