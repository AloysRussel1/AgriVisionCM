from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SelectField
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, SubmitField, FileField
from wtforms.validators import DataRequired
from wtforms.validators import DataRequired, Email, Length


class AddKnowledgeForm(FlaskForm):
    title = StringField('Titre', validators=[DataRequired()])
    type = SelectField('Type', choices=[('article', 'Article'),
                                        ('video', 'Vidéo'),
                                        ('qna', 'Q&A')],
                       validators=[DataRequired()])
    content = TextAreaField('Contenu', validators=[DataRequired()])
    file_upload = FileField('Fichier/Vidéo', validators=[
        FileAllowed(['jpg', 'jpeg', 'png', 'gif', 'mp4', 'avi'], 'Seuls les fichiers images et vidéos sont autorisés')
    ])


class EditProfileForm(FlaskForm):
    username = StringField('Nom d’utilisateur', validators=[DataRequired(), Length(min=1, max=80)])
    email = StringField('Email', validators=[DataRequired(), Email(), Length(max=120)])
    submit = SubmitField('Mettre à jour')