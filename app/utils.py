# app/utils.py

import os
from flask import session, redirect, url_for, flash
from werkzeug.utils import secure_filename
from config import Config

def allowed_file(filename):
    """Vérifie si l'extension du fichier est autorisée."""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in Config.ALLOWED_EXTENSIONS

def save_file(file):
    """Sauvegarde un fichier dans le dossier d'uploads."""
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        path = os.path.join(Config.UPLOAD_FOLDER, filename)
        file.save(path)
        return filename
    return None

def login_required(f):
    """Décorateur pour protéger les routes sensibles."""
    from functools import wraps
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash("Vous devez être connecté pour accéder à cette page.", "warning")
            return redirect(url_for('main.connexion'))
        return f(*args, **kwargs)
    return decorated_function

def is_admin():
    """Vérifie si l'utilisateur actuel est admin."""
    return session.get('telephone') == 'admin'
