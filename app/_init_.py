import os
from flask import Flask
from dotenv import load_dotenv
from .extensions import db, babel
from .models import *

def create_app():
    load_dotenv()
    app = Flask(__name__)
    app.config.from_object('config.Config')

    db.init_app(app)
    babel.init_app(app)

    from .auth.routes import auth_bp
    from .otp.routes import otp_bp
    from .bien.routes import bien_bp
    from .messaging.routes import messaging_bp
    from .main.routes import main_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(otp_bp)
    app.register_blueprint(bien_bp)
    app.register_blueprint(messaging_bp)
    app.register_blueprint(main_bp)

    return app
