from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

# Importez l'instance de db depuis __init__.py
from .. import db

class Comment(db.Model):
    __tablename__ = 'comments'
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    forum_id = db.Column(db.Integer, db.ForeignKey('forums.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    forum = db.relationship('Forum', backref=db.backref('comments', lazy=True))
    user = db.relationship('User', backref=db.backref('comments', lazy=True))