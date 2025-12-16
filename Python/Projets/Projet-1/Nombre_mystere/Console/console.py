from random import randint

def aleatoire():
    """
    Fonction qui retourne un nombre aléatoire entre 1 et 1000 compris
    Returns:
        int: Nombre aléatoire
    """
    return randint(1, 1000)

def saisie():
    """
    Fonction qui demande la saisie d'un nombre à l'utilisateur
    Returns:
        int: Nombre saisi par l'utilisateur
    """
    val = ""
    while val == "":
        val = input("Entrez un nombre entre 1 et 1000: ")
        try:
            nombre = int(val)
            if nombre < 1 or nombre > 1000:
                print("Veuillez entrer un nombre valide entre 1 et 1000.")
                val = ""
            else:
                return nombre
        except:
            print("Veuillez entrer un nombre valide entre 1 et 1000.")
            val = ""

def comparaison(val_saisie: int, nombre_mystere: int):
    """
    Fonction qui compare la valeur saisie avec le nombre mystère
    Args:
        val_saisie (int): Valeur entrée par l'utilisateur
        nombre_mystere (int): Valeur du nombre aléatoire
    Returns:
        str: Résultat de la comparaison
    """
    if (val_saisie > nombre_mystere):
        # Trop grand
        return "Trop grand"
    elif (val_saisie < nombre_mystere):
        # Trop petit
        return "Trop petit"
    else:
        # =
        return "Gagné"

def partie():
    """
    Fonction qui lance la partie
    """
    nombre_mystere = aleatoire()
    val_saisie = -1

    essai = 0
    while val_saisie != nombre_mystere:
        val_saisie = saisie()
        resultat = comparaison(val_saisie, nombre_mystere)
        print(resultat)
        essai += 1
    print("Félicitations ! Vous avez trouvé le nombre mystère :", nombre_mystere, " en ", essai, " essais.")

if __name__ == "__main__":
    partie()