from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from datetime import datetime
import uuid

from flask_marshmallow import Marshmallow

from werkzeug.security import generate_password_hash, check_password_hash

import secrets

from flask_login import LoginManager, UserMixin

db = SQLAlchemy()
login_manager = LoginManager()
ma = Marshmallow()

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

class User(db.Model, UserMixin):
    id = db.Column(db.String, primary_key = True)
    email = db.Column(db.String(150), nullable = False, unique = True)
    password = db.Column(db.String, nullable = False)
    token = db.Column(db.String, unique = True)
    date_created = db.Column(db.DateTime, nullable = False, default = datetime.utcnow)
    drone = db.relationship('Car', backref = 'owner', lazy = True)

    def __init__(self, email, password, token = '', id = ''):
        self.id = self.set_id()
        self.email = email
        self.password = self.set_password(password)
        self.token = self.set_token(24)

    def set_id(self):
        return str(uuid.uuid4())

    def set_password(self, password):
        self.pw_hash = generate_password_hash(password)
        return self.pw_hash

    def set_token(self, length):
        return secrets.token_hex(24)

class Car(db.Model):
    id = db.Column(db.String, primary_key = True)
    year = db.Column(db.Numeric)
    make = db.Column(db.String(100))
    model = db.Column(db.String(100))
    color = db.Column(db.String(50))    
    condition = db.Column(db.String(10))    
    dimensions = db.Column(db.String(100))
    weight = db.Column(db.String(100))    
    price = db.Column(db.Numeric(precision=10, scale=2))
    user_token = db.Column(db.String, db.ForeignKey('user.token'), nullable = False)

    def __init__(self, year, make, model, color, condition, dimensions, weight, price, user_token, id = ''):
        self.id = self.set_id()
        self.year = year
        self.make = make
        self.model = model        
        self.color = color
        self.condition = condition
        self.dimensions = dimensions
        self.weight = weight        
        self.price = price
        self.user_token = user_token

    def set_id(self):
        return (secrets.token_urlsafe())

class CarSchema(ma.Schema):
    class Meta:
        fields = ['id', 'year', 'make','model', 'color', 'condition', 'dimensions', 'weight', 'price']   

car_schema = CarSchema()
cars_schema = CarSchema(many=True)