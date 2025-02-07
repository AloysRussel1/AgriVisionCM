from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

# Importez l'instance de db depuis __init__.py
from .. import db

class Resource(db.Model):
    __tablename__ = 'resources'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    file_path = db.Column(db.String(200), nullable=False)
    type = db.Column(db.String(50))  # Peut être 'document', 'video', 'guide', etc.
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    user = db.relationship('User', backref=db.backref('resources', lazy=True))