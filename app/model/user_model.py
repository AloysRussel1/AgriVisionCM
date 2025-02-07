from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

# Importez l'instance de db depuis __init__.py
from .. import db

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128))

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    @property
    def is_active(self):
        return True  # Si tous les utilisateurs sont actifs par défaut

    @property
    def is_authenticated(self):
        return True  # Toujours True pour un utilisateur connecté

    @property
    def is_anonymous(self):
        return False  # Un utilisateur connecté n'est pas anonyme

    def get_id(self):
        return str(self.id)  # Retourne l'ID de l'utilisateur comme chaîne de caractères