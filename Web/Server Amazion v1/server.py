from flask import Flask, render_template, request, session, redirect, url_for
import logging
import json
import os

app = Flask(__name__)
app.secret_key = "a625bcb4-5c6f-431a-9084-3ccba6543c96"

def charger_produits():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    chemin_fichier = os.path.join(base_dir, "products.json")

    with open(chemin_fichier, "r", encoding="utf-8") as f:
        return json.load(f)

HEADER = ''
val_nameWebsite = "Amazion"

@app.route('/connexion/')
def connexion():
    return render_template("connexion.html", val_nameWebsite=val_nameWebsite)


@app.route('/', methods=['POST'])
def result():
    val1 = request.form['nom']
    val2 = request.form['prenom']

    # Stockage en session
    session["nom"] = val1
    session["prenom"] = val2

    return redirect(url_for("all")) 

@app.route('/')
def all():
    nom = session.get("nom")
    prenom = session.get("prenom")

    if not nom:
        return redirect(url_for("connexion"))
    
    if "panier" not in session:
        session["panier"] = []

    # Calcul du nombre d'objets dans le panier
    nb_objets_panier = len(session["panier"])

    produits = charger_produits()

    # 🔥 Filtrage des produits tendance
    produits_trend = [p for p in produits if p.get("trend") is True]

    return render_template(
        "home.html",
        nom=nom,
        prenom=prenom,
        header=HEADER,
        val_nameWebsite=val_nameWebsite,
        nb_objets_panier=nb_objets_panier,
        produits=produits_trend
    )

@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html", val_nameWebsite=val_nameWebsite, header=HEADER), 404

@app.errorhandler(500)
def server_error(e):
    # e contient l’exception si tu veux la logger

    session.clear()

    app.logger.error(f"Erreur serveur : {e}")
    return render_template("500.html", val_nameWebsite=val_nameWebsite, header=HEADER), 500

@app.route("/panier/")
def panier():
    panier_ids = session.get("panier", [])
    produits = charger_produits()

    produits_panier = []

    for id in panier_ids:
        produit = next((p for p in produits if p["id"] == id), None)
        if produit:
            produits_panier.append(produit)

    total = sum(p["prix"] for p in produits_panier)

    return render_template(
        "panier.html",
        produits_panier=produits_panier,
        total=total,
        val_nameWebsite=val_nameWebsite
    )

@app.route('/product/')
def produits():
    produits = charger_produits()
    return render_template("product.html", produits=produits, val_nameWebsite=val_nameWebsite)

@app.route('/contact/')
def contact():
    return render_template("contact.html", val_nameWebsite=val_nameWebsite)

@app.context_processor
def inject_panier_count():
    panier = session.get("panier", [])
    return dict(nb_objets_panier=len(panier))

@app.route('/logout/')
def logout():
    # Supprime toutes les données de session
    session.clear()
    # Redirige vers la page d’accueil ou formulaire
    return redirect(url_for("connexion"))

@app.route('/ajouter_product/<int:id>/', methods=['POST'])
def ajouter_panier(id):
    produits = charger_produits()
    
    produit = next((p for p in produits if p["id"] == id), None)

    if produit:
        if "panier" not in session:
            session["panier"] = []

        session["panier"].append(id)
        session.modified = True

    return redirect(url_for("produits"))

@app.route('/ajouter/<int:id>/', methods=['POST'])
def ajouter_panier_home(id):
    produits = charger_produits()
    
    produit = next((p for p in produits if p["id"] == id), None)

    if produit:
        if "panier" not in session:
            session["panier"] = []

        session["panier"].append(id)
        session.modified = True

    return redirect(url_for("all"))

@app.route("/supprimer/<int:index>")
def supprimer_produit(index):
    panier = session.get("panier", [])
    if 0 <= index < len(panier):
        panier.pop(index)
        session["panier"] = panier
        session.modified = True
    return redirect(url_for("panier"))

@app.route("/recherche")
def recherche():
    query = request.args.get("q", "").strip().lower()

    produits = charger_produits()

    if query:
        resultats = [
            p for p in produits
            if query in p["nom"].lower()
            or query in p.get("description", "").lower()
        ]
    else:
        resultats = produits

    nb_objets_panier = len(session.get("panier", []))

    return render_template(
        "product.html",
        produits=resultats,
        nb_objets_panier=nb_objets_panier,
        val_nameWebsite=val_nameWebsite,
        recherche=query
    )

app.run()
