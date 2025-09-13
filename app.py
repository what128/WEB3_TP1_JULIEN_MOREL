"""
Exercice de page de détails
"""

from flask import Flask, render_template, request, redirect
from datetime import datetime
import bd


app = Flask(__name__)



@app.route('/ajouter', methods=["GET", "POST"])
def ajouter_service_dans_bd():
    """Ajout du service dans la base de données"""
    if request.method == "POST":
        titre = request.form.get("titre", default="")
        localisation = request.form.get("localisation", default="")
        description = request.form.get("description", default="")
        cout = request.form.get("cout", type=int)
        statut = request.form.get("statut", type=int)
        categorie = request.form.get("categorie", type=int)
        with bd.creer_connexion() as conn:
            with conn.get_curseur() as curseur:
                curseur.execute(
                    "INSERT INTO `services`(`id_categorie`, `titre`, `description`," \
                    " `localisation`, `actif`, `cout`)" \
                    " VALUES (%(id_categorie)s,%(titre)s,%(description)s," \
                    "%(localisation)s,%(actif)s" \
                    ",%(cout)s);",
                    {
                        "id_categorie": categorie,
                        "titre": titre,
                        "description": description,
                        "localisation": localisation,
                        "actif": statut,
                        "cout": cout
                    }
                )
                return redirect('/', 302)



@app.route('/ajout', methods=["GET", "POST"])
def ajout_service():
    """Interface pour ajouter un service"""
    categories = []
    with bd.creer_connexion() as conn:
        with conn.get_curseur() as curseur:
            curseur.execute('select * from categories;')
            categories = curseur.fetchall()
           
    return render_template('ajout_service.jinja', page="Ajout d'un service", categories=categories) 

@app.route('/service', methods=["GET", "POST"])
def details_service():
    """Affiche les services"""
    erreur_service = True
    details_du_service = []
    if request.method == "GET":
        id_service = request.args.get("id", type=int)

    # TODO : faire try except et mettre dans logger

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


        return render_template(
            'details-service.jinja', page="Détails du service", details_service=details_du_service,
            erreur_service=erreur_service)
      


@app.route('/')
def index():
    """Affiche les services"""
    services = []
    services_actifs = False

    # TODO : faire try except et mettre dans logger

    with bd.creer_connexion() as conn:
        with conn.get_curseur() as curseur:
            curseur.execute('SELECT * from services WHERE actif=1 ORDER BY date_creation desc LIMIT 5;')
            services = curseur.fetchall()
            for service in services:
                curseur.execute(
                "SELECT nom_categorie FROM categories WHERE id_categorie=%(id_categorie)s",
                {
                    "id_categorie": service["id_categorie"]
                })
                service["nom_categorie"] = curseur.fetchone()["nom_categorie"]


    return render_template(
        'accueil.jinja', page="Accueil", services=services)
     
app.run()