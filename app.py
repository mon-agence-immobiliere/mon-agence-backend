from flask import Flask, render_template, request, redirect, url_for, flash, jsonify, session, g
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timedelta
from models import db, Utilisateur
import random
import vonage



def create_app():
    app = Flask(__name__)
    app.secret_key = 'cle_super_secrete'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)

    VONAGE_API_KEY = '6d785e7d'
    VONAGE_API_SECRET = 'I2cA0E0cSeiSaJHZ'
    VONAGE_BRAND_NAME = 'Mon Agence Immo'


    @app.route('/')
    def home():
        return render_template('home.html')

    @app.route('/inscription', methods=['GET', 'POST'])
    def inscription():
        if request.method == 'POST':
            nom = request.form['nom']
            telephone = request.form['telephone']
            indicatif = request.form['indicatif']
            numero_avec_indicatif = f"{indicatif}{telephone}"
            code_otp = str(random.randint(100000, 999999))

            flash(f"(Simulation OTP: {code_otp})", "info")

            client = vonage.Client(key=VONAGE_API_KEY, secret=VONAGE_API_SECRET)
            sms = vonage.Sms(client)
            sms.send_message({
                "from": VONAGE_BRAND_NAME,
                "to": numero_avec_indicatif,
                "text": f"Votre code de vérification est : {code_otp}",
            })

            flash("Code OTP envoyé. Saisissez-le ci-dessous.", "success")

            session['otp_code'] = code_otp
            session['nom'] = nom
            session['telephone'] = telephone
            session['indicatif'] = indicatif

            return redirect(url_for('verifier'))
        return render_template('inscription.html')

    @app.route('/verifier', methods=['GET', 'POST'])
    def verifier():
        if request.method == 'POST':
            code = request.form['code']
            if code == session.get('otp_code'):
                telephone = session.get('telephone')
                nom = session.get('nom')
                agent = Utilisateur.query.filter_by(telephone=telephone).first()
                if not agent:
                    new_agent = Utilisateur(
                        nom=nom,
                        telephone=telephone,
                        verified=True,
                        fin_essai=datetime.utcnow() + timedelta(days=7)
                    )
                    db.session.add(new_agent)
                    db.session.commit()
                return redirect(url_for('confirmation'))
            else:
                flash("Code incorrect.", "error")
        return render_template('verifier.html')

    @app.route('/confirmation')
    def confirmation():
        return render_template('confirmation.html')

    @app.route("/aide")
    def aide():
        return render_template("aide.html")

    @app.route("/confidentialite")
    def confidentialite():
        return render_template("confidentialite.html")

    @app.route("/contact", methods=["GET", "POST"])
    def contact():
        if request.method == "POST":
            nom = request.form["nom"]
            email = request.form["email"]
            message = request.form["message"]
            print(f"[CONTACT] {nom} ({email}) : {message}")
            flash("Votre message a bien été envoyé.", "success")
            return redirect(url_for("contact"))
        return render_template("contact.html")

    @app.route("/verifier_acces/<telephone>")
    def verifier_acces(telephone):
        agent = Utilisateur.query.filter_by(telephone=telephone).first()
        if not agent:
            return jsonify({"acces": False, "message": "Numéro inconnu."})
        if agent.abonnement_valide:
            return jsonify({"acces": True})
        if agent.fin_essai and agent.fin_essai > datetime.utcnow():
            return jsonify({"acces": True, "message": "Essai gratuit actif."})
        lien_paiement = "https://flutterwave.com/pay/exemple" if telephone.startswith("+228") else "https://buy.stripe.com/test_exemple"
        return jsonify({"acces": False, "paiement": lien_paiement})

    return app