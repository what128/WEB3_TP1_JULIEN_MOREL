"""
Exercice de page de détails
"""

from flask import Flask, render_template, request, redirect
import bd


app = Flask(__name__)

@app.route('/service', methods=["GET", "POST"])
def details_service():
    """Affiche les services"""
    details_service = []
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
                details_service = curseur.fetchall()

    return render_template(
        'accueil.jinja', page="Détails du service", details_service=details_service)
      


@app.route('/')
def index():
    """Affiche les services"""
    services = []

    # TODO : faire try except et mettre dans logger

    with bd.creer_connexion() as conn:
        with conn.get_curseur() as curseur:
            curseur.execute('SELECT * from services LIMIT 5')
            services = curseur.fetchall()

    return render_template(
        'accueil.jinja', page="Accueil", services=services)
      
app.run()