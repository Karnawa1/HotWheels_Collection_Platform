"""
Collection Service
Handles user collections and wishlists
"""

from typing import Optional, Tuple, List, Dict
from datetime import datetime, date
from flask import current_app
from sqlalchemy import and_, or_
from app import db
from app.models.user import User, UserCollection, Wishlist
from app.models.car_model import CarModel
from app.utils.validators import validate_condition, validate_price, validate_quantity, validate_priority
from app.utils.constants import ERROR_MESSAGES, SUCCESS_MESSAGES
from app.utils.helpers import paginate_query


class CollectionService:
    """
    Collection management service
    Single Responsibility: Handle collection and wishlist operations
    """

    @staticmethod
    def add_to_collection(user_id: int, model_id: int, **kwargs) -> Tuple[Optional[UserCollection], Optional[str]]:
        """
        Add a car model to user's collection

        Args:
            user_id: User ID
            model_id: Car model ID
            **kwargs: Additional fields (condition, price, quantity, etc.)

        Returns:
            Tuple of (collection_item, error_message)
        """
        # Verify user exists
        user = User.query.filter_by(userid=user_id, isactive=True).first()
        if not user:
            return None, ERROR_MESSAGES['USER_NOT_FOUND']

        # Verify model exists
        model = CarModel.query.filter_by(modelid=model_id).first()
        if not model:
            return None, ERROR_MESSAGES['MODEL_NOT_FOUND']

        # Validate condition if provided
        if 'condition' in kwargs:
            is_valid, error = validate_condition(kwargs['condition'])
            if not is_valid:
                return None, error

        # Validate acquisition price if provided
        if 'acquisitionprice' in kwargs and kwargs['acquisitionprice']:
            is_valid, error = validate_price(kwargs['acquisitionprice'])
            if not is_valid:
                return None, error

        # Validate quantity if provided
        if 'quantity' in kwargs:
            is_valid, error = validate_quantity(kwargs['quantity'])
            if not is_valid:
                return None, error

        try:
            # Create collection item
            collection_item = UserCollection(
                userid=user_id,
                modelid=model_id,
                acquisitiondate=kwargs.get('acquisitiondate', date.today()),
                acquisitionprice=kwargs.get('acquisitionprice'),
                condition=kwargs.get('condition', 'Mint'),
                isinpackage=kwargs.get('isinpackage', True),
                packagecondition=kwargs.get('packagecondition'),
                quantity=kwargs.get('quantity', 1),
                storagelocation=kwargs.get('storagelocation'),
                notes=kwargs.get('notes'),
                isfortrade=kwargs.get('isfortrade', False),
                isforsale=kwargs.get('isforsale', False)
            )

            db.session.add(collection_item)
            db.session.commit()

            current_app.logger.info(f"Added model {model_id} to collection for user {user_id}")

            return collection_item, None

        except Exception as e:
            db.session.rollback()
            current_app.logger.error(f"Add to collection error: {str(e)}")
            return None, "Failed to add to collection"

    @staticmethod
    def get_user_collection(user_id: int, page: int = 1, per_page: int = 20, **filters) -> Dict:
        """
        Get user's collection with pagination and filters

        Args:
            user_id: User ID
            page: Page number
            per_page: Items per page
            **filters: Optional filters (for_sale, for_trade, condition, etc.)

        Returns:
            Dictionary with paginated collection data
        """
        query = UserCollection.query.filter_by(userid=user_id)

        # Apply filters
        if filters.get('forsale'):
            query = query.filter_by(isforsale=True)

        if filters.get('fortrade'):
            query = query.filter_by(isfortrade=True)

        if filters.get('condition'):
            query = query.filter_by(condition=filters['condition'])

        # Order by most recent first
        query = query.order_by(UserCollection.createdat.desc())

        return paginate_query(query, page, per_page)

    @staticmethod
    def update_collection_item(collection_id: int, user_id: int, **kwargs) -> Tuple[Optional[UserCollection], Optional[str]]:
        """
        Update a collection item

        Args:
            collection_id: Collection item ID
            user_id: User ID (for ownership verification)
            **kwargs: Fields to update

        Returns:
            Tuple of (collection_item, error_message)
        """
        item = UserCollection.query.filter_by(
            collectionid=collection_id,
            userid=user_id
        ).first()

        if not item:
            return None, "Collection item not found"

        # Validate condition if being updated
        if 'condition' in kwargs:
            is_valid, error = validate_condition(kwargs['condition'])
            if not is_valid:
                return None, error

        try:
            # Update allowed fields
            allowed_fields = [
                'acquisitionprice', 'condition', 'isinpackage', 
                'packagecondition', 'quantity', 'storagelocation', 
                'notes', 'isfortrade', 'isforsale'
            ]

            for field in allowed_fields:
                if field in kwargs:
                    setattr(item, field, kwargs[field])

            db.session.commit()
            current_app.logger.info(f"Updated collection item {collection_id}")

            return item, None

        except Exception as e:
            db.session.rollback()
            current_app.logger.error(f"Update collection item error: {str(e)}")
            return None, "Failed to update collection item"

    @staticmethod
    def remove_from_collection(collection_id: int, user_id: int) -> Tuple[bool, Optional[str]]:
        """
        Remove item from collection

        Args:
            collection_id: Collection item ID
            user_id: User ID (for ownership verification)

        Returns:
            Tuple of (success, error_message)
        """
        item = UserCollection.query.filter_by(
            collectionid=collection_id,
            userid=user_id
        ).first()

        if not item:
            return False, "Collection item not found"

        try:
            db.session.delete(item)
            db.session.commit()

            current_app.logger.info(f"Removed collection item {collection_id}")
            return True, None

        except Exception as e:
            db.session.rollback()
            current_app.logger.error(f"Remove from collection error: {str(e)}")
            return False, "Failed to remove from collection"

    # WISHLIST METHODS

    @staticmethod
    def add_to_wishlist(user_id: int, model_id: int, **kwargs) -> Tuple[Optional[Wishlist], Optional[str]]:
        """
        Add a model to user's wishlist

        Args:
            user_id: User ID
            model_id: Car model ID
            **kwargs: Additional fields (priority, max_price_willing, notes)

        Returns:
            Tuple of (wishlist_item, error_message)
        """
        # Verify model exists
        model = CarModel.query.filter_by(modelid=model_id).first()
        if not model:
            return None, ERROR_MESSAGES['MODEL_NOT_FOUND']

        # Check if already in wishlist
        existing = Wishlist.query.filter_by(
            userid=user_id,
            modelid=model_id
        ).first()

        if existing:
            return None, "Model already in wishlist"

        # Validate priority if provided
        if 'priority' in kwargs:
            is_valid, error = validate_priority(kwargs['priority'])
            if not is_valid:
                return None, error

        try:
            wishlist_item = Wishlist(
                userid=user_id,
                modelid=model_id,
                priority=kwargs.get('priority', 3),
                maxpricewilling=kwargs.get('maxpricewilling'),
                notes=kwargs.get('notes')
            )

            db.session.add(wishlist_item)
            db.session.commit()

            current_app.logger.info(f"Added model {model_id} to wishlist for user {user_id}")

            return wishlist_item, None

        except Exception as e:
            db.session.rollback()
            current_app.logger.error(f"Add to wishlist error: {str(e)}")
            return None, "Failed to add to wishlist"

    @staticmethod
    def get_user_wishlist(user_id: int, page: int = 1, per_page: int = 20) -> Dict:
        """
        Get user's wishlist

        Args:
            user_id: User ID
            page: Page number
            per_page: Items per page

        Returns:
            Dictionary with paginated wishlist data
        """
        query = Wishlist.query.filter_by(userid=user_id).order_by(
            Wishlist.priority.desc(),
            Wishlist.createdat.desc()
        )

        return paginate_query(query, page, per_page)

    @staticmethod
    def remove_from_wishlist(wishlist_id: int, user_id: int) -> Tuple[bool, Optional[str]]:
        """
        Remove item from wishlist

        Args:
            wishlist_id: Wishlist item ID
            user_id: User ID (for ownership verification)

        Returns:
            Tuple of (success, error_message)
        """
        item = Wishlist.query.filter_by(
            wishlistid=wishlist_id,
            userid=user_id
        ).first()

        if not item:
            return False, "Wishlist item not found"

        try:
            db.session.delete(item)
            db.session.commit()

            current_app.logger.info(f"Removed wishlist item {wishlist_id}")
            return True, None

        except Exception as e:
            db.session.rollback()
            current_app.logger.error(f"Remove from wishlist error: {str(e)}")
            return False, "Failed to remove from wishlist"

    @staticmethod
    def get_collection_stats(user_id: int) -> Dict:
        """
        Get statistics about user's collection

        Args:
            user_id: User ID

        Returns:
            Dictionary with collection statistics
        """
        from sqlalchemy import func

        total_items = UserCollection.query.filter_by(userid=user_id).count()
        total_models = db.session.query(
            func.count(func.distinct(UserCollection.modelid))
        ).filter_by(userid=user_id).scalar()

        for_sale = UserCollection.query.filter_by(
            userid=user_id, 
            isforsale=True
        ).count()

        for_trade = UserCollection.query.filter_by(
            userid=user_id, 
            isfortrade=True
        ).count()

        wishlist_count = Wishlist.query.filter_by(userid=user_id).count()

        return {
            'total_items': total_items,
            'unique_models': total_models,
            'items_for_sale': for_sale,
            'items_for_trade': for_trade,
            'wishlist_items': wishlist_count
        }