from app import create_app, db
from app.models import Agent  # Chemin absolu ici

app = create_app()

with app.app_context():
    db.drop_all()
    db.create_all()
    print("[INIT] Base de données initialisée avec succès.")
