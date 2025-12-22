"""
Series Model
Represents Hot Wheels series (Mainline, Treasure Hunt, etc.)
"""

from app import db
from datetime import datetime
from sqlalchemy import CheckConstraint, UniqueConstraint


class Series(db.Model):
    """Series entity - different Hot Wheels series and collections"""

    __tablename__ = 'series'

    seriesid = db.Column('series_id', db.Integer, primary_key=True)
    seriesname = db.Column('series_name', db.String(150), nullable=False)
    releaseyear = db.Column('release_year', db.Integer, nullable=False)
    manufacturerid = db.Column('manufacturer_id', db.Integer, db.ForeignKey('manufacturers.manufacturer_id'))
    description = db.Column(db.Text)
    islimitededition = db.Column('is_limited_edition', db.Boolean, default=False)
    createdat = db.Column('created_at', db.DateTime, default=datetime.utcnow, nullable=False)

    # Constraints
    __table_args__ = (
        CheckConstraint('release_year >= 1968', name='check_series_year'),
        UniqueConstraint('series_name', 'release_year', name='unique_series_per_year'),
    )

    # Relationships
    manufacturer = db.relationship('Manufacturer', back_populates='series')
    carmodels = db.relationship('CarModel', back_populates='series', lazy='dynamic')

    def to_dict(self):
        """Convert model to dictionary"""
        return {
            'series_id': self.seriesid,
            'series_name': self.seriesname,
            'release_year': self.releaseyear,
            'manufacturer_id': self.manufacturerid,
            'description': self.description,
            'is_limited_edition': self.islimitededition,
            'created_at': self.createdat.isoformat() if self.createdat else None
        }

    def __repr__(self):
        return f'<Series {self.seriesname} ({self.releaseyear})>'
