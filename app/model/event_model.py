from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

# Importez l'instance de db depuis __init__.py
from .. import db

class Event(db.Model):
    __tablename__ = 'events'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    start_time = db.Column(db.DateTime, nullable=False)
    end_time = db.Column(db.DateTime, nullable=False)
    location = db.Column(db.String(200))  # Peut être une adresse physique ou un lien pour un événement en ligne
    type = db.Column(db.String(50))  # 'webinaire', 'réunion locale', etc.
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    user = db.relationship('User', backref=db.backref('events', lazy=True))