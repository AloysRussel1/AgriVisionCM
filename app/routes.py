from flask import Blueprint, render_template, request, redirect, url_for,flash,send_from_directory
from flask_login import login_required, current_user
from app.model.user_model import User
from app.model.knowledge_share_model import KnowledgeShare
from app.model.resource_model import Resource
from app.model.comment_model import Comment
from app.model.reaction_model import Reaction
from app.model.forum_model import Forum
from app import socketio
from flask_socketio import emit
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


@main.route('/events')
def events():
    return render_template('events.html', title='Événements')

@main.route('/knowledge')
@login_required
def knowledge_share():
    # Filtrer pour afficher uniquement les publications de l'utilisateur courant
    knowledge_items = KnowledgeShare.query.filter_by(user_id=current_user.id).order_by(KnowledgeShare.created_at.desc()).all()

    return render_template('knowledge_share.html', knowledge_items=knowledge_items)

@main.route('/knowledge/<int:id>')
@login_required
def view_knowledge(id):
    item = KnowledgeShare.query.get_or_404(id)
    
    # Vérifier que l'utilisateur courant est le propriétaire de l'élément
    if item.user_id != current_user.id:
        return redirect(url_for('main.knowledge_share'))  # Redirection si ce n'est pas sa publication

    return render_template('view_knowledge.html', item=item)



def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in current_app.config['ALLOWED_EXTENSIONS']

@main.route('/add_knowledge', methods=['GET', 'POST'])
def add_knowledge():
    
    form = AddKnowledgeForm()  # Création du formulaire
    if request.method == 'POST':
        title = request.form.get('title')
        content = request.form.get('content')
        knowledge_type = request.form.get('type')
        file = request.files.get('file_upload')

        if not title or not knowledge_type:
            flash('Le titre et le type sont obligatoires.', 'error')
            return redirect(url_for('main.add_knowledge'))

        file_path = None
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file_path = filename  # On ne stocke que le nom du fichier
            file.save(file_path)
        elif file:
            flash('Type de fichier non autorisé.', 'error')
            return redirect(url_for('main.add_knowledge'))

        knowledge = KnowledgeShare(
            title=title,
            content=content,
            type=knowledge_type,
            file_path=file_path,
            user_id=current_user.id
        )
        db.session.add(knowledge)
        db.session.commit()
        flash('Connaissance ajoutée avec succès !', 'success')
        return redirect(url_for('main.knowledge_share'))

    return render_template('add_knowledge.html', form=form)

@main.route('/uploads/<path:filename>')
def uploaded_file(filename):
    return send_from_directory(current_app.config['UPLOAD_FOLDER'], filename)

# ROUTES POUR LE FORUM

# 1. Affichage de la liste des sujets du forum
@main.route('/forums')
@login_required
def forums():
    forums = Forum.query.order_by(Forum.created_at.desc()).all()
    # On passe la variable "forums" (liste d'objets Forum) au template
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
            flash('Sujet créé avec succès', 'success')
            return redirect(url_for('main.forums'))
        else:
            flash('Le titre et le contenu sont requis.', 'error')
    return render_template('new_forum.html', title="Nouveau Sujet")

# 3. Affichage d'un sujet et gestion de l'ajout d'un commentaire
@main.route('/forums/<int:forum_id>', methods=['GET', 'POST'])
@login_required
def forum_detail(forum_id):
    forum_thread = Forum.query.get_or_404(forum_id)
    
    # Charger les commentaires depuis la base de données
    forum_thread.comments_list = Comment.query.filter_by(forum_id=forum_id).all()
    
    if request.method == 'POST':
        comment_content = request.form.get('comment')
        if comment_content:
            new_comment = Comment(content=comment_content, forum_id=forum_id, user_id=current_user.id)
            db.session.add(new_comment)
            db.session.commit()
            flash('Commentaire ajouté', 'success')
            return redirect(url_for('main.forum_detail', forum_id=forum_id))
        else:
            flash('Le commentaire ne peut pas être vide.', 'error')

    return render_template('forum_detail.html', forum=forum_thread, title=forum_thread.title)

# 4. SocketIO event handler pour l'ajout instantané d'un commentaire
@socketio.on('new_comment')
def handle_new_comment(data):
    forum_id = data.get('forum_id')
    comment_content = data.get('comment')
    if not forum_id or not comment_content:
        return
    forum = Forum.query.get(forum_id)
    if forum:
        new_comment = Comment(content=comment_content, forum_id=forum_id, user_id=current_user.id)
        db.session.add(new_comment)
        db.session.commit()
        emit('comment_added', {
            'forum_id': forum_id,
            'comment': {
                'content': new_comment.content,
                'username': current_user.username,
                'created_at': new_comment.created_at.strftime('%d/%m/%Y %H:%M')
            }
        }, broadcast=True)
 
                
@socketio.on('new_reaction')
def handle_new_reaction(data):
    forum_id = data.get('forum_id')
    comment_id = data.get('comment_id')
    reaction_type = data.get('reaction')

    if not forum_id or not comment_id or not reaction_type:
        return

    comment = Comment.query.get(comment_id)
    if comment:
        existing_reaction = Reaction.query.filter_by(
            comment_id=comment_id,
            user_id=current_user.id,
            reaction_type=reaction_type
        ).first()

        if existing_reaction:
            # Si la réaction existe déjà, on la supprime
            db.session.delete(existing_reaction)
            db.session.commit()
            reaction_count = Reaction.query.filter_by(comment_id=comment_id, reaction_type=reaction_type).count()
            emit('reaction_removed', {
                'comment_id': comment_id,
                'reaction_type': reaction_type,
                'reaction_count': reaction_count
            }, broadcast=True)
        else:
            # Sinon, on l'ajoute
            new_reaction = Reaction(
                reaction_type=reaction_type,
                comment_id=comment_id,
                user_id=current_user.id
            )
            db.session.add(new_reaction)
            db.session.commit()
            reaction_count = Reaction.query.filter_by(comment_id=comment_id, reaction_type=reaction_type).count()
            emit('reaction_added', {
                'comment_id': comment_id,
                'reaction_type': reaction_type,
                'reaction_count': reaction_count
            }, broadcast=True)

# @main.route('/knowledge/')
# @login_required
# def view_knowledge(id):
#     knowledge = KnowledgeShare.query.get_or_404(id)
#     return render_template('view_knowledge.html', knowledge=knowledge, title=f'Détail de la Connaissance')

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