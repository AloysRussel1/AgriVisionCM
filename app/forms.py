from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SelectField
from flask_wtf.file import FileField, FileAllowed
from wtforms.validators import DataRequired

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
