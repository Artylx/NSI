import customtkinter as ctk
import custom_tk
import random

# Variables globals
ROCK = 0
PAPER = 1
CISERS = 2

P_PLAYER = 0
P_COMPUTER = 0

ROOT = None
SIZE_WINDOW = (0, 0)
FUNC_shifumi = None
FUNC_lose = None
FUNC_win = None

IMG_ROCK = "./data/shifumi_rock_empty.png"

# Func
def result_solo(choice, controls):
    global P_COMPUTER, P_PLAYER
    custom_tk.remove_controls(controls)

    choice_computer = random.randint(0, 2)

    img_bg = custom_tk.Create_img(ROOT, custom_tk.get_resource_path("./data/shifumi_bg_result.png"), SIZE_WINDOW)

    label_title_u = custom_tk.Create_label(ROOT, "Vous", ("Arial", 32, "bold"), (235, 220), bg_color="#01193C", font_color="#13CDFE")
    label_title_computeur = custom_tk.Create_label(ROOT, "Ordinateur", ("Arial", 32, "bold"), (670, 220), bg_color="#01193C", font_color="#13CDFE")

    pos_result_player = (170, 307)
    result_p_img = None
    if choice == ROCK:
        result_p_img = custom_tk.Create_img(ROOT, custom_tk.get_resource_path("./data/shifumi_rock.png"), (215, 237), pos_result_player)
    elif choice == PAPER:
        result_p_img = custom_tk.Create_img(ROOT, custom_tk.get_resource_path("./data/shifumi_paper.png"), (215, 237), pos_result_player)
    elif choice == CISERS:
        result_p_img = custom_tk.Create_img(ROOT, custom_tk.get_resource_path("./data/shifumi_cisers.png"), (215, 237), pos_result_player)

    pos_result_c = (650, 307)
    result_c_img = None
    if choice_computer == ROCK:
        result_c_img = custom_tk.Create_img(ROOT, custom_tk.get_resource_path("./data/shifumi_rock.png"), (215, 237), pos_result_c)
    elif choice_computer == PAPER:
        result_c_img = custom_tk.Create_img(ROOT, custom_tk.get_resource_path("./data/shifumi_paper.png"), (215, 237), pos_result_c)
    elif choice_computer == CISERS:
        result_c_img = custom_tk.Create_img(ROOT, custom_tk.get_resource_path("./data/shifumi_cisers.png"), (215, 237), pos_result_c)
    
    label_result = None
    if (choice == choice_computer):
        # Egalité
        label_result = custom_tk.Create_label(ROOT, "Egalité", ("Arial", 40, "bold"), (397, 350), bg_color="#01193C", font_color="#13CDFE")
        
        ROOT.update()
        FUNC_lose()
    elif (choice == ROCK and choice_computer == CISERS) or (choice == CISERS and choice_computer == PAPER) or (choice == PAPER and choice_computer == ROCK):
        # Win player
        P_PLAYER += 1
        label_result = custom_tk.Create_label(ROOT, "Gagné", ("Arial", 40, "bold"), (397, 350), bg_color="#01193C", font_color="#13CDFE")

        ROOT.update()
        FUNC_win()
    else:
        # Win computer
        P_COMPUTER += 1
        label_result = custom_tk.Create_label(ROOT, f"Perdu\nOrdinateur: {P_COMPUTER }\nVous: {P_PLAYER}", ("Arial", 40, "bold"), (397, 350), bg_color="#01193C", font_color="#13CDFE")

        ROOT.update()
        FUNC_lose()

    FUNC_shifumi((img_bg, label_title_u, label_title_computeur, result_p_img, result_c_img, label_result))
    pass

def start_solo(controls_remove):
    custom_tk.remove_controls(controls_remove)

    if not ROOT:
        return False

    img_bg = custom_tk.Create_img(ROOT, custom_tk.get_resource_path("./data/shifumi_bg.png"), SIZE_WINDOW)

    pos_btn_rock = (160, 307)
    btn_rock = custom_tk.Create_img(ROOT, custom_tk.get_resource_path("./data/shifumi_rock.png"), (215, 237), pos_btn_rock)
    btn_rock.configure(cursor="hand2")

    pos_btn_paper = (402, 307)
    btn_paper = custom_tk.Create_img(ROOT, custom_tk.get_resource_path("./data/shifumi_paper.png"), (215, 237), pos_btn_paper)
    btn_paper.configure(cursor="hand2")

    pos_btn_cisers = (647, 307)
    btn_cisers = custom_tk.Create_img(ROOT, custom_tk.get_resource_path("./data/shifumi_cisers.png"), (215, 237), pos_btn_cisers)
    btn_cisers.configure(cursor="hand2")

    btn_rock.bind("<Button-1>", lambda e: result_solo(ROCK, (img_bg, btn_rock, btn_cisers, btn_paper)))
    btn_paper.bind("<Button-1>", lambda e: result_solo(PAPER, (img_bg, btn_rock, btn_cisers, btn_paper)))
    btn_cisers.bind("<Button-1>", lambda e: result_solo(CISERS, (img_bg, btn_rock, btn_cisers, btn_paper)))
