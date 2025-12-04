def test(mot):
    i = 0
    j = len(mot) - 1
    while i < j:
        print(i, j)
        print(mot[i], mot[j]) 
        if mot[i] != mot[j]:
            return False
        i += 1
        j -= 1
    return True

print(test("kayak"))  # True
print(test("python")) # False