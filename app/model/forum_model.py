from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

# Importez l'instance de db depuis __init__.py
from .. import db

class Forum(db.Model):
    __tablename__ = 'forums'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    user = db.relationship('User', backref=db.backref('forums', lazy=True))