"""
Transaction Model
Completed marketplace transactions
"""

from app import db
from datetime import datetime
from sqlalchemy import CheckConstraint


class Transaction(db.Model):
    """Transaction entity - completed marketplace transactions"""

    __tablename__ = 'transactions'

    transactionid = db.Column('transaction_id', db.Integer, primary_key=True)
    listingid = db.Column('listing_id', db.Integer, db.ForeignKey('listings.listing_id'), nullable=False)
    buyerid = db.Column('buyer_id', db.Integer, db.ForeignKey('users.user_id'), nullable=False, index=True)
    sellerid = db.Column('seller_id', db.Integer, db.ForeignKey('users.user_id'), nullable=False, index=True)
    transactiontype = db.Column('transaction_type', db.String(20), nullable=False)
    amount = db.Column(db.Numeric(10, 2), nullable=False)
    paymentmethod = db.Column('payment_method', db.String(50))
    paymentstatus = db.Column('payment_status', db.String(20), default='pending')
    shippingstatus = db.Column('shipping_status', db.String(20), default='not_shipped')
    trackingnumber = db.Column('tracking_number', db.String(100))
    createdat = db.Column('created_at', db.DateTime, default=datetime.utcnow, nullable=False, index=True)
    completedat = db.Column('completed_at', db.DateTime)

    # Constraints
    __table_args__ = (
        CheckConstraint(
            "transaction_type IN ('purchase', 'trade')",
            name='check_transaction_type'
        ),
        CheckConstraint('amount >= 0', name='check_amount_positive'),
        CheckConstraint(
            "payment_status IN ('pending', 'completed', 'failed', 'refunded')",
            name='check_payment_status'
        ),
        CheckConstraint(
            "shipping_status IN ('not_shipped', 'shipped', 'in_transit', 'delivered')",
            name='check_shipping_status'
        ),
        CheckConstraint('buyer_id != seller_id', name='check_no_self_transaction'),
    )

    # Relationships
    listing = db.relationship('Listing', back_populates='transactions')
    buyer = db.relationship('User', foreign_keys=[buyerid], back_populates='purchases')
    seller = db.relationship('User', foreign_keys=[sellerid], back_populates='sales')
    reviews = db.relationship('Review', back_populates='transaction', lazy='dynamic')

    def complete_transaction(self):
        """Mark transaction as completed"""
        self.paymentstatus = 'completed'
        self.completedat = datetime.utcnow()
        db.session.commit()

    def to_dict(self, include_relations=False):
        """Convert model to dictionary"""
        data = {
            'transaction_id': self.transactionid,
            'listing_id': self.listingid,
            'buyer_id': self.buyerid,
            'seller_id': self.sellerid,
            'transaction_type': self.transactiontype,
            'amount': float(self.amount) if self.amount else None,
            'payment_method': self.paymentmethod,
            'payment_status': self.paymentstatus,
            'shipping_status': self.shippingstatus,
            'tracking_number': self.trackingnumber,
            'created_at': self.createdat.isoformat() if self.createdat else None,
            'completed_at': self.completedat.isoformat() if self.completedat else None
        }

        if include_relations:
            if self.buyer:
                data['buyer_username'] = self.buyer.username
            if self.seller:
                data['seller_username'] = self.seller.username

        return data

    def __repr__(self):
        return f'<Transaction {self.transactionid}>'


class Review(db.Model):
    """Review entity - user reviews after transactions"""

    __tablename__ = 'reviews'

    reviewid = db.Column('review_id', db.Integer, primary_key=True)
    transactionid = db.Column('transaction_id', db.Integer, db.ForeignKey('transactions.transaction_id'), 
                             nullable=False)
    reviewerid = db.Column('reviewer_id', db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    revieweeid = db.Column('reviewee_id', db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    rating = db.Column(db.Integer, nullable=False)
    comment = db.Column(db.Text)
    createdat = db.Column('created_at', db.DateTime, default=datetime.utcnow, nullable=False)

    # Constraints
    __table_args__ = (
        CheckConstraint('rating BETWEEN 1 AND 5', name='check_rating_range'),
        db.UniqueConstraint('transaction_id', 'reviewer_id', 
                           name='unique_review_per_transaction'),
    )

    # Relationships
    transaction = db.relationship('Transaction', back_populates='reviews')
    reviewer = db.relationship('User', foreign_keys=[reviewerid], 
                               back_populates='reviews_written')
    reviewee = db.relationship('User', foreign_keys=[revieweeid], 
                              back_populates='reviews_received')

    def to_dict(self, include_users=False):
        """Convert model to dictionary"""
        data = {
            'review_id': self.reviewid,
            'transaction_id': self.transactionid,
            'reviewer_id': self.reviewerid,
            'reviewee_id': self.revieweeid,
            'rating': self.rating,
            'comment': self.comment,
            'created_at': self.createdat.isoformat() if self.createdat else None
        }

        if include_users:
            if self.reviewer:
                data['reviewer_username'] = self.reviewer.username
            if self.reviewee:
                data['reviewee_username'] = self.reviewee.username

        return data

    def __repr__(self):
        return f'<Review {self.reviewid}: {self.rating}/5>'
