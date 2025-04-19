from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, FloatField, TextAreaField, SelectField, FileField, HiddenField
from wtforms.validators import DataRequired, Length, EqualTo, NumberRange
from flask_wtf.file import FileAllowed

class RegisterForm(FlaskForm):
    nom = StringField("Nom", validators=[DataRequired(), Length(min=2, max=50)])
    telephone = StringField("Téléphone", validators=[DataRequired(), Length(min=8, max=15)])
    mot_de_passe = PasswordField("Mot de passe", validators=[DataRequired(), Length(min=6)])
    confirmer = PasswordField("Confirmer le mot de passe", validators=[DataRequired(), EqualTo('mot_de_passe')])
    submit = SubmitField("S’inscrire")


class LoginForm(FlaskForm):
    telephone = StringField("Téléphone", validators=[DataRequired()])
    mot_de_passe = PasswordField("Mot de passe", validators=[DataRequired()])
    submit = SubmitField("Se connecter")


class BienForm(FlaskForm):
    titre = StringField("Titre", validators=[DataRequired(), Length(max=100)])
    type_bien = SelectField("Type de bien", choices=[('maison', 'Maison'), ('terrain', 'Terrain'), ('appartement', 'Appartement')], validators=[DataRequired()])
    description = TextAreaField("Description", validators=[DataRequired(), Length(min=10)])
    prix = FloatField("Prix", validators=[DataRequired(), NumberRange(min=0)])
    localisation = StringField("Localisation", validators=[DataRequired(), Length(max=100)])
    image = FileField("Photo", validators=[FileAllowed(['jpg', 'jpeg', 'png'], 'Images uniquement !')])
    video = FileField("Vidéo", validators=[FileAllowed(['mp4'], 'MP4 uniquement !')])
    submit = SubmitField("Publier")


class MessageForm(FlaskForm):
    destinataire_id = HiddenField("ID destinataire", validators=[DataRequired()])
    contenu = TextAreaField("Message", validators=[DataRequired(), Length(min=2)])
    fichier = FileField("Joindre un fichier", validators=[FileAllowed(['jpg', 'jpeg', 'png', 'mp4'], 'Fichiers autorisés : jpg, png, mp4')])
    submit = SubmitField("Envoyer")


class ProfilForm(FlaskForm):
    photo = FileField("Changer ma photo", validators=[FileAllowed(['jpg', 'jpeg', 'png'], 'Formats acceptés : jpg, png')])
    submit = SubmitField("Mettre à jour")


class RechercheForm(FlaskForm):
    titre = StringField("Titre")
    localisation = StringField("Localisation")
    agent = StringField("Nom de l’agent")
    prix_min = FloatField("Prix min")
    prix_max = FloatField("Prix max")
    type_bien = SelectField("Type de bien", choices=[
        ('', 'Tous'),
        ('maison', 'Maison'),
        ('terrain', 'Terrain'),
        ('appartement', 'Appartement')
    ])
    submit = SubmitField("Rechercher")
