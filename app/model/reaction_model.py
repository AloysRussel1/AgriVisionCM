from .. import db

class Reaction(db.Model):
    __tablename__ = 'reactions'  # Nom de la table

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)  
    user = db.relationship('User', backref=db.backref('reactions', lazy=True))
    
    reaction_type = db.Column(db.String(80), nullable=False)  # Correction ici

    comment_id = db.Column(db.Integer, db.ForeignKey('comments.id'), nullable=False)  
    comment = db.relationship('Comment', backref=db.backref('reactions', lazy=True))  # Ajout de la relation
