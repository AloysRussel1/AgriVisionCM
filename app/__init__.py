from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate
import os

db = SQLAlchemy()
login_manager = LoginManager()
migrate = Migrate()

def create_app():
    app = Flask(__name__)
    # Charger la configuration correctement
    app.config.from_object('app.config.Config')

    app.config['UPLOAD_FOLDER'] = os.path.join(app.root_path, 'static', 'uploads')
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    app.config['SECRET_KEY'] = '11111'  # Remplissez avec une clé secrète
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'  
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'auth.authentification'  

    from .routes import main
    app.register_blueprint(main)

    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)

    from .model.user_model import User  
    from .model.forum_model import Forum
    from .model.comment_model import Comment
    from .model.resource_model import Resource
    from .model.event_model import Event
    from .model.registration_model import Registration
    from .model.knowledge_share_model import KnowledgeShare


    migrate.init_app(app, db)  # Initialise Flask-Migrate

    return app

from .model.user_model import User  # Pour load_user

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))