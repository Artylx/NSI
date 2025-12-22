# IMPORTS
import random

# CONSTANTS
SIZE_MAP = 10
NUMBER_DEFAULT = 0
NUMBER_COFFRE = 1
NUMBER_GOUFFRE = -1

# VARIABLES
MAP = None
position_player = (0, 0)
PLAYER_STR = "P"
pos_discovered = set()

# FUNCTIONS
def nouvelleGrille(size=SIZE_MAP):
    """
    Crée une nouvelle grille de jeu.
    Args:
        size (int): La taille de la grille (par défaut SIZE_MAP).
    Returns:
        list: Une grille de taille SIZE_MAP x SIZE_MAP remplie de zéros.
    """
    return [[NUMBER_DEFAULT for _ in range(size)] for _ in range(size)]

def afficherGrille(grille):
    """
    Affiche la grille de jeu dans la console.
    Args:
        grille (list): La grille à afficher.
    """
    for i in range(len(grille)):
        print("-" * (len(grille[i]) * 4 + 1), i)
        for col_index, cell in enumerate(grille[i]):

            if (i, col_index) == position_player:
                print(f"| {PLAYER_STR} ", end="")
            elif (i, col_index) in pos_discovered:
                if cell == NUMBER_COFFRE:
                    print("| C ", end="")
                elif cell == NUMBER_GOUFFRE:
                    print("| G ", end="")
                else:
                    print("|   ", end="")
            else:
                print("| ? ", end="")

        print("|")
    print("-" * (len(grille[0]) * 4 + 1))

def placerGouffres(grille, nombre_gouffres=5, value=-1):
    """
    Place des gouffres aléatoirement dans la grille.
    Args:
        grille (list): La grille de jeu.
        nombre_gouffres (int): Le nombre de gouffres à placer.
    """
    size = len(grille)
    placed = 0
    while placed < nombre_gouffres:
        x = random.randint(0, size - 1)
        y = random.randint(0, size - 1)
        if grille[x][y] == NUMBER_DEFAULT:
            grille[x][y] = value
            placed += 1

def placerCoffres(grille, nombre_coffres=3, value=1, size_coffres=2):
    """
    Place des coffres aléatoirement dans la grille.
    Args:
        grille (list): La grille de jeu.
        nombre_coffres (int): Le nombre de gouffres à placer.
    """
    size = len(grille)
    placed = 0
    while placed < nombre_coffres:
        can_place = True

        x = random.randint(0, size - 2)
        y = random.randint(0, size - 2)
        for _ in range(size_coffres):
           if grille[x][y] != NUMBER_DEFAULT or grille[x + _][y] != NUMBER_DEFAULT or grille[x][y + _] != NUMBER_DEFAULT or grille[x + _][y + _] != NUMBER_DEFAULT:
                can_place = False

        if can_place:
            for _ in range(size_coffres):
                grille[x + _][y] = value
                grille[x][y + _] = value
                grille[x + _][y + _] = value
            placed += 1

def saisiePosition():
    """
    Demande la saisie a l'utilisateir pour une position dans la grille.
    """
    global position_player
    while True:
        print("Saisir ou vous voulez aller: Haut, Bas, Gauche, Droite.")
        input_str = input("Votre choix: ").strip().lower()

        if (input_str == "haut"):
            position_player = (max(0, position_player[0] - 1), position_player[1])
        elif (input_str == "bas"):
            position_player = (min(SIZE_MAP - 1, position_player[0] + 1), position_player[1])
        elif (input_str == "gauche"):
            position_player = (position_player[0], max(0, position_player[1] - 1))
        elif (input_str == "droite"):
            position_player = (position_player[0], min(SIZE_MAP - 1, position_player[1] + 1))
        else:
            print("Direction invalide. Veuillez saisir Haut, Bas, Gauche ou Droite.")
            continue
        break

    print(f"Vous allez en {input_str}. Nouvelle position: {position_player}")

def verifierCase(grille, ligne, colonne):
    """
    Vérifie le contenu d'une case dans la grille.
    Args:
        grille (list): La grille de jeu.
        ligne (int): La ligne de la case.
        colonne (int): La colonne de la case.
    """

    case = grille[ligne][colonne]
    pos_discovered.add((ligne, colonne))
    if case == NUMBER_COFFRE:
        print("Vous avez trouvé un quart de coffre!")
    elif case == NUMBER_GOUFFRE:
        print("Vous êtes tombé dans un gouffre! Game Over.")
        return False
    else:
        print("Rien ici. Continuez votre exploration.")
    return True

def start_game():
    """
    Démarre le jeu.
    """
    global MAP
    MAP = nouvelleGrille()
    placerGouffres(MAP)
    placerCoffres(MAP)

    game_over = False
    verifierCase(MAP, position_player[0], position_player[1])
    while not game_over:
        afficherGrille(MAP)
        saisiePosition()
        game_over = not verifierCase(MAP, position_player[0], position_player[1])

if __name__ == "__main__":
    start_game()