def quick_sort(arr):
    arr = arr.copy()
    yield from quick_sort_recursive(arr, 0, len(arr) - 1)
    yield arr, (-1, -1)


def quick_sort_recursive(arr, low, high):
    if low < high:
        pivot_index = yield from partition(arr, low, high)

        yield from quick_sort_recursive(arr, low, pivot_index - 1)
        yield from quick_sort_recursive(arr, pivot_index + 1, high)


def partition(arr, low, high):
    pivot = arr[high]
    i = low - 1

    for j in range(low, high):
        yield arr, (j, high)

        if arr[j] < pivot:
            i += 1
            arr[i], arr[j] = arr[j], arr[i]
            yield arr, (i, j)

    arr[i + 1], arr[high] = arr[high], arr[i + 1]
    yield arr, (i + 1, high)

    return i + 1