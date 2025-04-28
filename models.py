from datetime import datetime
from app import db, login_manager
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy import func

@login_manager.user_loader
def load_user(user_id):
    return Company.query.get(int(user_id))

class Company(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    industry = db.Column(db.String(100))
    size = db.Column(db.String(50))  # Small, Medium, Large
    date_joined = db.Column(db.DateTime, default=datetime.utcnow)
    activities = db.relationship('Activity', backref='company', lazy=True)
    emission_targets = db.relationship('EmissionTarget', backref='company', lazy=True)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def get_total_emissions(self):
        return db.session.query(func.sum(Activity.emission_value)).filter_by(company_id=self.id).scalar() or 0
    
    def get_emissions_by_category(self):
        return db.session.query(
            Activity.category, 
            func.sum(Activity.emission_value).label('total')
        ).filter_by(company_id=self.id).group_by(Activity.category).all()

class Activity(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    category = db.Column(db.String(50), nullable=False)  # Energy, Transport, Manufacturing, etc.
    description = db.Column(db.Text)
    date = db.Column(db.Date, nullable=False)
    emission_value = db.Column(db.Float, nullable=False)  # In CO2e (Carbon dioxide equivalent)
    emission_unit = db.Column(db.String(20), default='kg', nullable=False)  # kg, tonnes
    company_id = db.Column(db.Integer, db.ForeignKey('company.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class EmissionTarget(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    target_value = db.Column(db.Float, nullable=False)  # Target emission value in CO2e
    target_unit = db.Column(db.String(20), default='kg', nullable=False)  # kg, tonnes
    target_date = db.Column(db.Date, nullable=False)
    category = db.Column(db.String(50))  # If for a specific category, otherwise overall
    company_id = db.Column(db.Integer, db.ForeignKey('company.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
