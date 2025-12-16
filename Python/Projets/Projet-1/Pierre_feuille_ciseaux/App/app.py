from random import randint
import tkinter as tk
from PIL import Image, ImageTk

# Variables basiques
PIERRE = 0
PAPIER = 1
CISEAUX = 2

score_player = 0
score_computer = 0

HEIGHT_ROOT = 600
WIDTH_ROOT = 600

PIERRE_PATH = "\\pierre_img.png"
CISEAUX_PATH = "\\ciseaux_img.png"
PAPIER_PATH = "\\feuille_img.png"

centered_x = WIDTH_ROOT // 2 - 100 // 2
gap = 170 # 170px

# Fonctions générales
def create_img(master, img_path, resize=(100, 100), racne_path="C:\\Users\\PC-Portable-Arthur\\Desktop\\NSI\\Python\\I-Introduction\\Projet-1\\Pierre_feuille_ciseaux\\App", cursor="hand2"):
    """
    Fonction simple permettant de créer une image Tkinter à partir d'un label
    Args:
        master (tk): La fenêtre ou le conteneur parent où l'étiquette sera placée.
        img_path (str): Chemin de l'image.
        resize (tuple): Taille de redimensionnement de l'image.
        racine_path (str): Racine du projet.
        cursor (str): Curseur utilisé lors du survol de l'image.
    Returns:
        tk.Label: Image plaçable créer.
    """
    img = Image.open(racne_path + img_path)
    img = img.resize(resize, Image.LANCZOS)
    tk_img = ImageTk.PhotoImage(img)
    label = tk.Label(master, image=tk_img, cursor=cursor)
    label.image = tk_img
    return label

def create_label(master, text="", font=("Arial", 18, "bold", "italic")):
    """
    Crée un text Tkinter avec des paramètres spécifiés.
    Args:
        master (tk): La fenêtre ou le conteneur parent où l'étiquette sera placée.
        text (str): Le texte à afficher sur l'étiquette.
        font: Police (tuple ou tkFont.Font). Exemple: ("Arial", 16, "bold").
    Returns:
        tk.Label: Texte créer.
    """
    label = tk.Label(master, text=text, font=font)
    return label

def Create_btn(master, text, width=200, height=30, cursor="hand2"):
    """
    Crée un bouton CustomTkinter avec des paramètres spécifiés.
    Args:
        master (tk): La fenêtre ou le conteneur parent où le bouton sera placée.
        text (str): Le texte à afficher sur le bouton.
        width (int): La largeur du bouton.
        height (int): La hauteur du bouton.
    Returns:
        tk.Button(): Le bouton créé.
    """
    button = tk.Button(master, text=text, width=width, height=height, font=("Arial", 16), cursor=cursor)
    return button

# Fonctions du jeu
def get_path(choix: int):
    """
    Fonction qui sert a récupérer le path de l'image en fonction du choix
    Args:
        choix (int): Choix
    Returns:
        path (str): Chemin de l'image
    """
    if (choix == PIERRE):
        return PIERRE_PATH
    elif (choix == PAPIER):
        return PAPIER_PATH
    else:
        return CISEAUX_PATH

def choix_ordinateur(master):
    """
    Génère le choix de l'ordinateur. 
    Met en évidence visuellement le choix dans l'interface (Images ???)
    Args:
        master (tk): La fenêtre ou le conteneur parent où l'étiquette sera placée.
    Returns:
        Valeurs multiples:
            Choix (int): Valeur aléatoire de l'ordinteur
            Image (tk.Label()): Label affiché pour le choix
    """
    choix = randint(0, 2)

    label_computer_choice = create_img(master, get_path(choix), cursor="arrow")
    label_computer_choice.place(x=centered_x + WIDTH_ROOT // 3, y=gap // 2 - 100 // 4)
    return choix, label_computer_choice

def choix_joueur(event, choix: int, lb_rock, lb_paper, lb_cisers, master):
    """
    Récupère le choix du joueur à partir d'un champ de saisie.
    Met à jour l'affichage graphique du choix (Images ???)
    Affiche le résultat avec resultat()
    Args:
        event: Event de la command (Pas utilisé ici).
        choix (int): Choix du joueur.
        lb_rock (tk.Label()): Label avec l'image de la pierre du joueur.
        lb_paper (tk.Label()): Label avec l'image du papier du joueur.
        lb_cisers (tk.Label()): Label avec l'image des ciseaux du joueur.
        master (tk): La fenêtre ou le conteneur parent où l'étiquette sera placée.
    """
    lb_rock.place_forget()
    lb_paper.place_forget()
    lb_cisers.place_forget()

    label_player_choice = create_img(master, get_path(choix), cursor="arrow")
    label_player_choice.place(x=centered_x + WIDTH_ROOT // 3, y=HEIGHT_ROOT - gap * 1.7 - 100 // 4)

    choix_computer, label_computer_choice = choix_ordinateur(master)

    resultats(master, choix, choix_computer, label_player_choice, label_computer_choice)

def quit_btn():
    exit(0)
    pass

def restart_btn(label_score, label_img_player, label_img_computer, button_restart, button_quit, label_result):
    """
    Fonction appelé par le bouton rejouer
    Args:
        label_score (tk.Label()): Texte a supprimé lors du restart de la partie.
        label_img_player (tk.Label()): Image a supprimé lors du restart de la partie.
        label_img_computer (tk.Label()): Image a supprimé lors du restart de la partie.
        button_restart (tk.Button()): Bouton a supprimé lors du restart de la partie.
        button_quit (tk.Button()): Bouton a supprimé lors du restart de la partie.
        label_result (tk.Label()): Texte a supprimé lors du restart de la partie.
    """

    # Suppression des anciens labels
    label_score.destroy()
    label_img_player.destroy()
    label_img_computer.destroy()
    button_restart.destroy()
    button_quit.destroy()
    label_result.destroy()

    start()
    pass

def show_end_btn(master, label_score, label_img_player, label_img_computer, label_result):
    """
    Fonction qui affiche le bouton restart et le bouton quitter
    Args:
        master (tk): La fenêtre ou le conteneur parent où l'étiquette sera placée.
        label_score (tk.Label()): Texte a supprimé lors du restart de la partie.
        label_img_player (tk.Label()): Image a supprimé lors du restart de la partie.
        label_img_computer (tk.Label()): Image a supprimé lors du restart de la partie.
        label_result (tk.Label()): Texte a supprimé lors du restart de la partie.
    """

    btn_quit = Create_btn(master, "Quitter", width=8, height=2)
    btn_quit.configure(background="red")
    btn_restart = Create_btn(master, "Rejouer", width=8, height=2)
    btn_restart.configure(background="green")

    btn_quit.configure(command=quit_btn)
    btn_restart.configure(command=lambda: restart_btn(label_score, label_img_player, label_img_computer, btn_restart, btn_quit, label_result))

    btn_quit.place(x=WIDTH_ROOT - gap, y=HEIGHT_ROOT - gap + 80)
    btn_restart.place(x=WIDTH_ROOT - gap, y=HEIGHT_ROOT - gap)

def resultats(master, choix_player, choix_computer, label_img_player, label_img_computer):
    """
    Fonctions qui affiche le résultat
    qui met à jour les scores et qui affiche le bouton restart
    Args:
        master (tk): La fenêtre ou le conteneur parent où l'étiquette sera placée.
        choix_player (int): Choix du joueur.
        choix_computer (int): Choix aléatoire.
        label_img_player (tk.Label()): Image a supprimé lors du restart de la partie.
        label_img_computer (tk.Label()): Image a supprimé lors du restart de la partie.
    Returns:

    """
    global score_computer, score_player

    if (choix_player == choix_computer):
        # Egalite
        text = "Egalité"
    elif (choix_player == PIERRE and choix_computer == CISEAUX) or (choix_player == PAPIER and choix_computer == PIERRE) or (choix_player == CISEAUX and choix_computer == PAPIER):
        # Joueur qui gagne
        text = "Gagné"
        score_player += 1
    else:
        # Ordinateur qui gagne
        text = "Perdu"
        score_computer += 1

    label_result = create_label(master, text, ("Arial", 32))
    label_result.place(x=centered_x - 15, y=gap + 20)

    label_score = create_label(master, "Score\nVous: " + str(score_player) + "\nOrdinateur: " + str(score_computer), ("Arial", 22))
    label_score.place(x=gap // 2, y=HEIGHT_ROOT - gap)

    show_end_btn(master, label_score, label_img_player, label_img_computer, label_result)

LABEL_ROCK = None
LABEL_CISERS = None
LABEL_PAPER = None

def start(label_rock=None, label_cisers=None, label_paper=None):
    """
    Fonction qui affiche les images de départ et qui caches les autres images.
    Args:
        lb_rock (tk.Label()): Label avec l'image de la pierre du joueur.
        lb_paper (tk.Label()): Label avec l'image du papier du joueur.
        lb_cisers (tk.Label()): Label avec l'image des ciseaux du joueur.
    """
    global LABEL_ROCK, LABEL_CISERS, LABEL_PAPER

    if not LABEL_ROCK:
        LABEL_ROCK = label_rock
    LABEL_ROCK.place(x=centered_x, y=HEIGHT_ROOT - gap)

    if not LABEL_CISERS:
        LABEL_CISERS = label_cisers
    LABEL_CISERS.place(x=centered_x + gap, y=HEIGHT_ROOT - gap)

    if not LABEL_PAPER:
        LABEL_PAPER = label_paper
    LABEL_PAPER.place(x=centered_x - gap, y=HEIGHT_ROOT - gap)

def creer_interface():
    """
    Met en place la fenêtre graphique, les boutons, les zones de saisie et d'affichage.
    Gère la boucle principale de l'application
    Args:

    """
    root = tk.Tk()
    root.title("Jeu pierre feuille ciseau")
    root.geometry(str(HEIGHT_ROOT) + "x" + str(WIDTH_ROOT))
    root.resizable(False, False)

    label_rock = create_img(root, PIERRE_PATH)
    label_cisers = create_img(root, CISEAUX_PATH)
    label_paper = create_img(root, PAPIER_PATH)

    start(label_rock=label_rock, label_cisers=label_cisers, label_paper=label_paper)

    label_rock.bind("<Button-1>", lambda e: choix_joueur(e, PIERRE, label_rock, label_paper, label_cisers, root))
    label_cisers.bind("<Button-1>", lambda e: choix_joueur(e, CISEAUX, label_rock, label_paper, label_cisers, root))
    label_paper.bind("<Button-1>", lambda e: choix_joueur(e, PAPIER, label_rock, label_paper, label_cisers, root))

    label_title_player = create_label(root, "Votre choix : ", ("Arial", 28))
    label_title_player.place(x=centered_x - WIDTH_ROOT // 4, y=HEIGHT_ROOT - gap * 1.7)

    label_title_computer = create_label(root, "Choix de l'ordinateur : ", ("Arial", 28))
    label_title_computer.place(x=centered_x - WIDTH_ROOT // 3, y=gap // 2)

    root.mainloop()
    return

creer_interface()