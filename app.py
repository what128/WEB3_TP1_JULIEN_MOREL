"""
Exercice de page de détails
"""

from flask import Flask, render_template, request
import bd


app = Flask(__name__)


@app.route('/')
def index():
    """Affiche les jeux"""
    jeux = []

    # TODO : faire try except et mettre dans logger

    with bd.creer_connexion() as conn:
        with conn.get_curseur() as curseur:
            curseur.execute('SELECT * from services_particuliers')
            jeux = curseur.fetchall()

    return render_template(
        'base.jhtml')
        
app.run()