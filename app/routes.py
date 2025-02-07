from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import login_required, current_user
from app.model.user_model import User
from app.model.knowledge_share_model import KnowledgeShare
from . import db
from app.forms import AddKnowledgeForm

import os
from flask import current_app
from werkzeug.utils import secure_filename


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
@login_required
def knowledge():
    knowledge_items = KnowledgeShare.query.order_by(KnowledgeShare.created_at.desc()).all()
    return render_template('knowledge_share.html', knowledge_items=knowledge_items, title='Partage de Connaissances')

@main.route('/knowledge/add', methods=['GET', 'POST'])
@login_required
def add_knowledge():
    form = AddKnowledgeForm()
    if form.validate_on_submit():
        title = form.title.data
        content = form.content.data
        type = form.type.data

        # Gestion du fichier uploadé
        file = form.file_upload.data
        filename = None
        if file:
            filename = secure_filename(file.filename)
            upload_path = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
            file.save(upload_path)
            # Ici, tu peux décider d'enregistrer le chemin du fichier dans la base de données,
            # par exemple en ajoutant un champ "file_url" dans ton modèle KnowledgeShare.
        
        # Créer l'enregistrement KnowledgeShare
        new_knowledge = KnowledgeShare(
            title=title,
            content=content,
            type=type,
            user_id=current_user.id
            # Si tu ajoutes un champ pour le fichier, ex: file_url=filename
        )
        db.session.add(new_knowledge)
        db.session.commit()
        return redirect(url_for('main.knowledge'))
    
    return render_template('add_knowledge.html', title='Ajouter une Connaissance', form=form)


@main.route('/knowledge/')
@login_required
def view_knowledge(id):
    knowledge = KnowledgeShare.query.get_or_404(id)
    return render_template('view_knowledge.html', knowledge=knowledge, title=f'Détail de la Connaissance')

@main.route('/edit_profile')
def edit_profile():
    return render_template('edit_profile.html', title='Editer votre profil')

@main.route('/auth')
def authentification():
    return render_template('auth.html', title='Authentification')

@main.route('/category/')
def category(category):
    # Logique pour afficher la page de la catégorie spécifiée
    return render_template('category.html', category=category, title=f'Catégorie - {category.capitalize()}')

@main.route('/resource/')
def resource(resource_id):
    # Logique pour afficher la ressource spécifiée
    return render_template('resource.html', resource_id=resource_id, title=f'Ressource - {resource_id.replace("-", " ").capitalize()}')