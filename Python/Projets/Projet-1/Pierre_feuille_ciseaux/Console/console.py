from random import randint

# Initialisation des variables
choix = ("pierre", "papier", "ciseaux")
player_score = 0
computer_score = 0

# Fonctions
def aleatoire():
    """
    Fonction qui donne le résulat aléatoire choisis parmis la liste
    Returns:
        text (str): Texte du choix
    """
    return choix[randint(0, 2)].lower()

def resultat(objet_player: str, objet_computer: str):
    """
    Fonction qui affiche le résultat du duel et les scores
    Args:
        objet_player (str): Choix du joueur
        objet_computer (str): Choix de l'ordinateur
    """
    global player_score, computer_score
    print("Choix de l'ordinateur : " + objet_computer)
    if (objet_computer == objet_player):
        # Egalites
        print("Egalité.")
        return
    elif (objet_computer == choix[0] and objet_player == choix[1]) or (objet_computer == choix[1] and objet_player == choix[2]) or (objet_computer == choix[2] and objet_player == choix[0]):
        # Joueur qui gagne
        print("Gagné")
        player_score += 1
    else:
        # Ordinateur qui gagne
        print("Perdu")
        computer_score += 1

    # Afficher les scores
    print("Score:")
    print("    Vous       : " + str(player_score))
    print("    Ordinateur : " + str(computer_score))
    print("")

def jouer():
    """
    Fonction qui demande le choix a l'utilisateur
    Returns:
        text (str): Valeur choisie
    """
    val = ""
    while val == "":
        val = input("Choix (" + choix[0] + ", " + choix[1] + ", " + choix[2] + "): ").lower()
        print("")
        if val != choix[0] and val != choix[1] and val != choix[2]:
            # Le choix rentré n'est pas dans la liste de choix
            print("Veuillez entrer un choix valide.")
            val = ""
        else:
            break
    return val
        
def partie():
    """
    Fonction principale du jeu
    """
    print("Jeu [" + choix[0].upper() + " " + choix[1].upper() + " " + choix[2].upper() + "]")
    game = True

    while game:
        val_p = jouer()
        val_c = aleatoire()

        resultat(val_p, val_c)

        resp = input("Voulez vous rejouer (O/n): ").lower()
        if resp != "o":
            game = False

# Lancement du jeu
partie()