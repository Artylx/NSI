def freq_suivante(f):
    f = 3/2*f
    if f >= 660:
        f = f/2
    return (f)

print(freq_suivante(330))