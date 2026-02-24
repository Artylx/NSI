def recherche(BDD, nom):
    for acteur in BDD :
        if(acteur[0] == nom):
            return acteur[1]
    return "Il n'existe pas d'acteur au nom " + nom


BDD=[("Bogart","25/12/1899","NY"), ("Bacall","16/9/1924","NY"), ("Hawks","30/5/1896","Goshen"), ("Cooper","5/1/1975","Phidalelphie")]
nom=input("saisir un nom d'acteur")
print(recherche(BDD, nom))