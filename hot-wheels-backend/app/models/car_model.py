"""
CarModel Model
Represents specific Hot Wheels car variants with colors and details
"""

from app import db
from datetime import datetime
from sqlalchemy import CheckConstraint, UniqueConstraint


class CarModel(db.Model):
    """CarModel entity - specific color/variant of a casting"""

    __tablename__ = 'car_models'

    modelid = db.Column('model_id', db.Integer, primary_key=True)
    castingid = db.Column('casting_id', db.Integer, db.ForeignKey('castings.casting_id'), nullable=False)
    seriesid = db.Column('series_id', db.Integer, db.ForeignKey('series.series_id'))
    releaseyear = db.Column('release_year', db.Integer, nullable=False)
    color = db.Column(db.String(50), nullable=False)
    tampodesign = db.Column('tampo_design', db.String(200))
    wheeltype = db.Column('wheel_type', db.String(100))
    basecolor = db.Column('base_color', db.String(50))
    windowcolor = db.Column('window_color', db.String(50))
    interiorcolor = db.Column('interior_color', db.String(50))
    productioncode = db.Column('production_code', db.String(10))
    sku = db.Column(db.String(50), unique=True)
    raritylevel = db.Column('rarity_level', db.String(20))
    estimatedproductionquantity = db.Column('estimated_production_quantity', db.Integer)
    msrp = db.Column(db.Numeric(10, 2))
    createdat = db.Column('created_at', db.DateTime, default=datetime.utcnow, nullable=False)
    updatedat = db.Column('updated_at', db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Constraints
    __table_args__ = (
        CheckConstraint(
            "rarity_level IN ('Common', 'Uncommon', 'Rare', 'Chase', 'Super Treasure Hunt')",
            name='check_rarity_level'
        ),
        UniqueConstraint(
            'casting_id', 'series_id', 'release_year', 'color', 'tampo_design',
            name='unique_car_variant'
        ),
    )

    # Relationships
    casting = db.relationship('Casting', back_populates='carmodels')
    series = db.relationship('Series', back_populates='carmodels')
    usercollections = db.relationship('UserCollection', back_populates='carmodel', lazy='dynamic')
    listings = db.relationship('Listing', back_populates='carmodel', lazy='dynamic')
    wishlists = db.relationship('Wishlist', back_populates='carmodel', lazy='dynamic')

    def to_dict(self, include_relations=False):
        """Convert model to dictionary"""
        data = {
            'model_id': self.modelid,
            'casting_id': self.castingid,
            'series_id': self.seriesid,
            'release_year': self.releaseyear,
            'color': self.color,
            'tampo_design': self.tampodesign,
            'wheel_type': self.wheeltype,
            'base_color': self.basecolor,
            'window_color': self.windowcolor,
            'interior_color': self.interiorcolor,
            'production_code': self.productioncode,
            'sku': self.sku,
            'rarity_level': self.raritylevel,
            'estimated_production_quantity': self.estimatedproductionquantity,
            'msrp': float(self.msrp) if self.msrp else None,
            'created_at': self.createdat.isoformat() if self.createdat else None,
            'updated_at': self.updatedat.isoformat() if self.updatedat else None
        }

        if include_relations:
            if self.casting:
                data['casting_name'] = self.casting.castingname
            if self.series:
                data['series_name'] = self.series.seriesname

        return data

    def __repr__(self):
        return f'<CarModel {self.modelid}: {self.color}>'
