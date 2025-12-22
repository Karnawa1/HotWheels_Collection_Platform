"""
User Model
Represents platform users with authentication
"""

from app import db
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy import CheckConstraint


class User(db.Model):
    """User entity - platform users (collectors, traders, admins)"""

    __tablename__ = 'users'

    userid = db.Column('user_id', db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False, index=True)
    email = db.Column(db.String(150), unique=True, nullable=False, index=True)
    passwordhash = db.Column('password_hash', db.String(255), nullable=False)
    fullname = db.Column('full_name', db.String(150))
    country = db.Column(db.String(50))
    city = db.Column(db.String(100))
    profileimageurl = db.Column('profile_image_url', db.Text)
    bio = db.Column(db.Text)
    isverified = db.Column('is_verified', db.Boolean, default=False)
    isactive = db.Column('is_active', db.Boolean, default=True)
    role = db.Column(db.String(20), default='collector')
    createdat = db.Column('created_at', db.DateTime, default=datetime.utcnow, nullable=False)
    lastlogin = db.Column('last_login', db.DateTime)

    # Constraints
    __table_args__ = (
        CheckConstraint(
            "role IN ('collector', 'trader', 'admin', 'moderator')",
            name='check_user_role'
        ),
        CheckConstraint(
            "email ~ '^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\\.[A-Za-z]{2,}$'",
            name='check_email_format'
        ),
    )

    # Relationships
    collections = db.relationship('UserCollection', back_populates='user', 
                                 cascade='all, delete-orphan', lazy='dynamic')
    wishlists = db.relationship('Wishlist', back_populates='user',
                               cascade='all, delete-orphan', lazy='dynamic')
    listings = db.relationship('Listing', foreign_keys='Listing.sellerid',
                              back_populates='seller', lazy='dynamic')
    purchases = db.relationship('Transaction', foreign_keys='Transaction.buyerid',
                               back_populates='buyer', lazy='dynamic')
    sales = db.relationship('Transaction', foreign_keys='Transaction.sellerid',
                           back_populates='seller', lazy='dynamic')
    reviews_written = db.relationship('Review', foreign_keys='Review.reviewerid',
                                     back_populates='reviewer', lazy='dynamic')
    reviews_received = db.relationship('Review', foreign_keys='Review.revieweeid',
                                      back_populates='reviewee', lazy='dynamic')

    def set_password(self, password):
        """Hash password using bcrypt (via werkzeug)"""
        self.passwordhash = generate_password_hash(password, method='pbkdf2:sha256')

    def check_password(self, password):
        """Verify password against hash"""
        return check_password_hash(self.passwordhash, password)

    def update_last_login(self):
        """Update last login timestamp"""
        self.lastlogin = datetime.utcnow()
        db.session.commit()

    def to_dict(self, include_sensitive=False):
        """Convert model to dictionary"""
        data = {
            'user_id': self.userid,
            'username': self.username,
            'full_name': self.fullname,
            'country': self.country,
            'city': self.city,
            'profile_image_url': self.profileimageurl,
            'bio': self.bio,
            'is_verified': self.isverified,
            'is_active': self.isactive,
            'role': self.role,
            'created_at': self.createdat.isoformat() if self.createdat else None,
            'last_login': self.lastlogin.isoformat() if self.lastlogin else None
        }

        if include_sensitive:
            # Mask email for privacy
            email_parts = self.email.split('@')
            if len(email_parts) == 2:
                data['email'] = f"{email_parts[0][:3]}***@{email_parts[1]}"
            else:
                data['email'] = "***@***"

        return data

    def __repr__(self):
        return f'<User {self.username}>'


class UserCollection(db.Model):
    """UserCollection entity - user's personal car collection"""

    __tablename__ = 'user_collections'

    collectionid = db.Column('collection_id', db.Integer, primary_key=True)
    userid = db.Column('user_id', db.Integer, db.ForeignKey('users.user_id', ondelete='CASCADE'), 
                      nullable=False, index=True)
    modelid = db.Column('model_id', db.Integer, db.ForeignKey('car_models.model_id'), nullable=False)
    acquisitiondate = db.Column('acquisition_date', db.Date, default=datetime.utcnow)
    acquisitionprice = db.Column('acquisition_price', db.Numeric(10, 2))
    condition = db.Column(db.String(20))
    isinpackage = db.Column('is_in_package', db.Boolean, default=True)
    packagecondition = db.Column('package_condition', db.String(20))
    quantity = db.Column(db.Integer, default=1)
    storagelocation = db.Column('storage_location', db.String(100))
    notes = db.Column(db.Text)
    isfortrade = db.Column('is_for_trade', db.Boolean, default=False, index=True)
    isforsale = db.Column('is_for_sale', db.Boolean, default=False, index=True)
    createdat = db.Column('created_at', db.DateTime, default=datetime.utcnow)
    updatedat = db.Column('updated_at', db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Constraints
    __table_args__ = (
        CheckConstraint(
            "condition IN ('Mint', 'Near Mint', 'Excellent', 'Good', 'Fair', 'Poor')",
            name='check_collection_condition'
        ),
        CheckConstraint('quantity > 0', name='check_quantity_positive'),
        db.UniqueConstraint('user_id', 'model_id', 'acquisition_date', 
                           name='unique_collection_item'),
    )

    # Relationships
    user = db.relationship('User', back_populates='collections')
    carmodel = db.relationship('CarModel', back_populates='usercollections')
    listings = db.relationship('Listing', back_populates='collectionitem', lazy='dynamic')

    def to_dict(self, include_model=False):
        """Convert model to dictionary"""
        data = {
            'collection_id': self.collectionid,
            'user_id': self.userid,
            'model_id': self.modelid,
            'acquisition_date': self.acquisitiondate.isoformat() if self.acquisitiondate else None,
            'acquisition_price': float(self.acquisitionprice) if self.acquisitionprice else None,
            'condition': self.condition,
            'is_in_package': self.isinpackage,
            'package_condition': self.packagecondition,
            'quantity': self.quantity,
            'storage_location': self.storagelocation,
            'notes': self.notes,
            'is_for_trade': self.isfortrade,
            'is_for_sale': self.isforsale,
            'created_at': self.createdat.isoformat() if self.createdat else None,
            'updated_at': self.updatedat.isoformat() if self.updatedat else None
        }

        if include_model and self.carmodel:
            data['car_model'] = self.carmodel.to_dict(include_relations=True)

        return data

    def __repr__(self):
        return f'<UserCollection {self.collectionid}>'


class Wishlist(db.Model):
    """Wishlist entity - models users want to acquire"""

    __tablename__ = 'wishlists'

    wishlistid = db.Column('wishlist_id', db.Integer, primary_key=True)
    userid = db.Column('user_id', db.Integer, db.ForeignKey('users.user_id', ondelete='CASCADE'),
                      nullable=False, index=True)
    modelid = db.Column('model_id', db.Integer, db.ForeignKey('car_models.model_id'), nullable=False)
    priority = db.Column(db.Integer)
    maxpricewilling = db.Column('max_price_willing', db.Numeric(10, 2))
    notes = db.Column(db.Text)
    createdat = db.Column('created_at', db.DateTime, default=datetime.utcnow)

    # Constraints
    __table_args__ = (
        CheckConstraint('priority BETWEEN 1 AND 5', name='check_priority_range'),
        CheckConstraint('max_price_willing >= 0', name='check_max_price_positive'),
        db.UniqueConstraint('user_id', 'model_id', name='unique_wishlist_item'),
    )

    # Relationships
    user = db.relationship('User', back_populates='wishlists')
    carmodel = db.relationship('CarModel', back_populates='wishlists')

    def to_dict(self, include_model=False):
        """Convert model to dictionary"""
        data = {
            'wishlist_id': self.wishlistid,
            'user_id': self.userid,
            'model_id': self.modelid,
            'priority': self.priority,
            'max_price_willing': float(self.maxpricewilling) if self.maxpricewilling else None,
            'notes': self.notes,
            'created_at': self.createdat.isoformat() if self.createdat else None
        }

        if include_model and self.carmodel:
            data['car_model'] = self.carmodel.to_dict(include_relations=True)

        return data

    def __repr__(self):
        return f'<Wishlist {self.wishlistid}>'
