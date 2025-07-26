# models.py

from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class Lead(db.Model):
    __tablename__ = 'leads'

    id = db.Column(db.Integer, primary_key=True)
    business_name = db.Column(db.String, nullable=False)
    location = db.Column(db.String, nullable=False)
    email = db.Column(db.String, nullable=True)
    website_url = db.Column(db.String, nullable=True)
    website_status = db.Column(db.String, nullable=False)  # Missing / Outdated / Good
    contacted = db.Column(db.Boolean, default=False)
    date_added = db.Column(db.DateTime, default=datetime.utcnow)

    __table_args__ = (
        db.UniqueConstraint('business_name', 'location', name='unique_lead'),
    )

    def __repr__(self):
        return f"<Lead {self.business_name} | {self.website_status}>"
