"""
Exercice de page de détails
"""

import re
from flask import Flask, render_template, request, redirect, abort, make_response
from flask.logging import create_logger
from babel import numbers, dates
import mysql
import bd



app = Flask(__name__)
logger = create_logger(app)
app.config["BABEL_DEFAULT_LOCALE"] = "fr_CA"

devise = {
        "fr_CA": "CAD",
        "en_US": "USD",
        "en_CA": "CAD"
    }

def get_locale():
    """Retrouver la langue"""
    return request.cookies.get("langue", default="fr_CA")

def retrouver_categories():
    """Retrouve les catégories de tous les services."""
    try:
        with bd.creer_connexion() as conn:
            with conn.get_curseur() as curseur:
                curseur.execute('select * from categories;')
                return curseur.fetchall()
    except Exception as e:
        logger.exception("Une erreur est survenue lors de la tentative pour retouver les" \
        "noms de catégories de services dans la base de données: %s", e)
        abort(500)


@app.route('/ajouter', methods=["GET", "POST"])
def ajouter_service_dans_bd():
    """Ajout du service dans la base de données"""
    classe_titre = ""
    classe_description = ""
    classe_localisation = ""
    classe_categorie = ""
    classe_photo = ""

    erreur = False

    if request.method == "POST":
        langue = get_locale()

        regex_titre_localisation = re.compile("^[a-zA-ZÀ-ÖØ-öø-ÿ\\s'-]{1,50}$")
        regex_description = re.compile("^.{5,2000}$")
        regex_html = re.compile("<(.*)>.*?|<(.*) />")
        titre = request.form.get("titre", default="").strip()
        if not regex_titre_localisation.match(titre) or regex_html.search(titre):
            erreur = True
            classe_titre="is-invalid"

        localisation = request.form.get("localisation", default="").strip()
        if not regex_titre_localisation.match(localisation) or regex_html.search(localisation):
            erreur = True
            classe_localisation = "is-invalid"

        description = request.form.get("description", default="").strip()
        if not regex_description.match(description) or regex_html.search(description):
            erreur = True
            classe_description =  "is-invalid"

        cout = request.form.get("cout", type=float, default=0)

        statut = request.form.get("statut", type=int, default=0)

        categorie = request.form.get("categorie", type=int)

        photo = request.form.get("photo", default="").strip()
        if regex_html.search(photo):
            erreur = True
            classe_photo = "is-invalid"

        if erreur:
            return render_template("ajout_service.jinja", classe_titre=classe_titre, langue=langue, titre=titre,
                classe_localisation=classe_localisation, localisation=localisation, classe_description=classe_description,
                description=description, cout=cout, classe_categorie=classe_categorie, categorie=categorie,
                statut=statut, classe_photo=classe_photo, photo=photo, categories=retrouver_categories())
        try:
            with bd.creer_connexion() as conn:
                with conn.get_curseur() as curseur:
                    curseur.execute(
                        "INSERT INTO `services`(`id_categorie`, `titre`, `description`," \
                        " `localisation`, `actif`, `cout`, `photo`)" \
                        " VALUES (%(id_categorie)s,%(titre)s,%(description)s," \
                        "%(localisation)s,%(actif)s" \
                        ",%(cout)s,%(photo)s);",
                        {
                            "id_categorie": categorie,
                            "titre": titre,
                            "description": description,
                            "localisation": localisation,
                            "actif": statut,
                            "cout": cout,
                            "photo": photo
                        }
                    )
                    id_service_courant = curseur.lastrowid
                    return redirect(f'/service?id={id_service_courant}', code=303)
        except Exception as e:
            logger.exception("Une erreur est survenue lors de l'ajout du service: %s", e)
            abort(500)


@app.route('/ajout', methods=["GET", "POST"])
def ajout_service():
    """Interface pour ajouter un service"""
    langue = get_locale()
    return render_template('ajout_service.jinja', page="Ajout d'un service", langue=langue, statut=1, categories=retrouver_categories())

@app.route('/cookies', methods=['GET', 'POST'])
def page_cookies():
    """Page pour changer les cookies"""
    langue = get_locale()
    return render_template('cookies.jinja', page="Langue", langue=langue)

@app.route('/modification-cookies', methods=['GET', 'POST'])
def modification_cookies():
    """Page pour la modification des cookies"""
    if request.method == "POST":
        langue = request.form.get("langue", default="fr_CA")
        response = make_response(redirect('/', code=303))
        response.set_cookie('langue', langue)
        return response

@app.route('/services')
def afficher_services():
    """Page web qui affiche tous les services"""
    services = []
    services_existants = False
    langue = get_locale()

    try:
        with bd.creer_connexion() as conn:
            with conn.get_curseur() as curseur:
                curseur.execute('SELECT * from services WHERE actif=1 ORDER BY date_creation desc;')
                services = curseur.fetchall()
                for service in services:
                    services_existants = True
                    curseur.execute(
                    "SELECT nom_categorie FROM categories WHERE id_categorie=%(id_categorie)s",
                    {
                        "id_categorie": service["id_categorie"]
                    })
                    service["nom_categorie"] = curseur.fetchone()["nom_categorie"]

                return render_template(
                    'services.jinja', page="Tous les services", langue=langue, services=services, services_existants=services_existants)
    except Exception as e:
        logger.exception("Une erreur est survenue lors de l'affichage des services: %s", e)
        abort(500)


@app.route('/modifier', methods=['GET', 'POST'])
def modifier_service():
    """Interface pour modifier un service"""
    if request.method == "GET":
        identifiant = request.args.get('id', type=int)
        if not identifiant:
            abort(400)
        langue = get_locale()
        try:
            with bd.creer_connexion() as conn:
                with conn.get_curseur() as curseur:
                    curseur.execute('select * from services where id_service = %(id)s;',
                                {
                                    'id': identifiant
                                })
                    service = curseur.fetchone()
            return render_template('modification_service.jinja', page="Modification d'un service", langue=langue, service=service)
        except Exception as e:
            logger.exception("Une erreur est survenue lors du chargement de la page pour modifier un service: %s", e)
            abort(500)


@app.route('/modification', methods=['GET', 'POST'])
def modification_service():
    """Modification d'un service"""
    classe_titre = ""
    classe_description = ""
    classe_localisation = ""
    classe_photo = ""

    erreur = False

    regex_titre_localisation = re.compile("^[a-zA-ZÀ-ÖØ-öø-ÿ\\s'-]{1,50}$")
    regex_description = re.compile("^.{5,2000}$")
    regex_html = re.compile("<(.*)>.*?|<(.*) />")

    if request.method == "POST":
        langue = get_locale()
        identifiant = request.form.get('id', type=int)
        titre = request.form.get('titre', default='')
        if not regex_titre_localisation.match(titre) or regex_html.search(titre):
            erreur = True
            classe_titre="is-invalid"

        localisation = request.form.get('localisation', default='').strip()
        if not regex_titre_localisation.match(localisation) or regex_html.search(localisation):
            erreur = True
            classe_localisation = "is-invalid"

        description = request.form.get('description', default='').strip()
        if not regex_description.match(description) or regex_html.search(description):
            erreur = True
            classe_description =  "is-invalid"

        cout = request.form.get('cout', type=float, default=0)
        statut = request.form.get('statut', type=int)

        photo = request.form.get('photo', default='').strip()
        if regex_html.search(photo):
            erreur = True
            classe_photo = "is-invalid"

        if erreur:
            return render_template("modification_service_erreur.jinja", page="Erreur de modification d'un service", langue=langue, id_service=identifiant, statut=statut, classe_titre=classe_titre, titre=titre,
                    classe_localisation=classe_localisation, localisation=localisation, classe_description=classe_description,
                    description=description, cout=cout, classe_photo=classe_photo, photo=photo)

        try:
            with bd.creer_connexion() as conn:
                with conn.get_curseur() as curseur:
                    curseur.execute('update services set '
                        'titre = %(titre)s, description = %(description)s, localisation = %(localisation)s,'
                        'actif = %(statut)s, cout = %(cout)s, photo = %(photo)s '
                        'where id_service = %(id)s;',
                        {
                            'id': identifiant,
                            'titre': titre,
                            'description': description,
                            'localisation': localisation,
                            'statut': statut,
                            'cout': cout,
                            'photo': photo
                        })
            return redirect(f'/service?id={identifiant}', code=303)
        except Exception as e:
            logger.exception("Une erreur est survenue lors de la modification du service: %s", e)
            abort(500)

@app.route('/service', methods=["GET", "POST"])
def details_service():
    """Affiche les services"""
    erreur_service = True
    details_du_service = []
    if request.method == "GET":
        id_service = request.args.get("id", type=int)
        if not id_service:
            abort(400)
        langue = get_locale()

        try:
            with bd.creer_connexion() as conn:
                with conn.get_curseur() as curseur:
                    curseur.execute('SELECT * from services where id_service=%(id_service)s',
                                    {
                                        'id_service': id_service
                                    }
                                    )
                    details_du_service = curseur.fetchone()
                    curseur.execute(
                    "SELECT nom_categorie FROM categories WHERE id_categorie=%(id_categorie)s",
                    {
                        "id_categorie": details_du_service["id_categorie"]
                    })
                    details_du_service["nom_categorie"] = curseur.fetchone()["nom_categorie"]
                    erreur_service = False
                    details_du_service["date_creation"] = dates.format_date(
                        details_du_service["date_creation"], format="long", locale=langue)
                    details_du_service["cout"] = numbers.format_currency(
                        details_du_service["cout"], currency=devise[langue], locale=langue)

            return render_template(
                'details-service.jinja', page="Détails du service", langue=langue, details_service=details_du_service,
                erreur_service=erreur_service)
        except Exception as e:
            logger.exception("Une erreur est survenue lors de l'affichage des détails du service: %s", e)
            abort(500)


@app.route('/')
def index():
    """Affiche les services"""
    services = []
    services_actifs = False
    langue = get_locale()

    try:
        with bd.creer_connexion() as conn:
            with conn.get_curseur() as curseur:
                curseur.execute('SELECT * from services WHERE actif=1 ORDER BY date_creation desc LIMIT 5;')
                services = curseur.fetchall()
                for service in services:
                    services_actifs = True
                    curseur.execute(
                    "SELECT nom_categorie FROM categories WHERE id_categorie=%(id_categorie)s",
                    {
                        "id_categorie": service["id_categorie"]
                    })
                    service["nom_categorie"] = curseur.fetchone()["nom_categorie"]

                return render_template(
                    'accueil.jinja', page="Accueil", langue=langue, services=services,
                    services_actifs=services_actifs)
    except Exception as e:
        logger.exception("Une erreur est survenue lors de l'affichage des services actifs: %s", e)
        abort(500)


@app.errorhandler(500)
def erreur_serveur_interne(e):
    """Pour les erreurs du côté serveur"""
    logger.exception(e)
    langue = get_locale()

    message = "Une erreur du côté serveur est survenue. Veuillez retourner à la page d'accueil."
    if e.original_exception and isinstance(e.original_exception, mysql.connector.errors.Error):
        message = "Une erreur est survenue en lien avec la base de données."

    return render_template("erreur.jinja", page="Erreur", langue=langue, message=message)

@app.errorhandler(404)
def page_non_trouvee(e):
    """Pour les routes invalides"""
    logger.exception(e)
    langue = get_locale()

    message = "Cette page n'existe pas"

    return render_template("erreur.jinja", page="Erreur", langue=langue, message=message)

@app.errorhandler(400)
def parametre_invalide(e):
    """Pour un paramètre manquant dans l'url"""
    logger.exception(e)
    langue = get_locale()

    message = "Un ou des paramètres invalides ont été spécifiées."

    return render_template("erreur.jinja", page="Erreur de paramètre",
                           langue=langue, message=message)

app.run()
