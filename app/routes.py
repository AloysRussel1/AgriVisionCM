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
from app import socketio
from flask_socketio import emit, join_room, leave_room
from . import db
from app.forms import AddKnowledgeForm
from app.forms import EditProfileForm
import os

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

@main.route('/add_product', methods=['GET', 'POST'])
@login_required
def add_product():
    if request.method == 'POST':
        name = request.form['name']
        price = request.form['price']
        unit = request.form['unit']
        city = request.form['city']
        quantity = request.form['quantity']
        description = request.form['description']
        image = request.files['image']

        if image:
            filename = secure_filename(image.filename)
            image_path = filename
            image.save(os.path.join(current_app.config['UPLOAD_FOLDER'], image_path))
        else:
            image_path = None

        new_product = Product(
            name=name, price=price, city=city,
            quantity=quantity, description=description,
            unit=unit,
            image=image_path,
            user_id=current_user.id
        )
        db.session.add(new_product)
        db.session.commit()

        flash('Produit ajouté avec succès', 'success')
        return redirect(url_for('main.market'))

    return render_template('add_product.html')

# Chat
@main.route("/conversation/<int:user_id>/<int:product_id>")
@login_required
def conversation(user_id, product_id):
    seller = User.query.get_or_404(user_id)
    product = Product.query.get_or_404(product_id)
    
    messages = Message.query.filter(
        (Message.sender_id == current_user.id) & (Message.receiver_id == user_id) & (Message.product_id == product_id)
    ).all() + Message.query.filter(
        (Message.sender_id == user_id) & (Message.receiver_id == current_user.id) & (Message.product_id == product_id)
    ).all()

    messages.sort(key=lambda msg: msg.timestamp)
    
    return render_template("conversation.html", seller=seller, messages=messages, product=product)


@main.route('/chat_history')
@login_required
def chat_history():
    today = date.today()  # Date actuelle pour le formatage de l’horodatage
    sent_messages = Message.query.filter_by(sender_id=current_user.id).all()
    received_messages = Message.query.filter_by(receiver_id=current_user.id).all()
    all_messages = sent_messages + received_messages

    conversations = {}
    for msg in all_messages:
        other_user_id = msg.receiver_id if msg.sender_id == current_user.id else msg.sender_id
        key = (other_user_id, msg.product_id)
        if key not in conversations:
            conversations[key] = {
                'other_user': User.query.get(other_user_id),
                'product': Product.query.get(msg.product_id),
                'last_message': msg,
                'unread_count': 0
            }
        if msg.timestamp > conversations[key]['last_message'].timestamp:
            conversations[key]['last_message'] = msg
        # Compter les messages non lus (reçus mais pas encore vus)
        if msg.receiver_id == current_user.id and not msg.is_read:  # Suppose un champ `is_read` dans Message
            conversations[key]['unread_count'] += 1

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
        # Log du token pour vérification
        token = current_app.config['HUGGINGFACE_API_TOKEN']
        print(f"Token envoyé : {token}")

        # Appel à l'API Hugging Face
        response = requests.post(
            "https://api-inference.huggingface.co/models/mistralai/Mixtral-8x7B-Instruct-v0.1",
            headers={
                "Authorization": f"Bearer {token}",
                "Content-Type": "application/json"
            },
            json={
                "inputs": prompt,
                "parameters": {
                    "max_new_tokens": 500,
                    "temperature": 0.7,
                    "top_p": 0.9,
                    "do_sample": True
                }
            }
        )

        if response.status_code != 200:
            print(f"Erreur Hugging Face - Code: {response.status_code}, Réponse: {response.text}")
            return jsonify({'error': f'Erreur lors de l’analyse Hugging Face : {response.text}'}), 500

        result = response.json()
        print(f"Réponse brute Hugging Face : {result}")

        # Extraire le texte généré
        interpretation_text = result[0]['generated_text'].strip()

        # Supprimer le prompt de la réponse
        if interpretation_text.startswith(prompt):
            interpretation_text = interpretation_text[len(prompt):].strip()
        else:
            # Si le prompt n'est pas au début, on suppose que tout est la réponse utile
            interpretation_text = interpretation_text.strip()

        # Séparer l'interprétation et les recommandations
        # On suppose que l'interprétation est le premier paragraphe, suivi des recommandations
        sections = interpretation_text.split('\n\n')
        if len(sections) >= 1:
            interpretation = sections[0].strip()
            recommendations = sections[1:] if len(sections) > 1 else []
        else:
            interpretation = "Aucune interprétation fournie."
            recommendations = []

        # Log pour vérification
        print(f"Interprétation extraite : {interpretation}")
        print(f"Recommandations extraites : {recommendations}")

        return jsonify({
            'price': simulated_prediction['price'],
            'confidence': simulated_prediction['confidence'] * 100,
            'factors': simulated_prediction['factors'],
            'interpretation': interpretation,
            'recommendations': recommendations
        })

    except Exception as e:
        print(f"Exception dans predict_price: {str(e)}")
        return jsonify({'error': f'Erreur serveur : {str(e)}'}), 500
    
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
    product_id = data.get("product_id")

    if not sender_id or not receiver_id or not content or not product_id:
        print("⚠️ Erreur: Données invalides reçues.")
        return

    print(f"💾 Enregistrement du message : {content} de {sender_id} vers {receiver_id} pour le produit {product_id}")

    message = Message(sender_id=sender_id, receiver_id=receiver_id, content=content, product_id=product_id)
    db.session.add(message)
    db.session.commit()

    room = f"chat_{min(sender_id, receiver_id)}_{max(sender_id, receiver_id)}"
    emit("receive_message", {
        "sender_id": sender_id,
        "receiver_id": receiver_id,
        "message": content,
        "product_id": product_id
    }, room=room)

@socketio.on("join_room")
def handle_join_room(data):
    room = f"chat_{min(data['user1'], data['user2'])}_{max(data['user1'], data['user2'])}"
    join_room(room)
    print(f"Utilisateur {data['user1']} a rejoint la salle {room}")

@socketio.on("leave_room")
def handle_leave_room(data):
    room = f"chat_{min(data['user1'], data['user2'])}_{max(data['user1'], data['user2'])}"
    leave_room(room)
    print(f"Utilisateur {data['user1']} a quitté la salle {room}")

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