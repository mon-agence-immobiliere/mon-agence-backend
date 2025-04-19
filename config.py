import os

class Config:
    # Sécurité
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'ma_clé_ultra_secrète_pour_la_prod'

    # Base de données
    SQLALCHEMY_DATABASE_URI = 'sqlite:///db.sqlite3'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # VONAGE (OTP)
    VONAGE_API_KEY = os.environ.get('VONAGE_API_KEY') or 'votre_api_key'
    VONAGE_API_SECRET = os.environ.get('VONAGE_API_SECRET') or 'votre_api_secret'
    VONAGE_BRAND_NAME = 'Mon Agence Immo'

    # E-mail admin
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = 'monagenceimmobilliere@gmail.com'
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD') or 'mot_de_passe_application'
    MAIL_DEFAULT_SENDER = 'monagenceimmobilliere@gmail.com'

    # Flask-Babel (langues)
    BABEL_DEFAULT_LOCALE = 'fr'
    BABEL_TRANSLATION_DIRECTORIES = 'app/translations'

    # Uploads (photo/vidéo)
    UPLOAD_FOLDER = 'app/static/uploads'
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16 Mo
    ALLOWED_EXTENSIONS = {'jpg', 'jpeg', 'png', 'mp4'}
