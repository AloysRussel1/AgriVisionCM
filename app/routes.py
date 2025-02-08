from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import login_required, current_user
from app.model.user_model import User
from app.model.knowledge_share_model import KnowledgeShare
from app.model.resource_model import Resource
from app.model.comment_model import Comment
from app.model.forum_model import Forum
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

# @main.route('/forums')
# def forums():
#     return render_template('forums.html', title='Forums')

# @main.route('/forum/comment', methods=['POST'])
# def add_comment():
#     forum = Forum.query.first()  # Assumes there's only one forum
#     content = request.form['content']
#     comment = Comment(content=content, forum_id=forum.id, user_id=current_user.id)
#     db.session.add(comment)
#     db.session.commit()
#     return redirect(url_for('main.forum'))

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


# 1. Affichage de la liste des sujets du forum
@main.route('/forums')
@login_required
def forums():
    forums = Forum.query.order_by(Forum.created_at.desc()).all()
    return render_template('forums.html', forums=forums, title="Forum")

# 2. Création d'un nouveau sujet (GET pour afficher le formulaire, POST pour le traiter)
@main.route('/forums/new', methods=['GET', 'POST'])
@login_required
def new_forum():
    if request.method == 'POST':
        title = request.form.get('title')
        content = request.form.get('content')
        if title and content:
            new_thread = Forum(title=title, content=content, user_id=current_user.id)
            db.session.add(new_thread)
            db.session.commit()
            return redirect(url_for('main.forums'))
        # Vous pouvez ajouter ici la gestion des erreurs
    return render_template('new_forum.html', title="Nouveau Sujet")

# 3. Affichage d'un sujet et gestion de l'ajout d'un commentaire
@main.route('/forums/<int:forum_id>', methods=['GET', 'POST'])
@login_required
def forum_detail(forum_id):
    forum_thread = Forum.query.get_or_404(forum_id)
    if request.method == 'POST':
        comment_content = request.form.get('comment')
        if comment_content:
            new_comment = Comment(content=comment_content, forum_id=forum_id, user_id=current_user.id)
            db.session.add(new_comment)
            db.session.commit()
            return redirect(url_for('main.forum_detail', forum_id=forum_id))
        # Vous pouvez ajouter ici la gestion d'erreurs si le commentaire est vide
    return render_template('forum_detail.html', forum=forum_thread, title=forum_thread.title)

@main.route('/shared_resources')
def shared_resources():
    resources_by_category = {
        'document': Resource.query.filter_by(type='document').all(),
        'guide': Resource.query.filter_by(type='guide').all(),
        'case_study': Resource.query.filter_by(type='case_study').all()
    }
    return render_template('shared_resources.html', resources_by_category=resources_by_category)


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