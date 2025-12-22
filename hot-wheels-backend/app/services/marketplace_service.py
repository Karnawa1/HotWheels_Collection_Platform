"""
Marketplace Service
Handles listings, transactions, and reviews
"""

from typing import Optional, Tuple, Dict
from datetime import datetime
from flask import current_app
from sqlalchemy import and_, or_
from app import db
from app.models.user import User
from app.models.listing import Listing
from app.models.transaction import Transaction, Review
from app.models.car_model import CarModel
from app.utils.validators import (
    validate_listing_type, validate_condition, 
    validate_price, validate_rating, validate_transaction_type
)
from app.utils.constants import ERROR_MESSAGES, LISTING_STATUSES, PAYMENT_STATUSES
from app.utils.helpers import paginate_query


class MarketplaceService:
    """
    Marketplace service
    Single Responsibility: Handle marketplace operations
    """

    @staticmethod
    def create_listing(seller_id: int, model_id: int, listing_type: str, 
                      condition: str, **kwargs) -> Tuple[Optional[Listing], Optional[str]]:
        """
        Create a new marketplace listing

        Args:
            seller_id: Seller user ID
            model_id: Car model ID
            listing_type: Type of listing (sale, trade, auction)
            condition: Item condition
            **kwargs: Additional fields (price, description, etc.)

        Returns:
            Tuple of (listing, error_message)
        """
        # Validate inputs
        is_valid, error = validate_listing_type(listing_type)
        if not is_valid:
            return None, error

        is_valid, error = validate_condition(condition)
        if not is_valid:
            return None, error

        # Validate price for sales
        if listing_type == 'sale':
            if 'price' not in kwargs or not kwargs['price']:
                return None, "Price is required for sales"

            is_valid, error = validate_price(kwargs['price'])
            if not is_valid:
                return None, error

        # Verify seller exists
        seller = User.query.filter_by(userid=seller_id, isactive=True).first()
        if not seller:
            return None, ERROR_MESSAGES['USER_NOT_FOUND']

        # Verify model exists
        model = CarModel.query.filter_by(modelid=model_id).first()
        if not model:
            return None, ERROR_MESSAGES['MODEL_NOT_FOUND']

        try:
            listing = Listing(
                sellerid=seller_id,
                modelid=model_id,
                listingtype=listing_type,
                price=kwargs.get('price'),
                condition=condition,
                description=kwargs.get('description'),
                collectionitemid=kwargs.get('collectionitemid'),
                expiresat=kwargs.get('expiresat')
            )

            db.session.add(listing)
            db.session.commit()

            current_app.logger.info(f"Created listing {listing.listingid} by user {seller_id}")

            return listing, None

        except Exception as e:
            db.session.rollback()
            current_app.logger.error(f"Create listing error: {str(e)}")
            return None, "Failed to create listing"

    @staticmethod
    def get_active_listings(page: int = 1, per_page: int = 20, **filters) -> Dict:
        """
        Get active marketplace listings with filters

        Args:
            page: Page number
            per_page: Items per page
            **filters: Optional filters (model_id, listing_type, price_min/max, etc.)

        Returns:
            Dictionary with paginated listings
        """
        query = Listing.query.filter_by(status=LISTING_STATUSES['ACTIVE'])

        # Apply filters
        if filters.get('model_id'):
            query = query.filter_by(modelid=filters['model_id'])

        if filters.get('listing_type'):
            query = query.filter_by(listingtype=filters['listing_type'])

        if filters.get('seller_id'):
            query = query.filter_by(sellerid=filters['seller_id'])

        if filters.get('price_min'):
            query = query.filter(Listing.price >= filters['price_min'])

        if filters.get('price_max'):
            query = query.filter(Listing.price <= filters['price_max'])

        # Order by newest first
        query = query.order_by(Listing.createdat.desc())

        return paginate_query(query, page, per_page)

    @staticmethod
    def get_listing(listing_id: int, increment_views: bool = True) -> Optional[Listing]:
        """
        Get a single listing by ID

        Args:
            listing_id: Listing ID
            increment_views: Whether to increment view counter

        Returns:
            Listing object or None
        """
        listing = Listing.query.filter_by(listingid=listing_id).first()

        if listing and increment_views:
            listing.increment_views()

        return listing

    @staticmethod
    def update_listing(listing_id: int, seller_id: int, **kwargs) -> Tuple[Optional[Listing], Optional[str]]:
        """
        Update a listing

        Args:
            listing_id: Listing ID
            seller_id: Seller ID (for ownership verification)
            **kwargs: Fields to update

        Returns:
            Tuple of (listing, error_message)
        """
        listing = Listing.query.filter_by(
            listingid=listing_id,
            sellerid=seller_id
        ).first()

        if not listing:
            return None, ERROR_MESSAGES['LISTING_NOT_FOUND']

        if listing.status != LISTING_STATUSES['ACTIVE']:
            return None, "Cannot update inactive listing"

        try:
            # Update allowed fields
            if 'price' in kwargs:
                is_valid, error = validate_price(kwargs['price'])
                if not is_valid:
                    return None, error
                listing.price = kwargs['price']

            if 'description' in kwargs:
                listing.description = kwargs['description']

            if 'condition' in kwargs:
                is_valid, error = validate_condition(kwargs['condition'])
                if not is_valid:
                    return None, error
                listing.condition = kwargs['condition']

            db.session.commit()
            current_app.logger.info(f"Updated listing {listing_id}")

            return listing, None

        except Exception as e:
            db.session.rollback()
            current_app.logger.error(f"Update listing error: {str(e)}")
            return None, "Failed to update listing"

    @staticmethod
    def cancel_listing(listing_id: int, seller_id: int) -> Tuple[bool, Optional[str]]:
        """
        Cancel a listing

        Args:
            listing_id: Listing ID
            seller_id: Seller ID (for ownership verification)

        Returns:
            Tuple of (success, error_message)
        """
        listing = Listing.query.filter_by(
            listingid=listing_id,
            sellerid=seller_id
        ).first()

        if not listing:
            return False, ERROR_MESSAGES['LISTING_NOT_FOUND']

        if listing.status != LISTING_STATUSES['ACTIVE']:
            return False, "Listing is not active"

        try:
            listing.status = LISTING_STATUSES['CANCELLED']
            db.session.commit()

            current_app.logger.info(f"Cancelled listing {listing_id}")
            return True, None

        except Exception as e:
            db.session.rollback()
            current_app.logger.error(f"Cancel listing error: {str(e)}")
            return False, "Failed to cancel listing"

    # TRANSACTION METHODS

    @staticmethod
    def create_transaction(listing_id: int, buyer_id: int, **kwargs) -> Tuple[Optional[Transaction], Optional[str]]:
        """
        Create a new transaction (purchase or trade)

        Args:
            listing_id: Listing ID
            buyer_id: Buyer user ID
            **kwargs: Additional fields (payment_method, etc.)

        Returns:
            Tuple of (transaction, error_message)
        """
        listing = Listing.query.filter_by(listingid=listing_id).first()

        if not listing:
            return None, ERROR_MESSAGES['LISTING_NOT_FOUND']

        if listing.status != LISTING_STATUSES['ACTIVE']:
            return None, ERROR_MESSAGES['LISTING_NOT_ACTIVE']

        # Prevent self-purchase
        if listing.sellerid == buyer_id:
            return None, ERROR_MESSAGES['SELF_TRANSACTION']

        # Verify buyer exists
        buyer = User.query.filter_by(userid=buyer_id, isactive=True).first()
        if not buyer:
            return None, ERROR_MESSAGES['USER_NOT_FOUND']

        try:
            transaction_type = 'purchase' if listing.listingtype == 'sale' else 'trade'
            amount = listing.price if listing.price else 0

            transaction = Transaction(
                listingid=listing_id,
                buyerid=buyer_id,
                sellerid=listing.sellerid,
                transactiontype=transaction_type,
                amount=amount,
                paymentmethod=kwargs.get('paymentmethod'),
                paymentstatus=PAYMENT_STATUSES['PENDING']
            )

            db.session.add(transaction)

            # Mark listing as sold
            listing.mark_as_sold()

            db.session.commit()

            current_app.logger.info(f"Created transaction {transaction.transactionid}")

            return transaction, None

        except Exception as e:
            db.session.rollback()
            current_app.logger.error(f"Create transaction error: {str(e)}")
            return None, "Failed to create transaction"

    @staticmethod
    def get_user_transactions(user_id: int, as_buyer: bool = True, page: int = 1, per_page: int = 20) -> Dict:
        """
        Get user's transactions

        Args:
            user_id: User ID
            as_buyer: If True, get purchases; if False, get sales
            page: Page number
            per_page: Items per page

        Returns:
            Dictionary with paginated transactions
        """
        if as_buyer:
            query = Transaction.query.filter_by(buyerid=user_id)
        else:
            query = Transaction.query.filter_by(sellerid=user_id)

        query = query.order_by(Transaction.createdat.desc())

        return paginate_query(query, page, per_page)

    # REVIEW METHODS

    @staticmethod
    def create_review(transaction_id: int, reviewer_id: int, reviewee_id: int, 
                     rating: int, comment: str = None) -> Tuple[Optional[Review], Optional[str]]:
        """
        Create a review for a transaction

        Args:
            transaction_id: Transaction ID
            reviewer_id: Reviewer user ID
            reviewee_id: Reviewee user ID
            rating: Rating (1-5)
            comment: Optional comment

        Returns:
            Tuple of (review, error_message)
        """
        # Validate rating
        is_valid, error = validate_rating(rating)
        if not is_valid:
            return None, error

        # Verify transaction exists and user is participant
        transaction = Transaction.query.filter_by(
            transactionid=transaction_id
        ).filter(
            or_(
                Transaction.buyerid == reviewer_id,
                Transaction.sellerid == reviewer_id
            )
        ).first()

        if not transaction:
            return None, "Transaction not found or you are not a participant"

        # Check if review already exists
        existing = Review.query.filter_by(
            transactionid=transaction_id,
            reviewerid=reviewer_id
        ).first()

        if existing:
            return None, "You have already reviewed this transaction"

        try:
            review = Review(
                transactionid=transaction_id,
                reviewerid=reviewer_id,
                revieweeid=reviewee_id,
                rating=rating,
                comment=comment
            )

            db.session.add(review)
            db.session.commit()

            current_app.logger.info(f"Created review {review.reviewid}")

            return review, None

        except Exception as e:
            db.session.rollback()
            current_app.logger.error(f"Create review error: {str(e)}")
            return None, "Failed to create review"