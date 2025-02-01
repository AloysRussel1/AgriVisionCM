from flask import Blueprint, render_template

main = Blueprint('main', __name__)

@main.route('/')
def index():
    return render_template('index.html', title='Accueil')

@main.route('/predict')
def predict():
    return render_template('predict.html', title='Prédire')

@main.route('/history')
def history():
    return render_template('history.html', title='Historique des Prix')

@main.route('/resources')
def resources():
    return render_template('resources.html', title='Ressources')

@main.route('/about')
def about():
    return render_template('about.html', title='À Propos')

@main.route('/profile')
def profile():
    return render_template('profile.html', title='Profil')

@main.route('/community')
def community():
    return render_template('community.html', title='Communauté')

@main.route('/forums')
def forums():
    return render_template('forums.html', title='Forums')

@main.route('/events')
def events():
    return render_template('events.html', title='Événements')

@main.route('/knowledge')
def knowledge():
    return render_template('knowledge.html', title='Partage de Connaissances')