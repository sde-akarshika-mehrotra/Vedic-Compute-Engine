from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin

db = SQLAlchemy()

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)
    clients = db.relationship('Client', backref='agent', lazy=True)

class Client(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    principal = db.Column(db.Float, nullable=False)
    rate = db.Column(db.Float, nullable=False)
    tenure = db.Column(db.Float, nullable=False)
    emi = db.Column(db.Float, nullable=False)
    # Link to the User (Agent) who saved this
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)