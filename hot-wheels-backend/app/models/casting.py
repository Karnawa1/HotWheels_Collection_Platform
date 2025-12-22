"""
Casting Model
Represents the base casting/tooling of a Hot Wheels model
"""

from app import db
from datetime import datetime
from sqlalchemy import CheckConstraint


class Casting(db.Model):
    """Casting entity - the base tooling/mold for a car model"""

    __tablename__ = 'castings'

    castingid = db.Column('casting_id', db.Integer, primary_key=True)
    castingname = db.Column('casting_name', db.String(200), nullable=False)
    firstreleaseyear = db.Column('first_release_year', db.Integer, nullable=False)
    manufacturerid = db.Column('manufacturer_id', db.Integer, db.ForeignKey('manufacturers.manufacturer_id'))
    scale = db.Column(db.String(10), default='1:64')
    designer = db.Column(db.String(100))
    basedonrealcar = db.Column('based_on_real_car', db.Boolean, default=False)
    realcarmodel = db.Column('real_car_model', db.String(200))
    createdat = db.Column('created_at', db.DateTime, default=datetime.utcnow, nullable=False)

    # Constraints
    __table_args__ = (
        CheckConstraint('first_release_year >= 1968', name='check_casting_year'),
    )

    # Relationships
    manufacturer = db.relationship('Manufacturer', back_populates='castings')
    carmodels = db.relationship('CarModel', back_populates='casting', lazy='dynamic')

    def to_dict(self, include_models=False):
        """Convert model to dictionary"""
        data = {
            'casting_id': self.castingid,
            'casting_name': self.castingname,
            'first_release_year': self.firstreleaseyear,
            'manufacturer_id': self.manufacturerid,
            'scale': self.scale,
            'designer': self.designer,
            'based_on_real_car': self.basedonrealcar,
            'real_car_model': self.realcarmodel,
            'created_at': self.createdat.isoformat() if self.createdat else None
        }

        if include_models:
            data['models_count'] = self.carmodels.count()

        return data

    def __repr__(self):
        return f'<Casting {self.castingname}>'
