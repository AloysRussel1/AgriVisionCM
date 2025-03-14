from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from datetime import datetime
# Importez l'instance de db depuis __init__.py
from .. import db

class Notification(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    message = db.Column(db.String(255), nullable=False)
    type = db.Column(db.String(20), nullable=False, default='info')  # 'message', 'prediction', 'warning', etc.
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    is_read = db.Column(db.Boolean, default=False)