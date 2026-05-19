from flask import Config, Flask, render_template, request, session, redirect, url_for
import json
import os
from datetime import datetime

from dataBase import Product_DataBase, User_DataBase
from config import Config

app = Flask(__name__)
conf = Config()

product_database = Product_DataBase(conf.get_value("product_database_path", "./products.json"))
user_database = User_DataBase(conf.get_value("user_database_path", "./users.json"))

def log(text: str, type="info") -> None:
    """
    Fonction qui affiche un message dans la console avec une couleur différente selon le type (info, erreur, etc.).
    Paramètres:
        text: Le message à afficher
        type: Le type de message (info, erreur, etc.)

    Exemple d'utilisation :
    log("Le serveur a démarré avec succès.", "info")
    """
    import colorama

    color = colorama.Fore.WHITE
    if type == "info":
        color = colorama.Fore.BLUE
    elif type == "erreur":
        color = colorama.Fore.RED
    elif type == "success":
        color = colorama.Fore.GREEN
    elif type == "warning":
        color = colorama.Fore.YELLOW

    print(f"{color}[{type.upper()}]{colorama.Fore.RESET} {text}")

# Get de la clé secrette
secret_key = conf.get_value("secret_key")
if secret_key:
    app.secret_key = secret_key
else:
    log("Il manque la clé secrette. Arrêt du serveur.", "erreur")
    exit(1)

# Fonction du server

def create_session(email: str, password: str) -> None:
    session["email"] = email
    session["password"] = password
    session["panier"] = []

def is_logged_in() -> bool:
    if "email" in session and "password" in session:
        email = session["email"]
        password = session["password"]
        
        if user_database.try_login(email, password):
            return True
    return False

def destroy_session() -> None:
    session.pop("email", None)
    session.pop("password", None)
    session.pop("panier", None)

def render_template_with_common(template_name: str, title_page: str = "", **context) -> str:
    """
    Fonction qui rend un template en y ajoutant les variables communes à tous les templates.
    Paramètres:
        template_name: Le nom du template à rendre
        title_page: Le titre de la page
        context: Les variables à passer au template

    Exemple d'utilisation :
    render_template_with_common("home.html", nom=nom, prenom=prenom)
    """
    common_context = {
        "val_nameWebsite": conf.get_value("name_website", "Amazion"),
        "nb_objets_panier": sum(item["qty"] for item in session.get("panier", [])),
        "val_titlePage": title_page
    }
    context.update(common_context)
    return render_template("content/" + template_name, **context)

@app.route('/')
def home():

    if not is_logged_in():
        return redirect(url_for("connection_page"))

    query = request.args.get("q", "").lower()

    produits = product_database.get_products()

    if query:
        produits = [
            p for p in produits
            if query in p["nom"].lower()
        ]

    return render_template_with_common(
        "home.html",
        title_page="Accueil",
        produits=produits,
        search=query
    )

# PARTIE EVAN


@app.route('/login/', methods=['POST'])
def connection_post():
    email = request.form['mail']
    password = request.form['password']

    if user_database.try_login(email, password):
        create_session(email, password)
        return redirect(url_for("home"))
    else:
        return render_template_with_common("connect.html", title_page="Connexion", error="Email ou mot de passe incorrect.")

@app.route('/login/')
def connection_page():
    return render_template_with_common("connect.html", title_page="Connexion")

@app.route('/logout/')
def logout_page():
    destroy_session()
    return redirect(url_for("connection_page"))


# FIN PARTIE EVAN

@app.route('/add-to-cart/<int:product_id>')
def add_to_cart(product_id):
    if not is_logged_in():
        return redirect(url_for("connection_page"))

    produits = product_database.get_products()

    produit = next((p for p in produits if p["id"] == product_id), None)

    if produit is None:
        return redirect(url_for("home"))

    panier = session.get("panier", [])

    for item in panier:
        if item["product_id"] == product_id:
            item["qty"] += 1
            break
    else:
        panier.append({
            "product_id": product_id,
            "qty": 1
        })

    session["panier"] = panier

    return redirect(url_for("home"))

@app.route('/cart/')
def cart_page():

    if not is_logged_in():
        return redirect(url_for("connection_page"))

    panier = session.get("panier", [])

    produits_db = product_database.get_products()

    panier_complet = []

    for item in panier:

        produit = next(
            (p for p in produits_db if p["id"] == item["product_id"]),
            None
        )

        if produit:

            panier_complet.append({
                "produit": produit,
                "qty": item["qty"]
            })

    return render_template_with_common(
        "cart.html",
        title_page="Panier",
        panier=panier_complet
    )

@app.route('/account/')
def account_page():
    if not is_logged_in():
        return redirect(url_for("connection_page"))

    user = user_database.get_user_by_email(session["email"])

    return render_template_with_common(
        "account.html",
        title_page="Mon compte",
        user=user
    )

@app.route('/account/update/', methods=['POST'])
def account_update():
    if not is_logged_in():
        return redirect(url_for("connection_page"))

    email = session["email"]
    user = user_database.get_user_by_email(email)

    if not user:
        return redirect(url_for("account_page"))

    # champs
    user["username"] = request.form.get("username")
    user["firstname"] = request.form.get("firstname")
    user["name"] = request.form.get("name")
    user["email"] = request.form.get("email")
    user["password"] = request.form.get("password")

    user_database.save()

    # update session
    session["email"] = user["email"]
    session["password"] = user["password"]

    return redirect(url_for("account_page"))

@app.route("/cart/remove/<int:id>", methods=["POST"])
def remove_from_cart(id):
    panier = session.get("panier", [])

    session["panier"] = [
        item for item in panier
        if item["product_id"] != id
    ]

    return redirect(url_for("cart_page"))

# PARTIE MAEL


@app.route("/cart/remove-one/<int:id>", methods=["POST"])
def remove_qty(id):

    panier = session.get("panier", [])

    for item in panier:

        if item["product_id"] == id:

            item["qty"] -= 1

            if item["qty"] <= 0:
                panier.remove(item)

            break

    session["panier"] = panier

    return redirect(url_for("cart_page"))

@app.route("/cart/add/<int:id>", methods=["POST"])
def add_qty(id):
    panier = session.get("panier", [])

    for item in panier:
        if item["product_id"] == id:
            item["qty"] += 1
            break

    session["panier"] = panier

    return redirect(url_for("cart_page"))


# FIN PARTIE MAEL

@app.route("/checkout/pay", methods=["POST"])
def confirm_fake_payment():

    if not is_logged_in():
        return redirect(url_for("connection_page"))

    panier = session.get("panier", [])

    if not isinstance(panier, list) or len(panier) == 0:
        return redirect(url_for("cart_page"))

    user = user_database.get_user_by_email(session["email"])

    if "orders" not in user:
        user["orders"] = []

    products = product_database.get_products()
    products_by_id = {p["id"]: p for p in products}

    total = 0
    items = []

    for item in panier:

        product = products_by_id.get(item["product_id"])

        if not product:
            continue

        total += product["prix"] * item["qty"]

        items.append({
            "product_id": item["product_id"],
            "qty": item["qty"]
        })

    if user["orders"]:
        max_id = max(o["id"] for o in user["orders"])
    else:
        max_id = 0

    order = {
        "id": max_id + 1,
        "items": items,
        "total": round(total, 2),
        "date": "2026-05-18"
    }

    user["orders"].append(order)

    user_database.save()

    session["panier"] = []

    return render_template_with_common(
        "order_success.html",
        title_page="Commande validée",
        order=order
    )

@app.route("/orders")
def orders_page():

    if not is_logged_in():
        return redirect(url_for("connection_page"))

    user = user_database.get_user_by_email(session["email"])

    orders = user.get("orders", [])

    products = product_database.get_products()
    products_by_id = {p["id"]: p for p in products}

    # enrichissement
    enriched_orders = []

    for order in orders:

        enriched_items = []

        for item in order["items"]:

            product = products_by_id.get(item["product_id"])

            if product:

                enriched_items.append({
                    "product": product,
                    "qty": item["qty"]
                })

        enriched_orders.append({
            "id": order["id"],
            "date": order["date"],
            "total": order["total"],
            "items": enriched_items
        })

    return render_template_with_common(
        "orders.html",
        title_page="Mes commandes",
        orders=enriched_orders
    )

@app.route("/orders/delete/<int:order_id>", methods=["POST"])
def delete_order(order_id):

    if not is_logged_in():
        return redirect(url_for("connection_page"))

    user = user_database.get_user_by_email(session["email"])

    orders = user.get("orders", [])

    user["orders"] = [
        o for o in orders
        if o["id"] != order_id
    ]

    user_database.save()

    return redirect(url_for("orders_page"))

@app.route("/checkout")
def checkout():

    if not is_logged_in():
        return redirect(url_for("connection_page"))

    panier = session.get("panier", [])

    if not panier:
        return redirect(url_for("cart_page"))

    return render_template_with_common(
        "checkout.html",
        title_page="Paiement",
        panier=panier
    )

@app.route("/register/", methods=["GET", "POST"])
def register_page():

    if request.method == "GET":
        return render_template_with_common("register.html", title_page="Inscription")

    email = request.form.get("mail")
    password = request.form.get("password")
    username = request.form.get("username")

    if not email or not password:
        return render_template_with_common(
            "register.html",
            title_page="Inscription",
            error="Champs obligatoires manquants"
        )

    user = user_database.get_user_by_email(email)

    if user:
        return render_template_with_common(
            "register.html",
            title_page="Inscription",
            error="Compte déjà existant"
        )

    new_user = {
        "id": user_database.get_next_id() if hasattr(user_database, "get_next_id") else 1,
        "username": username or email.split("@")[0],
        "name": "",
        "firstname": "",
        "email": email,
        "password": password,
        "is_admin": False,
        "orders": []
    }

    user_database.add_user(new_user)
    user_database.save()

    create_session(email, password)

    return redirect(url_for("home"))



# Route pour gérer les erreurs
from werkzeug.exceptions import HTTPException

@app.errorhandler(Exception)
def handle_exception(e):
    if isinstance(e, HTTPException):
        code = e.code
        message = e.description
    else:
        code = 500
        message = "Une erreur interne est survenue."

    # log technique complet
    if code >= 500:
        log(repr(e), "erreur")
        log(session, "info")
    else:
        log(str(e), "warning")

    return render_template_with_common(
        "errors.html",
        title_page=f"Erreur {code}",
        error_code=code,
        error_message=message
    ), code


# Lancement du server
ip = conf.get_value("ip")
port = conf.get_value("port")
if __name__ == "__main__":
    app.run(ip, port, debug=conf.get_value("debug", False))