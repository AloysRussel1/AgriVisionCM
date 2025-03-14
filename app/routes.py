from flask import Blueprint, render_template, request, redirect, url_for, flash, send_from_directory
from flask_login import login_required, current_user
from app.model.user_model import User
from app.model.knowledge_share_model import KnowledgeShare
from app.model.resource_model import Resource
from app.model.comment_model import Comment
from app.model.reaction_model import Reaction
from app.model.forum_model import Forum
from app.model.product_model import Product
from app.model.message_model import Message
from app.model.notification_model import Notification
from app import socketio
from flask_socketio import emit, join_room, leave_room
from . import db
from app.forms import AddKnowledgeForm
from app.forms import EditProfileForm
import os

import requests
from datetime import datetime

from flask import jsonify, request
import random
import requests


from datetime import date  
from flask import current_app
from werkzeug.utils import secure_filename

main = Blueprint('main', __name__)

# Pages Statiques
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

@main.route('/auth')
def authentification():
    return render_template('auth.html', title='Authentification')

@main.route('/community')
def community():
    return render_template('community.html', title='Communauté')

@main.route('/events')
def events():
    return render_template('events.html', title='Événements')

# Profil Utilisateur
@main.route('/profile')
@login_required
def profile():
    user_data = {
        'username': current_user.username,
        'email': current_user.email,
        'joined_date': current_user.joined_date.strftime('%Y-%m-%d') if hasattr(current_user, 'joined_date') else 'Non spécifié',
    }
    return render_template('profile.html', title='Profil', user=user_data)

@main.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm()
    
    if form.validate_on_submit():
        existing_user = User.query.filter(
            (User.username == form.username.data) & (User.id != current_user.id)
        ).first()
        existing_email = User.query.filter(
            (User.email == form.email.data) & (User.id != current_user.id)
        ).first()

        if existing_user:
            flash('Ce nom d’utilisateur est déjà pris.', 'error')
            return render_template('edit_profile.html', title='Modifier le Profil', form=form)
        if existing_email:
            flash('Cet email est déjà utilisé.', 'error')
            return render_template('edit_profile.html', title='Modifier le Profil', form=form)

        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Votre profil a été mis à jour avec succès !', 'success')
        return redirect(url_for('main.profile'))

    if request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email

    return render_template('edit_profile.html', title='Modifier le Profil', form=form)

# Marché
@main.route('/market', methods=['GET', 'POST'])
@login_required
def market():
    if request.method == 'POST':
        name = request.form['name']
        price = request.form['price']
        city = request.form['city']
        quantity = request.form['quantity']
        description = request.form['description']
        image = request.files['image']
        
        image_path = f"static/uploads/{image.filename}"
        image.save(image_path)

        new_product = Product(
            name=name, price=price, city=city,
            quantity=quantity, description=description,
            image=image_path, user_id=current_user.id
        )
        db.session.add(new_product)
        db.session.commit()
        
        flash('Produit ajouté avec succès', 'success')
        return redirect(url_for('main.market'))
    
    products = Product.query.all()
    return render_template('market.html', products=products)

@main.route('/add_product', defaults={'product_id': None}, methods=['GET', 'POST'])
@main.route('/add_product/<int:product_id>', methods=['GET', 'POST'])
@login_required
def add_product(product_id=None):
    print(f"URL appelée : {request.url}")
    product = None
    if product_id:
        product = Product.query.get_or_404(product_id)
        if product.user_id != current_user.id:
            flash('Vous ne pouvez pas modifier ce produit.', 'error')
            return redirect(url_for('main.market'))
        print(f"Produit récupéré : {product.__dict__}")

    if request.method == 'POST':
        name = request.form['name']
        price = request.form['price']
        unit = request.form['unit']
        city = request.form['city']
        quantity = request.form['quantity']
        description = request.form['description']
        image = request.files.get('image')

        if product:  # Mode édition
            product.name = name
            product.price = price
            product.unit = unit
            product.city = city
            product.quantity = quantity
            product.description = description
            if image and image.filename:
                filename = secure_filename(image.filename)
                image_path = filename
                image.save(os.path.join(current_app.config['UPLOAD_FOLDER'], image_path))
                product.image = image_path
            db.session.commit()
            flash('Produit mis à jour avec succès !', 'success')
        else:  # Mode ajout
            if not image or not image.filename:
                flash('Une image est requise pour ajouter un produit.', 'error')
                return redirect(url_for('main.add_product'))

            filename = secure_filename(image.filename)
            image_path = filename
            image.save(os.path.join(current_app.config['UPLOAD_FOLDER'], image_path))

            new_product = Product(
                name=name,
                price=price,
                unit=unit,
                city=city,
                quantity=quantity,
                description=description,
                image=image_path,
                user_id=current_user.id
            )
            db.session.add(new_product)
            db.session.commit()
            flash('Produit ajouté avec succès !', 'success')

        return redirect(url_for('main.market'))

    print(f"Rendu avec product : {product}")
    return render_template('add_product.html', product=product)


@main.route('/delete_product/<int:product_id>')
@login_required
def delete_product(product_id):
    product = Product.query.get_or_404(product_id)
    if product.user_id != current_user.id:
        flash('Vous ne pouvez pas supprimer ce produit.', 'error')
        return redirect(url_for('main.market'))

    db.session.delete(product)
    db.session.commit()
    flash('Produit supprimé avec succès !', 'success')
    return redirect(url_for('main.market'))

# Chat
@main.route("/conversation/<int:user_id>", methods=['GET', 'POST'])  # Plus de <int:product_id>
@login_required
def conversation(user_id):
    seller = User.query.get_or_404(user_id)

    if request.method == 'POST':
        data = request.get_json()
        content = data.get('content')
        product_id = data.get('product_id')  # Toujours envoyé par Socket.IO, mais optionnel

        if not content:
            return jsonify({'error': 'Le contenu du message est requis'}), 400

        # Utiliser un product_id par défaut si non fourni (par exemple, dernier produit ou 1)
        last_message = Message.query.filter(
            ((Message.sender_id == current_user.id) & (Message.receiver_id == user_id)) |
            ((Message.sender_id == user_id) & (Message.receiver_id == current_user.id))
        ).order_by(Message.timestamp.desc()).first()
        product_id = last_message.product_id if last_message and 'product_id' in data else data.get('product_id', 1)  # Fallback à 1

        message = Message(
            sender_id=current_user.id,
            receiver_id=user_id,
            product_id=product_id,
            content=content,
            timestamp=datetime.utcnow(),
            is_read=False
        )
        db.session.add(message)

        product = Product.query.get(product_id)
        notification = Notification(
            user_id=user_id,
            message=f"Nouveau message de {current_user.username} concernant {product.name if product else 'un produit'}",
            type="message",
            timestamp=datetime.utcnow(),
            is_read=False
        )
        db.session.add(notification)

        db.session.commit()

        return jsonify({
            'success': True,
            'message': content,
            'timestamp': message.timestamp.strftime('%H:%M')
        })

    # GET : Afficher tous les messages avec cet utilisateur, quel que soit le produit
    messages = Message.query.filter(
        ((Message.sender_id == current_user.id) & (Message.receiver_id == user_id)) |
        ((Message.sender_id == user_id) & (Message.receiver_id == current_user.id))
    ).all()

    messages.sort(key=lambda msg: msg.timestamp)
    
    # Product est optionnel, on prend le dernier ou un défaut
    last_message = messages[-1] if messages else None
    product = Product.query.get(last_message.product_id) if last_message else Product.query.first()
    
    return render_template("conversation.html", seller=seller, messages=messages, product=product)


@main.route('/chat_history')
@login_required
def chat_history():
    today = date.today()
    sent_messages = Message.query.filter_by(sender_id=current_user.id).all()
    received_messages = Message.query.filter_by(receiver_id=current_user.id).all()
    all_messages = sent_messages + received_messages

    conversations = {}
    for msg in all_messages:
        other_user_id = msg.receiver_id if msg.sender_id == current_user.id else msg.sender_id
        if other_user_id not in conversations:
            conversations[other_user_id] = {
                'other_user': User.query.get(other_user_id),
                'last_message': msg,
                'unread_count': 0
            }
        if msg.timestamp > conversations[other_user_id]['last_message'].timestamp:
            conversations[other_user_id]['last_message'] = msg
        if msg.receiver_id == current_user.id and not msg.is_read:
            conversations[other_user_id]['unread_count'] += 1

    conversation_list = list(conversations.values())
    conversation_list.sort(key=lambda x: x['last_message'].timestamp, reverse=True)

    return render_template('chat_history.html', conversations=conversation_list, today=today)


# Connaissance
@main.route('/knowledge')
@login_required
def knowledge_share():
    knowledge_items = KnowledgeShare.query.filter_by(user_id=current_user.id).order_by(KnowledgeShare.created_at.desc()).all()
    return render_template('knowledge_share.html', knowledge_items=knowledge_items)

@main.route('/knowledge/<int:id>')
@login_required
def view_knowledge(id):
    item = KnowledgeShare.query.get_or_404(id)
    if item.user_id != current_user.id:
        return redirect(url_for('main.knowledge_share'))
    return render_template('view_knowledge.html', item=item)

@main.route('/add_knowledge', methods=['GET', 'POST'])
def add_knowledge():
    form = AddKnowledgeForm()
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
            file_path = filename
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

# Forum
@main.route('/forums')
@login_required
def forums():
    forums = Forum.query.order_by(Forum.created_at.desc()).all()
    return render_template('forums.html', forums=forums, title="Forum")

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

@main.route('/forums/<int:forum_id>', methods=['GET', 'POST'])
@login_required
def forum_detail(forum_id):
    forum_thread = Forum.query.get_or_404(forum_id)
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

#prediction
@main.route('/predict_price', methods=['POST'])
@login_required
def predict_price():
    data = request.get_json()
    product = data['product']
    region = data['region']
    date = data['date']

    # Simulation de prédiction
    simulated_prediction = {
        'price': random.randint(1000, 11000),
        'confidence': round(random.uniform(0.7, 1.0), 2),
        'factors': ['Demande saisonnière', 'Conditions météo', 'Offre locale']
    }

    # Prompt pour Hugging Face
    prompt = f"""
        Vous êtes un expert en agriculture et en analyse de données. Voici une prédiction de prix pour un produit agricole :
        - Produit : {product}
        - Région : {region}
        - Date : {date}
        - Prix prédit : {simulated_prediction['price']} XAF
        - Niveau de confiance : {simulated_prediction['confidence'] * 100}%
        - Facteurs clés : {', '.join(simulated_prediction['factors'])}

        Fournissez une interprétation détaillée de cette prédiction, expliquez ce que cela signifie pour un agriculteur ou un vendeur, et donnez 3 recommandations spécifiques basées sur ces données.
    """

    try:
        token = current_app.config['HUGGINGFACE_API_TOKEN']
        response = requests.post(
            "https://api-inference.huggingface.co/models/mistralai/Mixtral-8x7B-Instruct-v0.1",
            headers={"Authorization": f"Bearer {token}", "Content-Type": "application/json"},
            json={"inputs": prompt, "parameters": {"max_new_tokens": 500, "temperature": 0.7, "top_p": 0.9, "do_sample": True}}
        )

        if response.status_code != 200:
            error_notif = Notification(
                user_id=current_user.id,
                message=f"Erreur lors de la prédiction pour {product}.",
                type="warning",
                timestamp=datetime.utcnow()
            )
            db.session.add(error_notif)
            db.session.commit()
            return jsonify({'error': f'Erreur lors de l’analyse Hugging Face : {response.text}'}), 500

        result = response.json()
        interpretation_text = result[0]['generated_text'].strip()
        if interpretation_text.startswith(prompt):
            interpretation_text = interpretation_text[len(prompt):].strip()
        sections = interpretation_text.split('\n\n')
        interpretation = sections[0].strip() if len(sections) >= 1 else "Aucune interprétation fournie."
        recommendations = sections[1:] if len(sections) > 1 else []

        # Ajouter une notification de prédiction
        prediction_notif = Notification(
            user_id=current_user.id,
            message=f"Prédiction terminée pour {product} dans {region} : {simulated_prediction['price']} XAF",
            type="prediction",
            timestamp=datetime.utcnow()
        )
        db.session.add(prediction_notif)
        db.session.commit()

        return jsonify({
            'price': simulated_prediction['price'],
            'confidence': simulated_prediction['confidence'] * 100,
            'factors': simulated_prediction['factors'],
            'interpretation': interpretation,
            'recommendations': recommendations
        })

    except Exception as e:
        error_notif = Notification(
            user_id=current_user.id,
            message=f"Erreur serveur lors de la prédiction pour {product}.",
            type="warning",
            timestamp=datetime.utcnow()
        )
        db.session.add(error_notif)
        db.session.commit()
        return jsonify({'error': f'Erreur serveur : {str(e)}'}), 500
    
# Notifications    
@main.route('/get_notifications', methods=['GET'])
@login_required
def get_notifications():
    notifications = Notification.query.filter_by(user_id=current_user.id).order_by(Notification.timestamp.desc()).all()
    return jsonify([{
        'id': notif.id,
        'message': notif.message,
        'type': notif.type,
        'timestamp': notif.timestamp.strftime('%H:%M:%S'),
        'is_read': notif.is_read
    } for notif in notifications])
    
@main.route('/mark_notification_read', methods=['POST'])
@login_required
def mark_notification_read():
    data = request.get_json()
    notification_id = data.get('notification_id')
    notification = Notification.query.filter_by(id=notification_id, user_id=current_user.id).first()
    if notification:
        notification.is_read = True
        db.session.commit()
        return jsonify({'success': True})
    return jsonify({'success': False}), 403
    
    
# Routes Dynamiques
@main.route('/category/')
def category(category):
    return render_template('category.html', category=category, title=f'Catégorie - {category.capitalize()}')

@main.route('/resource/')
def resource(resource_id):
    return render_template('resource.html', resource_id=resource_id, title=f'Ressource - {resource_id.replace("-", " ").capitalize()}')

# Utilitaires
def allowed_file(filename):
    allowed_extensions = {'png', 'jpg', 'jpeg', 'gif'}
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in allowed_extensions

@main.route('/uploads/<path:filename>')
def uploaded_file(filename):
    return send_from_directory(current_app.config['UPLOAD_FOLDER'], filename)

# Handlers SocketIO
@socketio.on("send_message")
def handle_send_message(data):
    print("📩 Message reçu côté serveur :", data)
    
    sender_id = data.get("sender_id")
    receiver_id = data.get("receiver_id")
    content = data.get("message")
    product_id = data.get("product_id", 1)

    if not sender_id or not receiver_id or not content:
        print("⚠️ Erreur: Données invalides reçues.")
        return

    print(f"💾 Enregistrement du message : {content} de {sender_id} vers {receiver_id} pour le produit {product_id}")

    message = Message(
        sender_id=sender_id,
        receiver_id=receiver_id,
        content=content,
        product_id=product_id,
        timestamp=datetime.utcnow(),
        is_read=False
    )
    db.session.add(message)

    sender = User.query.get(sender_id)
    #product = Product.query.get(product_id)

    notification = Notification(
        user_id=receiver_id,
        message=f"Nouveau message de {sender.username}",
        type="message",
        timestamp=datetime.utcnow(),
        is_read=False
    )
    db.session.add(notification)

    db.session.commit()
    print(f"✅ Notification créée pour user_id={receiver_id}: {notification.message}")

    room = f"chat_{min(sender_id, receiver_id)}_{max(sender_id, receiver_id)}"
    emit("receive_message", {
        "sender_id": sender_id,
        "receiver_id": receiver_id,
        "message": content,
        "product_id": product_id,
        "timestamp": message.timestamp.strftime('%d/%m/%Y %H:%M')  # Date complète
    }, room=room)


@socketio.on('join_room')
def handle_join_room(data):
    room = f"chat_{min(data['user1'], data['user2'])}_{max(data['user1'], data['user2'])}"
    join_room(room)
    print(f"🚪 Utilisateur a rejoint la room: {room}")


@socketio.on('leave_room')
def handle_leave_room(data):
    room = f"chat_{min(data['user1'], data['user2'])}_{max(data['user1'], data['user2'])}"
    leave_room(room)
    print(f"🏃 Utilisateur a quitté la room: {room}")

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
            db.session.delete(existing_reaction)
            db.session.commit()
            reaction_count = Reaction.query.filter_by(comment_id=comment_id, reaction_type=reaction_type).count()
            emit('reaction_removed', {
                'comment_id': comment_id,
                'reaction_type': reaction_type,
                'reaction_count': reaction_count
            }, broadcast=True)
        else:
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