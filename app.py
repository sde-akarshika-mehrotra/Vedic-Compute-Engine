from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from core import VedicMathEngine
from models import db, User, Client
import time
import os

app = Flask(__name__)

# --- CONFIGURATION ---
app.config['SECRET_KEY'] = 'vedic-secret-key-123' # Change this for production
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'

# --- INIT EXTENSIONS ---
db.init_app(app)
engine = VedicMathEngine()
login_manager = LoginManager()
login_manager.login_view = 'login'
login_manager.init_app(app)

@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))

# --- DATABASE SETUP ---
with app.app_context():
    db.create_all()

# ---- ROUTES ----

@app.route('/')
def home():
    return render_template('index.html', user=current_user)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        if User.query.filter_by(username=username).first():
            flash('Username already exists.', 'error')
        else:
            new_user = User(username=username, password=generate_password_hash(password, method='scrypt'))
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user)
            return redirect(url_for('dashboard'))
            
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user = User.query.filter_by(username=username).first()
        
        if user and check_password_hash(user.password, password):
            login_user(user)
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid credentials.', 'error')
            
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/dashboard')
@login_required
def dashboard():
    # Show only clients belonging to the logged-in user
    clients = Client.query.filter_by(user_id=current_user.id).all()
    return render_template('dashboard.html', clients=clients, user=current_user)

@app.route('/save_client', methods=['POST'])
@login_required
def save_client():
    data = request.json
    new_client = Client(
        name=data['name'],
        phone=data['phone'],
        principal=data['principal'],
        rate=data['rate'],
        tenure=data['years'],
        emi=data['emi'],
        user_id=current_user.id
    )
    db.session.add(new_client)
    db.session.commit()
    return jsonify({"message": "Client saved successfully!"})

# --- VEDIC API (Same as before) ---
@app.route('/calculate/emi', methods=['POST'])
def calculate_emi():
    data = request.json
    try:
        p = float(data.get('principal'))
        r = float(data.get('rate'))
        t = float(data.get('years'))
        start = time.time_ns()
        
        emi = engine.calculate_emi(p, r, t)
        
        end = time.time_ns()
        return jsonify({
            "emi": emi,
            "latency_microseconds": (end - start) / 1000
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)