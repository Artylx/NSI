def est_croissante(L):
    for i in range(len(L) - 1):
        if L[i] > L[i + 1]:
            return False
    return True

print(est_croissante([1, 2, 2, 3, 4]))
print(est_croissante([1, 2, 3, 2, 4]))