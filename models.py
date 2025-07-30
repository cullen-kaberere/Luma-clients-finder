from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class Client(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    business_name = db.Column(db.String(255))
    location = db.Column(db.String(255))
    email = db.Column(db.String(255))
    source_url = db.Column(db.String(512))
    found_at = db.Column(db.DateTime, default=datetime.utcnow)
