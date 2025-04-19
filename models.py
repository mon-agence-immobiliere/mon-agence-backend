from extensions import db
from datetime import datetime

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(100), nullable=False)
    telephone = db.Column(db.String(20), unique=True, nullable=False)
    mot_de_passe = db.Column(db.String(200))
    type_compte = db.Column(db.String(10), default='client')  # client ou agent
    photo = db.Column(db.String(200))
    verified = db.Column(db.Boolean, default=False)
    fin_essai = db.Column(db.DateTime)

    def is_agent(self):
        return self.type_compte == 'agent'

class Bien(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    titre = db.Column(db.String(150), nullable=False)
    type_bien = db.Column(db.String(50), nullable=False)
    description = db.Column(db.Text, nullable=False)
    prix = db.Column(db.Float, nullable=False)
    localisation = db.Column(db.String(150))
    image = db.Column(db.String(150))
    video = db.Column(db.String(150))
    date_publication = db.Column(db.DateTime, default=datetime.utcnow)
    est_promu = db.Column(db.Boolean, default=False)
    agent_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    agent = db.relationship('User', backref='biens')

class Favori(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    utilisateur_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    bien_id = db.Column(db.Integer, db.ForeignKey('bien.id'))
    date_ajout = db.Column(db.DateTime, default=datetime.utcnow)

class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    expediteur_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    destinataire_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    contenu = db.Column(db.Text)
    fichier = db.Column(db.String(150))
    date_envoi = db.Column(db.DateTime, default=datetime.utcnow)

class Abonnement(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    date_debut = db.Column(db.DateTime, default=datetime.utcnow)
    date_fin = db.Column(db.DateTime)
    actif = db.Column(db.Boolean, default=True)
