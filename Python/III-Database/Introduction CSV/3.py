import matplotlib.pyplot as plt

def tracerGraphe(temperature, precipitation):
    """
    Trace l'évolution de la température et des précipitations sur une année.
    Paramètres :
        - temperature : liste de 12 valeurs
        - precipitation : liste de 12 valeurs
    """
    # Liste des indices représentant les mois (0→Janvier,1→Février, ..., 11→Décembre)
    mois = list(range(12))
    # Liste des noms des mois affichés sur l'axe horizontal
    noms_mois = [
        'Janvier', 'Fevrier', 'Mars', 'Avril', 'Mai', 'Juin',
        'Juillet', 'Aout', 'Septembre', 'Octobre', 'Novembre', 'Décembre'
    ]

    def configurer_axes(ylabel):
        """
        Configure les éléments communs aux axes des deux graphiques.
        Paramètre :
        - ylabel : texte affiché sur l'axe vertical (dépend du graphique)
        """
        # Nom affiché sous l'axe horizontal
        plt.xlabel("mois de l'année")
        # Nom affiché à gauche, sur l'axe vertical
        plt.ylabel(ylabel)
        # Limite de l'axe horizontal (de 0 à 12 pour couvrir 12 mois)
        plt.xlim(0, 12)
        # Configuration des graduations (ticks) de l'axe horizontal :
        # - positions : 0 à 11
        # - labels : noms des mois
        # - rotation : texte vertical pour la lisibilité
        # - color : couleur du texte
        # - fontsize : taille de police
        plt.xticks(mois, noms_mois, rotation=90, color="red", fontsize=8)
        # Affiche une grille pour faciliter la lecture des valeurs
        plt.grid()

    # --- Graphique température ---
    # division de la fenêtre graphique en 1 lignes, 2 colonne,
    # graphique en position 1
    plt.subplot(1, 2, 1)
    configurer_axes("température (en °C)")
    plt.plot(mois, temperature, color="red",
             linewidth=2, marker="+", linestyle="dotted")

    # --- Graphique précipitation ---
    # graphique en position 2
    plt.subplot(1, 2, 2)
    configurer_axes("précipitation (en mm)")
    plt.plot(mois, precipitation, color="blue",
             linewidth=2, marker="+", linestyle="dotted")

    # Affiche les deux graphiques
    plt.show()

albi = [["Janvier",5.4,55.9,96.6],
["Février",6.4,53.1,118.6],
["Mars",9.3,51.5,177],
["Avril",11.8,82,183.6],
["Mai",15.9,79.9,219.3],
["Juin",19.6,64.4,244.9],
["Juillet",22.3,40.6,270.6],
["Août",22,55.9,255.7],
["Septembre",18.5,57.1,213.5],
["Octobre",14.6,65.4,154.1],
["Novembre",9,60,92.7],
["Décembre",5.9,65.1,86.8]]

def get_temp(datas):
    L = []
    for month in datas:
        L.append(month[1])
    return L

def get_precipitation(datas):
    L = []
    for month in datas:
        L.append(month[2])
    return L

tracerGraphe(get_temp(albi), get_precipitation(albi))