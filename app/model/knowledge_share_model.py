from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from .. import db

class KnowledgeShare(db.Model):
    __tablename__ = 'knowledge_shares'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text)
    type = db.Column(db.String(50))  # 'article', 'video', 'qna'
    file_path = db.Column(db.String(255))  # Stocke le chemin du fichier
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    user = db.relationship('User', backref=db.backref('knowledge_shares', lazy=True))