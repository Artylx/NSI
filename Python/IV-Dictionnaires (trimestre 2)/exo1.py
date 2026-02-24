carte={
    "Albi":[("Toulouse",75)],
    "Biarritz":[("Bordeaux",193),("Toulouse",311)],
    "Bordeaux":[("Biarritz",193),("Toulouse",243)],
    "Foix":[("Toulouse",70)],
    "Narbonne":[("Toulouse",163)],
    "Toulouse":[("Albi",75),("Biarritz",311),("Bordeaux",243),("Foix",70),("Narbonne",163)]}

def voisines(ville):
    """
    La fonction reçoit en paramètre le nom d’une ville.
    Elle renvoie la liste des villes voisines,
    c’est-à-dire directement reliées par une autoroute.
    """
    return carte[ville]

def reliées(ville1,ville2):
    """
    La fonction reçoit en paramètre deux noms de ville
    Elle renvoie True si les deux villes sont directement
    reliées par une autoroute sinon elle renvoie False
    """
    for tple in carte[ville1]:
        if tple[0] == ville2:
            return True
    return False

def distance_directe(ville1, ville2):
    """
    La fonction reçoit en paramètres deux noms de ville.
    Elle renvoie la distance entre ces deux villes si elles
    sont directement reliées sinon elle renvoie -1.
    """
    for tple in carte[ville1]:
        if tple[0] == ville2:
            return tple[1]
    return -1

def plus_court_chemin(depart, arrivee):
    """
    Renvoie la distance minimale entre depart et arrivee
    en utilisant l'algorithme de Dijkstra.
    """
    # Initialisation
    distances = {}
    for ville in carte:
        distances[ville] = float("inf")
    distances[depart] = 0

    visites = []

    while True:
        # Trouver la ville non visitée avec la plus petite distance
        ville_min = None
        dist_min = float("inf")
        for ville in distances:
            if ville not in visites and distances[ville] < dist_min:
                dist_min = distances[ville]
                ville_min = ville

        if ville_min is None:
            break  # plus de villes accessibles

        if ville_min == arrivee:
            return distances[arrivee]

        visites.append(ville_min)

        # Mise à jour des distances des voisines
        for voisine, d in carte[ville_min]:
            if voisine not in visites:
                nouvelle_distance = distances[ville_min] + d
                if nouvelle_distance < distances[voisine]:
                    distances[voisine] = nouvelle_distance

    return -1  # pas de chemin
            
            

print(plus_court_chemin("Bordeaux", "Albi"))