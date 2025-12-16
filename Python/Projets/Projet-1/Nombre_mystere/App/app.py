import random
import tkinter as tk

def aleatoire():
    """
    Fonction qui créer un nombre aléatoire entre 1 et 1'000 compris
    Returns:
        int: Nombre aléatoire
    """
    return random.randint(1, 1000)

def afficher(text: str, label):
        """
        Fonction qui affiche un text sur le label
        Args:
            text (str): Texte a afficher
            label (Tkinter.Label): Label sur lequel afficher le texte
        """
        label.configure(text=text)
        pass

def comparaison(val_saisie: int, nombre_mystere: int, label):
    """
    Fonction qui applique la logique de la comparaison pour
    le jeu et qui le résultat à l'écran avec la fonction afficher()
    Args:
        val_saisie (int): Valeur entrée par l'utilisateur
        nombre_mystere (int): Valeur du nombre aléatoire
        label (Tkinter.Label): Label sur lequel afficher le texte
    """
    if (val_saisie > nombre_mystere):
        # Trop grand
        afficher("Trop grand", label)
    elif (val_saisie < nombre_mystere):
        # Trop petit
        afficher("Trop petit", label)
    else:
        # =
        afficher("Gagné")

def saisie_graphique(entry, nombre_mystere, label):
    """
    Fonction qui est appelée par l'entry de l'interface utilisateur
    Args:
        event: Event de l'entry
        nombre_mystere (int): Nombre mystère à deviner
        entry (Tkinter.Entry): Entry de l'interface utilisateur
    """
    text = entry.get()
    try:
        nombre = int(text)
        comparaison(nombre, nombre_mystere, label)
    except:
        afficher("Veuillez saisir un nombre", label)
        entry.delete(0, "end")

def partie():
    """
    Fonction qui lance la partie
    """
    nombre_mystere = aleatoire()

    root = tk.Tk()
    root.geometry("400x400")
    root.title("Nombre mystère")

    entry = tk.Entry(root)
    entry.pack(pady=10)

    label = tk.Label(root)
    label.pack(pady=10)

    entry.bind("<Return>", lambda e: saisie_graphique(entry, nombre_mystere, label))

    root.mainloop()

# Appel de la fonction pincipale
partie()