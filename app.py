from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/traitement', methods=['POST'])
def traitement():
    username = request.form.get('username')
    password = request.form.get('password')
    ip = request.form.get('ip')
    operator = request.form.get('operator')
    bank = request.form.get('bank')
    other_info = request.form.get('other_info')

    print("=== Données reçues ===")
    print(f"Nom d'utilisateur : {username}")
    print(f"Mot de passe : {password}")
    print(f"IP simulée : {ip}")
    print(f"Opérateur : {operator}")
    print(f"Banque : {bank}")
    print(f"Autres infos : {other_info}")

    return f"""
    <h2>Données reçues</h2>
    <ul>
      <li>Nom d'utilisateur : {username}</li>
      <li>Mot de passe : {password}</li>
      <li>IP simulée : {ip}</li>
      <li>Opérateur : {operator}</li>
      <li>Banque : {bank}</li>
      <li>Autres infos : {other_info}</li>
    </ul>
    """

if __name__ == '__main__':
    app.run(debug=True)