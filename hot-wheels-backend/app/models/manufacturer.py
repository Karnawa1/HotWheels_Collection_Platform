"""
Manufacturer Model
Represents die-cast toy manufacturers (Mattel, Matchbox, etc.)
"""

from app import db
from datetime import datetime


class Manufacturer(db.Model):
    """Manufacturer entity - stores information about toy car manufacturers"""

    __tablename__ = 'manufacturers'

    manufacturerid = db.Column('manufacturer_id', db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    country = db.Column(db.String(50))
    foundedyear = db.Column('founded_year', db.Integer)
    createdat = db.Column('created_at', db.DateTime, default=datetime.utcnow, nullable=False)

    # Relationships
    series = db.relationship('Series', back_populates='manufacturer', lazy='dynamic')
    castings = db.relationship('Casting', back_populates='manufacturer', lazy='dynamic')

    def to_dict(self):
        """Convert model to dictionary"""
        return {
            'manufacturer_id': self.manufacturerid,
            'name': self.name,
            'country': self.country,
            'founded_year': self.foundedyear,
            'created_at': self.createdat.isoformat() if self.createdat else None
        }

    def __repr__(self):
        return f'<Manufacturer {self.name}>'
