from flask import Blueprint, render_template, request, redirect, url_for, session, flash, current_app
from werkzeug.utils import secure_filename
from ..models import db, Bien, Favori, User
import os
import uuid

bien_bp = Blueprint('bien', __name__)

@bien_bp.route('/publier', methods=['GET', 'POST'])
def publier():
    if 'user_id' not in session or session.get('type_compte') != 'agent':
        flash("Seuls les agents peuvent publier.", "warning")
        return redirect(url_for('auth.login'))

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
            image_file.save(os.path.join(current_app.config['UPLOAD_FOLDER'], image_filename))

        if video_file:
            video_filename = secure_filename(str(uuid.uuid4()) + "_" + video_file.filename)
            video_file.save(os.path.join(current_app.config['UPLOAD_FOLDER'], video_filename))

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
        flash("Bien publié avec succès.", "success")
        return redirect(url_for('main.dashboard'))

    return render_template('bien/publier.html')

@bien_bp.route('/')
def index():
    biens = Bien.query.order_by(Bien.est_promu.desc(), Bien.date_publication.desc()).all()
    return render_template('bien/index.html', biens=biens)

@bien_bp.route('/favoris/ajouter/<int:bien_id>')
def ajouter_favori(bien_id):
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))

    favori = Favori(utilisateur_id=session['user_id'], bien_id=bien_id)
    db.session.add(favori)
    db.session.commit()
    flash("Ajouté aux favoris.", "success")
    return redirect(url_for('bien.index'))

@bien_bp.route('/favoris/supprimer/<int:favori_id>')
def supprimer_favori(favori_id):
    favori = Favori.query.get_or_404(favori_id)
    db.session.delete(favori)
    db.session.commit()
    flash("Retiré des favoris.", "info")
    return redirect(url_for('main.dashboard'))
