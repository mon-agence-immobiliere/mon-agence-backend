# app/config.py

import os

class Config:
    # Clé secrète (garde-la en sécurité !)
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'ma_clé_ultra_secrète_pour_la_prod'

    # Base de données (SQLite → PostgreSQL en prod)
    SQLALCHEMY_DATABASE_URI = 'sqlite:///db.sqlite3'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Mail (pour recevoir les messages admin)
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = 'monagenceimmobilliere@gmail.com'
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD') or 'mot_de_passe_app_spécial'
    MAIL_DEFAULT_SENDER = 'monagenceimmobilliere@gmail.com'

    # Flask-Babel (langues)
    BABEL_DEFAULT_LOCALE = 'fr'
    BABEL_TRANSLATION_DIRECTORIES = 'app/translations'

    # Uploads (photos, vidéos)
    UPLOAD_FOLDER = 'app/static/uploads'
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16 Mo
    ALLOWED_EXTENSIONS = {'jpg', 'jpeg', 'png', 'mp4'}

    # API SMS (ex : Vonage ou Twilio)
    VONAGE_API_KEY = os.environ.get('VONAGE_API_KEY')
    VONAGE_API_SECRET = os.environ.get('VONAGE_API_SECRET')
    VONAGE_BRAND_NAME = 'Mon Agence Immo'

    # Stripe ou Flutterwave (paiement)
    STRIPE_PUBLIC_KEY = os.environ.get('STRIPE_PUBLIC_KEY')
    STRIPE_SECRET_KEY = os.environ.get('STRIPE_SECRET_KEY')

    # Mobile Money (ex : CinetPay / PayDunya)
    CINETPAY_API_KEY = os.environ.get('CINETPAY_API_KEY')
    CINETPAY_SECRET = os.environ.get('CINETPAY_SECRET')
