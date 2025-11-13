import importlib
import subprocess
import sys

"""
Owner: ARTHUR
"""
def install_and_import(package_names):
    for package_name in package_names:
        try:
            importlib.import_module(package_name)
            print(f"[SUCESS] Le module '{package_name}' est déjà installé.")
        except ImportError:
            print(f"[WARNING] Le module '{package_name}' n'est pas installé. Installation en cours...")
            # Ici on affiche la sortie de pip (console visible)
            subprocess.check_call([sys.executable, "-m", "pip", "install", package_name])
            print(f"[SUCESS] Le module '{package_name}' a été installé avec succès.")
    print(f"[DEBUG] Fin d'installation des modules.")

try:
    install_and_import(("customtkinter", "pygame", "random", "ctypes", "pillow"))
except Exception as e:
    print(e)
    input()
    exit(1)

import customtkinter as ctk
import custom_tk as custom_tk
import pygame
import random
import ctypes
import time
import shifumi_game

pygame.mixer.init()
pygame.mixer.init(frequency=44100, size=-16, channels=2)

IMG_EXIT = "./data/exit_img.png"

IMG_CASINO = "./data/entre_casino.jpg" # 1024x640
IMG_PORTE_CASINO = "./data/entre_casino_porte.jpg" # 567x233
size_img = (1024, 640)

IMG_GAMES = "./data/games_casino.png" # 1536x1024
IMG_GAME_NB = "./data/games_casino_nb.png" # 1254 898
IMG_GAME_SHIFUMI = "./data/games_casino_shifumi.png" # 695x849

WIDTH = size_img[0]
HEIGHT = size_img[1]

DEBUG = False
print(f"[DEBUG] Debugging {DEBUG}")

root = ctk.CTk()
shifumi_game.ROOT = root
shifumi_game.SIZE_WINDOW = (WIDTH, HEIGHT)

screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

x = (screen_width // 2) - (WIDTH // 2)
y = (screen_height // 2) - (HEIGHT // 2)

root.title("Casino")
root.geometry(f"{WIDTH}x{HEIGHT}+{x}+{y}")
root.resizable(False, False)
root.iconbitmap(custom_tk.get_resource_path("./data/icon.ico"))

def music_games():
    """
    Owner: DIMITRI
    """
    pygame.mixer.music.fadeout(100)
    pygame.mixer.music.load(custom_tk.get_resource_path("data/loop_games.mp3"))
    pygame.mixer.music.play(-1)
    
def music_win_games():
    """
    Owner: TOAN
    """
    pygame.mixer.music.load(custom_tk.get_resource_path("data/win_sound.mp3"))
    pygame.mixer.music.play()

    time.sleep(3)
    pass

def music_lose_games():
    """
    Owner: DIMITRI
    """
    pygame.mixer.music.load(custom_tk.get_resource_path("data/lose_sound.mp3"))
    pygame.mixer.music.play()

    while pygame.mixer.music.get_busy():
        pass
    pass

def only_numbers(new_value):
    """
    Autorise seulement les nombres (ou vide).
    Owner: ARTHUR
    """
    return new_value.isdigit() or new_value == ""
vcmd = (root.register(only_numbers), "%P")

def afficher_text_nb(affichage_label, text: str):
    """
    Découpe un texte en lignes de maximum `max_char` caractères 
    sans couper les mots, et met à jour un label tkinter.
    Owner: ARTHUR
    """
    max_char = 17
    mots = text.split()
    lignes = []
    ligne = ""

    for mot in mots:
        if len(ligne) + len(mot) + (1 if ligne else 0) <= max_char:
            ligne += (" " if ligne else "") + mot
        else:
            lignes.append(ligne)
            ligne = mot

    if ligne:
        lignes.append(ligne)

    text_apply = "\n".join(lignes)
    affichage_label.configure(text=text_apply)

ESSAIS_NB = 0
ESSAIS_NB_MAX = 20
def comparaison_nb(nombre: int, affichage_label, nombre_aleatoire: int):
    """
    Owner: DIMITRI
    """
    global ESSAIS_NB
    ESSAIS_NB -= 1

    if (nombre > nombre_aleatoire):
        
        if ESSAIS_NB == 0:
            # Si le joueur n'a plus d'essais
            afficher_text_nb(affichage_label, f"Vous avez perdu le nombre était {nombre_aleatoire}")
            root.update()

            music_lose_games()
            return 
        else:
            afficher_text_nb(affichage_label, f"{nombre} est trop grand, essaye encore... Il reste {ESSAIS_NB} essais")
        return False
    elif (nombre < nombre_aleatoire):
        if ESSAIS_NB == 0:
            # Si le joueur n'a plus d'essais
            afficher_text_nb(affichage_label, f"Vous avez perdu le nombre était {nombre_aleatoire}")
            root.update()

            music_lose_games()
            return True
        else:
            # A
            afficher_text_nb(affichage_label, f"{nombre} est trop petit, essaye encore... Il reste {ESSAIS_NB} essais")
        return False
    else:
        afficher_text_nb(affichage_label, f"Gagné en {ESSAIS_NB_MAX - ESSAIS_NB} essais")
        root.update()

        music_win_games()
        return True
    pass

def click_btn_nb(entry, affichage_label, nombre_aleatoire, controls):
    """
    Owner: ARTHUR
    """
    if ESSAIS_NB == 0:
        return

    text = entry.get()
    try:
        nombre = int(text)
        value = comparaison_nb(nombre, affichage_label, nombre_aleatoire)
        if not value:
            entry.delete(0, "end") 
            entry.insert(0, "0")
        else:
            casino(controls)
    except Exception as e:
        print(e)
        afficher_text_nb(affichage_label, "Veuillez entrer un nombre valide")
    return

def game_mystery_nb(controls):
    """
    Owner: ARTHUR
    """
    global ESSAIS_NB

    custom_tk.remove_controls(controls)
    music_games()
    nombre_aleatoire = random.randint(1, 1000)
    ESSAIS_NB = ESSAIS_NB_MAX

    color_text = "#fcad35"
    
    img_bg = custom_tk.Create_img(root, custom_tk.get_resource_path("./data/game_nb.png"), size_img)

    pos_entry = (262, 377)
    entry = custom_tk.Create_entry(root, "", True, bg_color="#450a0e", border_color="#c7660c", border_widht=5, radius=10, font_color=color_text, fg_color="#6e0f0f", height=49, width=180, pos=pos_entry, font=("Arial", 26, "bold"))
    entry.insert(0, "0")
    entry.configure(validate="key", validatecommand=vcmd)
    

    pos_btn = (262, 440)
    imb_btn = custom_tk.Create_img(root, custom_tk.get_resource_path("./data/game_nb_btn.png"), (180, 60), pos_btn)
    imb_btn.configure(cursor="hand2")

    pos_label = (573, 255)
    affichage_label = custom_tk.Create_label(root, "", ("Arial", 24, "bold"), pos_label, bg_color="#540c12", font_color=color_text)
    afficher_text_nb(affichage_label, "Règles: Nombre mystère compris entre 1 et 1000 inclus")

    imb_btn.bind("<Button-1>", lambda e: click_btn_nb(entry, affichage_label, nombre_aleatoire, (img_bg, entry, img_bg, affichage_label, imb_btn)))

def menu_shifumi(controls):
    """
    Owner: ARTHUR
    """
    custom_tk.remove_controls(controls)
    music_games()

    img_bg = custom_tk.Create_img(root, custom_tk.get_resource_path("./data/shifumi_menu.png"), size_img) # 1536x1024

    pos_play_solo = (241, 79)
    btn_play_solo = custom_tk.Create_img(root, custom_tk.get_resource_path("./data/shifumi_menu_btn_solo.png"), (540, 150), pos_play_solo) # 1174x896 ; 809x239
    btn_play_solo.configure(cursor="hand2")

    pos_return = (262, 418)
    btn_return = custom_tk.Create_img(root, custom_tk.get_resource_path("./data/shifumi_menu_btn_return.png"), (500, 136), pos_return) # 1142x355
    btn_return.configure(cursor="hand2")

    btn_return.bind("<Button-1>", lambda e: casino((img_bg, btn_play_solo, btn_return)))
    btn_play_solo.bind("<Button-1>", lambda e: shifumi_game.start_solo((img_bg, btn_play_solo, btn_return)))
    
    pass

def open(controls):
    """
    Owner: ARTHUR
    """
    pygame.mixer.music.load(custom_tk.get_resource_path("data/porte_ouverture.mp3"))
    pygame.mixer.music.play()

    if not DEBUG:
        while pygame.mixer.music.get_busy():
            # Attendre la fin du son
            pass

    casino(controls)

def casino(controls):
    """
    Owner: ARTHUR
    """
    custom_tk.remove_controls(controls)

    pygame.mixer.music.load(custom_tk.get_resource_path("data/casino_ambiance.mp3"))
    pygame.mixer.music.play(loops=-1)

    img_casino_background = custom_tk.Create_img(root, custom_tk.get_resource_path(IMG_GAMES), size_img, (0, 0))

    pos_nb = (188, 79)
    img_casino_nb = custom_tk.Create_img(root, custom_tk.get_resource_path(IMG_GAME_NB), (210, HEIGHT - pos_nb[1]), pos=pos_nb)
    img_casino_nb.configure(cursor="hand2")

    pos_shifumi = (560, 110)
    img_casino_shifumi = custom_tk.Create_img(root, custom_tk.get_resource_path(IMG_GAME_SHIFUMI), (210, HEIGHT - pos_shifumi[1]), pos=pos_shifumi)
    img_casino_shifumi.configure(cursor="hand2")

    img_casino_nb.bind("<Button-1>", lambda e: game_mystery_nb((img_casino_background, img_casino_nb, img_casino_shifumi)))
    img_casino_shifumi.bind("<Button-1>", lambda e: menu_shifumi((img_casino_background, img_casino_nb, img_casino_shifumi)))
    pass

def start():
    """
    Owner: ARTHUR
    """
    pygame.mixer.music.load(custom_tk.get_resource_path("./data/rue_ambiance.mp3"))
    pygame.mixer.music.play(loops=-1)

    img_casino = custom_tk.Create_img(root, custom_tk.get_resource_path(IMG_CASINO), size_img, (0, 0))
    img_casino_porte = custom_tk.Create_img(root, custom_tk.get_resource_path(IMG_PORTE_CASINO), (112, 141), (457, 407))
    img_casino_porte.configure(cursor="hand2")

    img_casino_porte.bind("<Button-1>", lambda e: open((img_casino, img_casino_porte)))

    root.mainloop()

shifumi_game.FUNC_shifumi = menu_shifumi
shifumi_game.FUNC_lose = music_lose_games
shifumi_game.FUNC_win = music_win_games

hwnd = ctypes.windll.kernel32.GetConsoleWindow()
try:
    print("[DEBUG] Le jeu de lance...")

    ctypes.windll.user32.ShowWindow(hwnd, 0)
    start()
except Exception as e:
    ctypes.windll.user32.ShowWindow(hwnd, 5)
    print(e)
    input()
    exit(1)

pygame.mixer.stop()

# --icon=data/icon.ico 
# pyinstaller --onefile --icon=data/icon.ico --add-data "./data/icon_app.png;."  --name=casino --add-data "./data/shifumi_paper.png;." --add-data "./data/shifumi_bg.png;." --add-data "./data/shifumi_rock.png;." --add-data "./data/shifumi_cisers.png;." --add-data "./data/loop_games.mp3;." --add-data "./data/win_sound.mp3;." --add-data "./data/lose_sound.mp3;." --add-data "./data/game_nb.png;." --add-data "./data/game_nb_btn.png;." --add-data "./data/casino_ambiance.mp3;." --add-data "./data/porte_ouverture.wav;." --add-data "./data/rue_ambiance.mp3;." --add-data "./data/exit_img.png;." --add-data "./data/entre_casino.jpg;." --add-data "./data/entre_casino_porte.jpg;." --add-data "./data/games_casino.png;." --add-data "./data/games_casino_nb.png;." --add-data "./data/games_casino_shifumi.png;." main.py