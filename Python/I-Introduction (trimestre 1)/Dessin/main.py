import tkinter
import random

def dessin_damier():
    pos_start = (0, 0)
    size = (20, 20)

    n_y = 13
    n_x = 30
    gap_b = size[1]
    for x in range(0, n_x, 1):
        if gap_b == size[1]:
            gap_b = 0
        else:
            gap_b = size[1]
        
        for y in range(0, n_y, 1):
            x1 = pos_start[0] + x * size[0]
            y1 = pos_start[1] + size[1] * y + size[1] * y + gap_b
            x2 = pos_start[0] + size[0] + x * size[0]
            y2 = pos_start[1] + size[1] + size[1] * y + size[1] * y + gap_b
            espace_dessin.create_rectangle(x1, y1, x2, y2, fill="red")

def dessin_cible():
    pos_start = (-200, -200)
    size_r = (700 - pos_start[0], 700 - pos_start[1])
    n_cercle = 50

    gap = size_r[0] // n_cercle

    for n in range(0, n_cercle, 1):
        color = "#%02x%02x%02x" % (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
        espace_dessin.create_oval((gap * n) / 2 + pos_start[0], (gap * n) / 2 + pos_start[1], size_r[0] - (gap * n) / 2 + pos_start[0], size_r[1] - (gap * n) / 2 + pos_start[1], fill=color)
    pass

# Construction de la fenêtre
fenetre=tkinter.Tk()
# Définition de la taille de la fenetre
fenetre.geometry("700x700")
# Titre de la fenetre
fenetre.title("Dessins")

# Construction d'un espace de dessin dans la fenetre
# L'attribut background définit la couleur de fond, l'attribut highlightbackground met une bordure
espace_dessin=tkinter.Canvas(fenetre,background="white",height=500,width=500,highlightbackground="green")

# On place l'espace dessin dans la fenêtre
espace_dessin.pack()
espace_dessin.place(x=100,y=50)
#Création d'un bouton qui appelle lors d'un clic la fonction dessin
def A():
    dessin_damier()
    # while (1) :
    #     dessin_cible()
    #     fenetre.update()

bouton=tkinter.Button(fenetre,text="  Dessiner  ",command=A)
#on insère le bouton dans la fenêtre
bouton.pack()
#on positionne le bouton dans la fenêtre
bouton.place(x=600,y=600)
# Lancement de la boucle principale qui met en marche la fenêtre et écoute les événement de la fenêtre
fenetre.mainloop()