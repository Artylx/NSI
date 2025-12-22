import customtkinter as ctk
import sys
from PIL import Image
from pathlib import Path

def get_resource_path(relative_path):
    """Retourne le chemin absolu de la ressource embarquée ou locale."""

    if hasattr(sys, '_MEIPASS'):
        return Path(sys._MEIPASS) / relative_path
    return Path(__file__).parent / relative_path

def remove_controls(controls: list):
    """
    Fonction qui sert a faire le nettoyage des controls demandé.
    Args:
        controls (list): Liste de control à remove.
    """
    for control in controls:
        control.destroy()
    return

def Centered_pos(width, height, controlRect=(0, 0), dif=(0, 0)):
    """
    Calculer le centre d'une position à partir de la largeur et de la hauteur données,
    en tenant compte de la taille du contrôle (controlRect).
    Et également de la différence (dif) à appliquer sur les coordonnées calculées.
    Args:
        width (int): La largeur de la fenêtre ou de l'élément parent.
        height (int): La hauteur de la fenêtre ou de l'élément parent.
        controlRect (tuple): Un tuple contenant la largeur et la hauteur du contrôle (largeur, hauteur).
    """
    return ((width // 2 - controlRect[0] // 2) + dif[0], (height // 2 - controlRect[1] // 2) + dif[1])

def Create_btn(main, text, text_size=16, width=200, height=30, pos=(0, 0), pady=0, cursor="hand2", command=None):
    """
    Crée un bouton CustomTkinter avec des paramètres spécifiés.
    Args:
        main: La fenêtre ou le conteneur parent où le bouton sera placé.
        text (str): Le texte à afficher sur le bouton.
        width (int): La largeur du bouton.
        height (int): La hauteur du bouton.
        pos (tuple): Un tuple contenant les coordonnées (x, y) où le bouton sera placé.
    Returns:
        ctk.CTkButton: Le bouton créé.
    """
    button = ctk.CTkButton(main, text=text, width=width, height=height, font=ctk.CTkFont(size=text_size), cursor=cursor, command=lambda :command)
    button.place(x=pos[0], y=pos[1])
    if pady > 0:
        button.pack(pady=pady)
    return button

def Create_label(main, text, font=None, pos=(0, 0), pady=0, bg_color="transparent", font_color="white"):
    """
    Crée une étiquette CustomTkinter avec des paramètres spécifiés.
    Args:
        main: La fenêtre ou le conteneur parent où l'étiquette sera placée.
        text (str): Le texte à afficher sur l'étiquette.
        font: ctk.CTkFont(size=16, weight=None, slant=None, underline=False, overstrike=False)
        pos (tuple): Un tuple contenant les coordonnées (x, y) où l'étiquette sera placée.
        pady (int): Le padding vertical à appliquer autour de l'étiquette.
    Returns:
        ctk.CTkLabel: L'étiquette créée.
    """
    label = ctk.CTkLabel(main, text=text, font=font, bg_color=bg_color, text_color=font_color)
    label.place(x=pos[0], y=pos[1])
    if pady > 0:
        label.pack(pady=pady)
    return label

def Create_entry(main, placeholder="", disable_enter=False, char='', bg_color="white", border_color="black", border_widht=2, radius=20, font_color="black", font=None, width=200, height=30, pos=(0, 0), pady=0, fg_color="transparent"):
    """
    Crée une entrée CustomTkinter avec des paramètres spécifiés.
    Args:
        main: La fenêtre ou le conteneur parent où l'entrée sera placée.
        placeholder_text (str): Le texte d'espace réservé à afficher dans l'entrée.
        width (int): La largeur de l'entrée.
        height (int): La hauteur de l'entrée.
        pos (tuple): Un tuple contenant les coordonnées (x, y) où l'entrée sera placée.
        pady (int): Le padding vertical à appliquer autour de l'entrée.
        font: ctk.CTkFont(size=16, weight=None, slant=None, underline=False, overstrike=False)
    Returns:
        ctk.CTkEntry: L'entrée créée.
    """
    entry = ctk.CTkEntry(main, placeholder_text=placeholder, width=width, height=height, font=font, bg_color=bg_color, fg_color=fg_color, corner_radius=radius, text_color=font_color, border_color=border_color, border_width=border_widht)
    entry.place(x=pos[0], y=pos[1])
    if (disable_enter):
        def disable_enter(event):
            return "break"
        entry.bind("<Return>", disable_enter)
    if pady > 0:
        entry.pack(pady=pady)
    return entry

def Create_div(main, width=200, height=100, pos=(0, 0), pady=0):
    """
    Crée un panneau CustomTkinter avec des paramètres spécifiés.
    Args:
        main: La fenêtre ou le conteneur parent où le panneau sera placé.
        width (int): La largeur du panneau.
        height (int): La hauteur du panneau.
        pos (tuple): Un tuple contenant les coordonnées (x, y) où le panneau sera placé.
        pady (int): Le padding vertical à appliquer autour du panneau.
    Returns:
        ctk.CTkFrame: Le panneau créé.
    """
    div = ctk.CTkFrame(main, width=width, height=height)
    div.place(x=pos[0], y=pos[1])
    if pady > 0:
        div.pack(pady=pady)
    return div

def Create_img(main, image_path, size=(100, 100), pos=(0, 0), pady=0, bg="transparent"):
    """
    Crée une image CustomTkinter avec des paramètres spécifiés.
    Args:
        main: La fenêtre ou le conteneur parent où l'image sera placée.
        image_path (str): Le chemin vers l'image à afficher.
        size (tuple): Un tuple contenant la largeur et la hauteur de l'image (largeur, hauteur).
        pos (tuple): Un tuple contenant les coordonnées (x, y) où l'image sera placée.
        pady (int): Le padding vertical à appliquer autour de l'image.
        bg (str): Couleur de l'arrière plan de l'image.
    Returns:
        ctk.CTkLabel: L'étiquette contenant l'image créée.
    """
    path = get_resource_path(image_path)

    pil_img = Image.open(path).convert("RGBA")
    image = ctk.CTkImage(light_image=pil_img, dark_image=pil_img, size=size)
    label = ctk.CTkLabel(main, image=image, text="", bg_color=bg)
    label.image = image # keep a reference to avoid garbage collection
    label.place(x=pos[0], y=pos[1])
    if pady > 0:
        label.pack(pady=pady)
    return label