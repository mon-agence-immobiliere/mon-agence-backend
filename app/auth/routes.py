from flask import Flask, render_template, redirect, url_for, request, session, flash, send_from_directory
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from datetime import datetime, timedelta
import os
import uuid

from models import db, User, Bien, Message, Favori, Abonnement

app = Flask(__name__)
app.secret_key = 'ton_secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///mon_agence.db'
app.config['UPLOAD_FOLDER'] = 'static/uploads'

db.init_app(app)


# --- Authentification ---
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        nom = request.form['nom']
        telephone = request.form['telephone']
        mot_de_passe = generate_password_hash(request.form['mot_de_passe'])

        if User.query.filter_by(telephone=telephone).first():
            flash("Ce numéro est déjà enregistré.")
            return redirect(url_for('register'))

        user = User(nom=nom, telephone=telephone, mot_de_passe=mot_de_passe)
        db.session.add(user)
        db.session.commit()
        flash("Inscription réussie. Connecte-toi.")
        return redirect(url_for('login'))

    return render_template('register.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        telephone = request.form['telephone']
        mot_de_passe = request.form['mot_de_passe']
        user = User.query.filter_by(telephone=telephone).first()

        if user and check_password_hash(user.mot_de_passe, mot_de_passe):
            session['user_id'] = user.id
            session['type_compte'] = user.type_compte
            flash("Bienvenue, " + user.nom)
            return redirect(url_for('dashboard'))
        else:
            flash("Identifiants incorrects.")
            return redirect(url_for('login'))

    return render_template('login.html')


@app.route('/logout')
def logout():
    session.clear()
    flash("Déconnecté avec succès.")
    return redirect(url_for('login'))


# --- Tableau de bord personnalisé ---
@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    user = User.query.get(session['user_id'])

    if user.is_agent():
        biens = Bien.query.filter_by(agent_id=user.id).all()
        return render_template('dashboard_agent.html', user=user, biens=biens)
    else:
        favoris = Favori.query.filter_by(utilisateur_id=user.id).all()
        return render_template('dashboard_user.html', user=user, favoris=favoris)


# --- Publier un bien ---
@app.route('/publier', methods=['GET', 'POST'])
def publier():
    if 'user_id' not in session or session.get('type_compte') != 'agent':
        return redirect(url_for('login'))

    if request.method == 'POST':
        titre = request.form['titre']
        type_bien = request.form['type_bien']
        description = request.form['description']
        prix = float(request.form['prix'])
        localisation = request.form['localisation']

        image_file = request.files['image']
        video_file = request.files['video']

        image_filename = None
        video_filename = None

        if image_file:
            image_filename = secure_filename(str(uuid.uuid4()) + "_" + image_file.filename)
            image_file.save(os.path.join(app.config['UPLOAD_FOLDER'], image_filename))

        if video_file:
            video_filename = secure_filename(str(uuid.uuid4()) + "_" + video_file.filename)
            video_file.save(os.path.join(app.config['UPLOAD_FOLDER'], video_filename))

        bien = Bien(
            titre=titre,
            type_bien=type_bien,
            description=description,
            prix=prix,
            localisation=localisation,
            image=image_filename,
            video=video_filename,
            agent_id=session['user_id']
        )

        db.session.add(bien)
        db.session.commit()
        flash("Bien publié avec succès.")
        return redirect(url_for('dashboard'))

    return render_template('publier.html')


# --- Fil d’actualité (accessible à tous) ---
@app.route('/')
def index():
    biens = Bien.query.order_by(
        Bien.est_promu.desc(),
        Bien.date_publication.desc()
    ).all()
    return render_template('index.html', biens=biens)


# --- Ajouter aux favoris ---
@app.route('/favoris/ajouter/<int:bien_id>')
def ajouter_favori(bien_id):
    if 'user_id' not in session:
        return redirect(url_for('login'))

    favori = Favori(utilisateur_id=session['user_id'], bien_id=bien_id)
    db.session.add(favori)
    db.session.commit()
    flash("Ajouté aux favoris.")
    return redirect(url_for('index'))


@app.route('/favoris/supprimer/<int:favori_id>')
def supprimer_favori(favori_id):
    favori = Favori.query.get_or_404(favori_id)
    db.session.delete(favori)
    db.session.commit()
    flash("Retiré des favoris.")
    return redirect(url_for('dashboard'))


# --- Messagerie privée ---
@app.route('/messages', methods=['GET', 'POST'])
def messages():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    user = User.query.get(session['user_id'])
    users = User.query.filter(User.id != user.id).all()

    if request.method == 'POST':
        destinataire_id = request.form['destinataire_id']
        contenu = request.form['contenu']
        fichier = request.files['fichier']
        fichier_nom = None

        if fichier:
            fichier_nom = secure_filename(str(uuid.uuid4()) + "_" + fichier.filename)
            fichier.save(os.path.join(app.config['UPLOAD_FOLDER'], fichier_nom))

        msg = Message(
            expediteur_id=user.id,
            destinataire_id=destinataire_id,
            contenu=contenu,
            fichier=fichier_nom
        )
        db.session.add(msg)
        db.session.commit()
        flash("Message envoyé.")

    messages_envoyes = Message.query.filter_by(expediteur_id=user.id).all()
    messages_recus = Message.query.filter_by(destinataire_id=user.id).all()

    return render_template('messages.html', users=users, messages_envoyes=messages_envoyes, messages_recus=messages_recus)


# --- Profil ---
@app.route('/profil', methods=['GET', 'POST'])
def profil():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    user = User.query.get(session['user_id'])

    if request.method == 'POST':
        fichier = request.files['photo']
        if fichier:
            nom_fichier = secure_filename(str(uuid.uuid4()) + "_" + fichier.filename)
            fichier.save(os.path.join(app.config['UPLOAD_FOLDER'], nom_fichier))
            user.photo = nom_fichier
            db.session.commit()
            flash("Photo mise à jour.")

    return render_template('profil.html', user=user)



