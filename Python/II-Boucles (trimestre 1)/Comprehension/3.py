"""
Ecrire un programme qui utilise la compréhension de liste qui permet de construire la liste L contenant le
carré des entiers de 1 à 20 exclu.
"""

L = [x**2 for x in range(1, 20) if x % 2 == 0]
print(L)