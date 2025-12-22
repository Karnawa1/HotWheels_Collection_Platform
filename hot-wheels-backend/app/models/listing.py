"""
Listing Model
Marketplace listings for sale/trade/auction
"""

from app import db
from datetime import datetime
from sqlalchemy import CheckConstraint


class Listing(db.Model):
    """Listing entity - marketplace listings for sale/trade"""

    __tablename__ = 'listings'

    listingid = db.Column('listing_id', db.Integer, primary_key=True)
    sellerid = db.Column('seller_id', db.Integer, db.ForeignKey('users.user_id'), nullable=False, index=True)
    collectionitemid = db.Column('collection_item_id', db.Integer, db.ForeignKey('user_collections.collection_id'))
    modelid = db.Column('model_id', db.Integer, db.ForeignKey('car_models.model_id'), nullable=False, index=True)
    listingtype = db.Column('listing_type', db.String(20), nullable=False)
    price = db.Column(db.Numeric(10, 2))
    condition = db.Column(db.String(20), nullable=False)
    description = db.Column(db.Text)
    status = db.Column(db.String(20), default='active', index=True)
    viewscount = db.Column('views_count', db.Integer, default=0)
    createdat = db.Column('created_at', db.DateTime, default=datetime.utcnow, nullable=False)
    expiresat = db.Column('expires_at', db.DateTime)
    soldat = db.Column('sold_at', db.DateTime)

    # Constraints
    __table_args__ = (
        CheckConstraint(
            "listing_type IN ('sale', 'trade', 'auction')",
            name='check_listing_type'
        ),
        CheckConstraint('price IS NULL OR price > 0', name='check_price_positive'),
        CheckConstraint(
            "status IN ('active', 'sold', 'cancelled', 'expired')",
            name='check_listing_status'
        ),
        CheckConstraint(
            "condition IN ('Mint', 'Near Mint', 'Excellent', 'Good', 'Fair', 'Poor')",
            name='check_listing_condition'
        ),
    )

    # Relationships
    seller = db.relationship('User', foreign_keys=[sellerid], back_populates='listings')
    carmodel = db.relationship('CarModel', back_populates='listings')
    collectionitem = db.relationship('UserCollection', back_populates='listings')
    transactions = db.relationship('Transaction', back_populates='listing', lazy='dynamic')

    def increment_views(self):
        """Increment view counter"""
        self.viewscount += 1
        db.session.commit()

    def mark_as_sold(self):
        """Mark listing as sold"""
        self.status = 'sold'
        self.soldat = datetime.utcnow()
        if self.collectionitem:
            self.collectionitem.isforsale = False
        db.session.commit()

    def to_dict(self, include_relations=False):
        """Convert model to dictionary"""
        data = {
            'listing_id': self.listingid,
            'seller_id': self.sellerid,
            'collection_item_id': self.collectionitemid,
            'model_id': self.modelid,
            'listing_type': self.listingtype,
            'price': float(self.price) if self.price else None,
            'condition': self.condition,
            'description': self.description,
            'status': self.status,
            'views_count': self.viewscount,
            'created_at': self.createdat.isoformat() if self.createdat else None,
            'expires_at': self.expiresat.isoformat() if self.expiresat else None,
            'sold_at': self.soldat.isoformat() if self.soldat else None
        }

        if include_relations:
            if self.seller:
                data['seller'] = {
                    'username': self.seller.username,
                    'is_verified': self.seller.isverified
                }
            if self.carmodel:
                data['car_model'] = self.carmodel.to_dict(include_relations=True)

        return data

    def __repr__(self):
        return f'<Listing {self.listingid}: {self.listingtype}>'
