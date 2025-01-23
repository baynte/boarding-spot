from extensions import db
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    user_type = db.Column(db.String(20), nullable=False)  # 'tenant' or 'landlord'
    contact_number = db.Column(db.String(20))  # New field for contact number
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    # Add rooms relationship
    rooms = db.relationship('Room', backref='landlord', lazy=True)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Room(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    landlord_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    price = db.Column(db.Float, nullable=False)
    size = db.Column(db.Float)  # in square meters
    location = db.Column(db.String(200))
    amenities = db.Column(db.Text)  # JSON string of amenities
    availability = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    image_urls = db.Column(db.Text)  # JSON string of image URLs

    # Criteria for TOPSIS
    safety_score = db.Column(db.Float)  # 1-10
    cleanliness_score = db.Column(db.Float)  # 1-10
    accessibility_score = db.Column(db.Float)  # 1-10
    noise_level = db.Column(db.Float)  # 1-10 (lower is better)

class TenantPreference(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    tenant_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    max_price = db.Column(db.Float, nullable=False)
    min_size = db.Column(db.Float, nullable=False)
    preferred_location = db.Column(db.String(200), nullable=False)
    required_amenities = db.Column(db.Text, nullable=False)  # JSON string of required amenities
    
    # Weights for TOPSIS criteria (0-1)
    safety_weight = db.Column(db.Float, nullable=False, default=0.25)
    cleanliness_weight = db.Column(db.Float, nullable=False, default=0.25)
    accessibility_weight = db.Column(db.Float, nullable=False, default=0.25)
    noise_level_weight = db.Column(db.Float, nullable=False, default=0.25)

    # Add constraints to ensure weights are between 0 and 1
    __table_args__ = (
        db.CheckConstraint('safety_weight >= 0 AND safety_weight <= 1', name='safety_weight_range'),
        db.CheckConstraint('cleanliness_weight >= 0 AND cleanliness_weight <= 1', name='cleanliness_weight_range'),
        db.CheckConstraint('accessibility_weight >= 0 AND accessibility_weight <= 1', name='accessibility_weight_range'),
        db.CheckConstraint('noise_level_weight >= 0 AND noise_level_weight <= 1', name='noise_weight_range'),
        db.CheckConstraint('safety_weight + cleanliness_weight + accessibility_weight + noise_level_weight = 1', name='weights_sum'),
        db.CheckConstraint('max_price > 0', name='positive_price'),
        db.CheckConstraint('min_size > 0', name='positive_size'),
    )