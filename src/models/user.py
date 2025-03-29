from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from datetime import datetime

db = SQLAlchemy()

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    accounts = db.relationship('Account', backref='owner', lazy=True)
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
        
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def __repr__(self):
        return f'<User {self.email}>'


class Account(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    service_name = db.Column(db.String(100), nullable=False)
    username = db.Column(db.String(100), nullable=True)
    email = db.Column(db.String(120), nullable=False)
    last_password_reset = db.Column(db.DateTime, nullable=True)
    password_compromised = db.Column(db.Boolean, default=False)
    last_breach_check = db.Column(db.DateTime, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    category = db.Column(db.String(50), nullable=True)
    date_discovered = db.Column(db.DateTime, nullable=True)
    discovery_method = db.Column(db.String(50), nullable=True, default='scan')
    confidence_level = db.Column(db.String(20), nullable=True)
    
    def __repr__(self):
        return f'<Account {self.service_name} for {self.email}>'


class BreachRecord(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    account_id = db.Column(db.Integer, db.ForeignKey('account.id'), nullable=False)
    breach_name = db.Column(db.String(100), nullable=False)
    breach_date = db.Column(db.DateTime, nullable=False)
    data_classes = db.Column(db.String(256), nullable=True)  # Comma-separated list of breached data types
    detected_at = db.Column(db.DateTime, default=datetime.utcnow)
    is_resolved = db.Column(db.Boolean, default=False)
    
    account = db.relationship('Account', backref=db.backref('breach_records', lazy=True))
    
    def __repr__(self):
        return f'<Breach {self.breach_name} for account {self.account_id}>'