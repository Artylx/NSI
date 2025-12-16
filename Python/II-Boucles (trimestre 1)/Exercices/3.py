def remplacer_par_indices(L):
    for i in range(len(L)):
        L[i] = i
    return L

print(remplacer_par_indices(['pomme', 'poire', 'banane']))