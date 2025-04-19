from flask import Blueprint, render_template, redirect, url_for, request, session, flash
from ..models import db, User, Bien, Favori
from werkzeug.utils import secure_filename
import os
import uuid

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def home():
    return render_template('main/home.html')

@main_bp.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))

    user = User.query.get(session['user_id'])

    if user.is_agent():
        biens = Bien.query.filter_by(agent_id=user.id).all()
        return render_template('main/dashboard_agent.html', user=user, biens=biens)
    else:
        favoris = Favori.query.filter_by(utilisateur_id=user.id).all()
        return render_template('main/dashboard_user.html', user=user, favoris=favoris)

@main_bp.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        nom = request.form['nom']
        email = request.form['email']
        message = request.form['message']
        print(f"[CONTACT] {nom} ({email}) : {message}")
        flash("Votre message a bien été envoyé.", "success")
        return redirect(url_for('main.contact'))
    return render_template('main/contact.html')

@main_bp.route('/profil', methods=['GET', 'POST'])
def profil():
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))

    user = User.query.get(session['user_id'])

    if request.method == 'POST':
        fichier = request.files['photo']
        if fichier:
            nom_fichier = secure_filename(str(uuid.uuid4()) + '_' + fichier.filename)
            fichier.save(os.path.join('static/uploads', nom_fichier))
            user.photo = nom_fichier
            db.session.commit()
            flash("Photo mise à jour.", "success")

    return render_template('main/profil.html', user=user)
