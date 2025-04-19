from flask import Blueprint, render_template, request, redirect, url_for, flash, session, current_app
from werkzeug.utils import secure_filename
from ..models import db, User, Message
import os
import uuid

messaging_bp = Blueprint('messaging', __name__)

@messaging_bp.route('/messages', methods=['GET', 'POST'])
def messages():
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))

    user = User.query.get(session['user_id'])
    users = User.query.filter(User.id != user.id).all()

    if request.method == 'POST':
        destinataire_id = request.form['destinataire_id']
        contenu = request.form['contenu']
        fichier = request.files.get('fichier')
        fichier_nom = None

        if fichier:
            fichier_nom = secure_filename(str(uuid.uuid4()) + '_' + fichier.filename)
            fichier.save(os.path.join(current_app.config['UPLOAD_FOLDER'], fichier_nom))

        msg = Message(
            expediteur_id=user.id,
            destinataire_id=destinataire_id,
            contenu=contenu,
            fichier=fichier_nom
        )
        db.session.add(msg)
        db.session.commit()
        flash("Message envoyé.", "success")
        return redirect(url_for('messaging.messages'))

    messages_envoyes = Message.query.filter_by(expediteur_id=user.id).all()
    messages_recus = Message.query.filter_by(destinataire_id=user.id).all()

    return render_template('messaging/messages.html', users=users, messages_envoyes=messages_envoyes, messages_recus=messages_recus)
