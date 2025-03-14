from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_socketio import SocketIO
import os
from dotenv import load_dotenv  # Importer pour charger le .env

# Charger les variables d'environnement depuis .env (si présent)
load_dotenv()

# Initialisation des extensions
db = SQLAlchemy()
login_manager = LoginManager()
migrate = Migrate()
socketio = SocketIO(cors_allowed_origins="*", async_mode="eventlet")

def create_app():
    app = Flask(__name__)
    
    # Configuration de base
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', '11111')  # Clé secrète par défaut ou depuis .env
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['UPLOAD_FOLDER'] = os.path.join(app.root_path, 'static', 'uploads')
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    
# Charger le token Hugging Face
    app.config['HUGGINGFACE_API_TOKEN'] = os.getenv('HUGGINGFACE_API_TOKEN')
    if not app.config['HUGGINGFACE_API_TOKEN']:
        raise ValueError("Le token HUGGINGFACE_API_TOKEN n'est pas défini dans le fichier .env")
    
    # Initialisation des extensions avec l'application
    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'auth.authentification'
    migrate.init_app(app, db)
    socketio.init_app(app)

    # Enregistrement des blueprints
    from .routes import main
    app.register_blueprint(main)

    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)
    
    # Importation des modèles
    from .model.user_model import User
    from .model.forum_model import Forum
    from .model.comment_model import Comment
    from .model.event_model import Event
    from .model.registration_model import Registration
    from .model.knowledge_share_model import KnowledgeShare
    from .model.reaction_model import Reaction
    from .model.product_model import Product
    from .model.message_model import Message  
    from .model.notification_model import Notification

    return app

@login_manager.user_loader
def load_user(user_id):
    from .model.user_model import User
    return User.query.get(int(user_id))