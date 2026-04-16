from flask import Config, Flask, render_template, request, session, redirect, url_for
import json
import os

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
        "nb_objets_panier": len(session.get("panier", [])),
        "val_titlePage": title_page
    }
    context.update(common_context)
    return render_template("content/" + template_name, **context)

@app.route('/product/')
def product_page():

    return render_template_with_common("product.html", title_page="Produits")

@app.route('/')
def home():
    if not is_logged_in():
        return redirect(url_for("connection_page"))

    return render_template_with_common("home.html", title_page="Accueil")

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

@app.route('/register/')
def register_page():
    return render_template_with_common("register.html", title_page="Inscription")



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