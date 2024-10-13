from flask import Flask, render_template, request, redirect, url_for, flash
import sqlite3
import sqlite3

# Connexion à la base de données
conn = sqlite3.connect('database.db')
cursor = conn.cursor()

# Créer la table users
cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL,
        email TEXT NOT NULL UNIQUE,
        password TEXT NOT NULL
    )
''')

conn.commit()
conn.close()


app = Flask(__name__)
app.secret_key = "gyudeyuezyudeyuyuyudyueyudezyuYYUDZYyuyuuehyueyucsdcsdygcsdgh4775**5'88*8::;::;:;:"

# Fonction pour se connecter à la base de données
def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

# Page d'accueil avec formulaire de connexion et d'inscription
@app.route('/')
def index():
    return render_template('index.html')

# Route pour gérer l'inscription
@app.route('/register', methods=['POST'])
def register():
    username = request.form['username']
    email = request.form['email-inscription']
    password = request.form['password-inscription']
    confirm_password = request.form['confirm-password']

    if password != confirm_password:
        flash("Les mots de passe ne correspondent pas")
        return redirect(url_for('index'))

    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Vérifier si l'utilisateur existe déjà
    cursor.execute("SELECT * FROM users WHERE email = ?", (email,))
    existing_user = cursor.fetchone()
    
    if existing_user:
        flash("Un utilisateur avec cet email existe déjà")
        conn.close()
        return redirect(url_for('index'))

    # Insérer un nouvel utilisateur
    cursor.execute("INSERT INTO users (username, email, password) VALUES (?, ?, ?)",
                   (username, email, password))
    conn.commit()
    conn.close()
    
    flash("Inscription réussie ! Vous pouvez maintenant vous connecter.")
    return redirect(url_for('index'))

# Route pour gérer la connexion
@app.route('/login', methods=['POST'])
def login():
    email = request.form['email']
    password = request.form['password']

    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Vérifier les informations de connexion
    cursor.execute("SELECT * FROM users WHERE email = ? AND password = ?", (email, password))
    user = cursor.fetchone()
    conn.close()

    if user:
        flash("Connexion réussie !")
        # Ici tu peux rediriger vers une autre page après la connexion
        return redirect(url_for('start'))

    else:
        flash("Email ou mot de passe incorrect.")
        return redirect(url_for('index'))
@app.route('/start', methods=['GET', 'POST'])
def start():
    flash("Bienvenue sur la page de démarrage!")
    return render_template('start.html')
if __name__ == "__main__":
    app.run(debug=True)
