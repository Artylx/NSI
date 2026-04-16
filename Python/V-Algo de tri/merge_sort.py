def merge_sort(arr):
    arr = arr.copy()
    yield from merge_sort_recursive(arr, 0, len(arr) - 1)
    yield arr, (-1, -1)


def merge_sort_recursive(arr, left, right):
    if left >= right:
        return

    mid = (left + right) // 2

    yield from merge_sort_recursive(arr, left, mid)
    yield from merge_sort_recursive(arr, mid + 1, right)
    yield from merge(arr, left, mid, right)


def merge(arr, left, mid, right):
    left_part = arr[left:mid + 1]
    right_part = arr[mid + 1:right + 1]

    i = j = 0
    k = left

    while i < len(left_part) and j < len(right_part):
        # Visualisation comparaison
        yield arr, (left + i, mid + 1 + j)

        if left_part[i] <= right_part[j]:
            arr[k] = left_part[i]
            i += 1
        else:
            arr[k] = right_part[j]
            j += 1

        # Visualisation écriture
        yield arr, (k, k)
        k += 1

    while i < len(left_part):
        arr[k] = left_part[i]
        yield arr, (k, k)
        i += 1
        k += 1

    while j < len(right_part):
        arr[k] = right_part[j]
        yield arr, (k, k)
        j += 1
        k += 1