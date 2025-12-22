"""
Unit Tests for Collection Service
Tests user collection and wishlist management
"""

import pytest
from decimal import Decimal
from datetime import date
from app.services.collection_service import CollectionService
from app.models.user import UserCollection, Wishlist


class TestCollectionServiceAddToCollection:
    """Tests for adding items to collection"""

    def test_add_to_collection_success(self, app, sample_user, sample_car_model):
        """Test successfully adding to collection"""
        with app.app_context():
            item, error = CollectionService.add_to_collection(
                user_id=sample_user.userid,
                model_id=sample_car_model.modelid,
                condition='Mint',
                acquisitionprice=4.99,
                quantity=1,
                notes='Test note'
            )
            
            assert item is not None
            assert error is None
            assert item.userid == sample_user.userid
            assert item.modelid == sample_car_model.modelid
            assert item.condition == 'Mint'

    def test_add_to_collection_with_defaults(self, app, sample_user, sample_car_model):
        """Test adding to collection with default values"""
        with app.app_context():
            item, error = CollectionService.add_to_collection(
                user_id=sample_user.userid,
                model_id=sample_car_model.modelid
            )
            
            assert item is not None
            assert error is None
            assert item.condition == 'Mint'  # Default
            assert item.quantity == 1  # Default
            assert item.isinpackage is True  # Default

    def test_add_to_collection_user_not_found(self, app, sample_car_model):
        """Test adding to collection with non-existent user"""
        with app.app_context():
            item, error = CollectionService.add_to_collection(
                user_id=99999,
                model_id=sample_car_model.modelid
            )
            
            assert item is None
            assert error is not None
            assert 'User not found' in error

    def test_add_to_collection_model_not_found(self, app, sample_user):
        """Test adding to collection with non-existent model"""
        with app.app_context():
            item, error = CollectionService.add_to_collection(
                user_id=sample_user.userid,
                model_id=99999
            )
            
            assert item is None
            assert error is not None
            assert 'model not found' in error.lower()

    def test_add_to_collection_invalid_condition(self, app, sample_user, sample_car_model):
        """Test adding to collection with invalid condition"""
        with app.app_context():
            item, error = CollectionService.add_to_collection(
                user_id=sample_user.userid,
                model_id=sample_car_model.modelid,
                condition='Perfect'  # Invalid
            )
            
            assert item is None
            assert error is not None
            assert 'condition' in error.lower()

    def test_add_to_collection_invalid_quantity(self, app, sample_user, sample_car_model):
        """Test adding to collection with invalid quantity"""
        with app.app_context():
            item, error = CollectionService.add_to_collection(
                user_id=sample_user.userid,
                model_id=sample_car_model.modelid,
                quantity=0  # Invalid
            )
            
            assert item is None
            assert error is not None

    def test_add_to_collection_for_sale(self, app, sample_user, sample_car_model):
        """Test adding to collection with for_sale flag"""
        with app.app_context():
            item, error = CollectionService.add_to_collection(
                user_id=sample_user.userid,
                model_id=sample_car_model.modelid,
                isforsale=True
            )
            
            assert item is not None
            assert item.isforsale is True


class TestCollectionServiceGetCollection:
    """Tests for getting user collection"""

    def test_get_user_collection(self, app, sample_user, sample_collection_item):
        """Test getting user's collection"""
        with app.app_context():
            result = CollectionService.get_user_collection(
                user_id=sample_user.userid
            )
            
            assert 'items' in result
            assert 'pagination' in result
            assert len(result['items']) >= 1

    def test_get_user_collection_empty(self, app, sample_user_2):
        """Test getting empty collection"""
        with app.app_context():
            result = CollectionService.get_user_collection(
                user_id=sample_user_2.userid
            )
            
            assert 'items' in result
            assert len(result['items']) == 0

    def test_get_user_collection_filter_for_sale(self, app, sample_user, sample_car_model):
        """Test filtering collection by for_sale"""
        with app.app_context():
            # Add item for sale
            CollectionService.add_to_collection(
                user_id=sample_user.userid,
                model_id=sample_car_model.modelid,
                isforsale=True
            )
            
            result = CollectionService.get_user_collection(
                user_id=sample_user.userid,
                forsale=True
            )
            
            for item in result['items']:
                assert item['is_for_sale'] is True

    def test_get_user_collection_pagination(self, app, sample_user):
        """Test collection pagination"""
        with app.app_context():
            result = CollectionService.get_user_collection(
                user_id=sample_user.userid,
                page=1,
                per_page=5
            )
            
            assert result['pagination']['per_page'] == 5
            assert result['pagination']['page'] == 1


class TestCollectionServiceUpdateItem:
    """Tests for updating collection items"""

    def test_update_collection_item_success(self, app, sample_user, sample_collection_item):
        """Test successfully updating collection item"""
        with app.app_context():
            item, error = CollectionService.update_collection_item(
                collection_id=sample_collection_item.collectionid,
                user_id=sample_user.userid,
                condition='Good',
                notes='Updated notes'
            )
            
            assert item is not None
            assert error is None
            assert item.condition == 'Good'
            assert item.notes == 'Updated notes'

    def test_update_collection_item_not_found(self, app, sample_user):
        """Test updating non-existent collection item"""
        with app.app_context():
            item, error = CollectionService.update_collection_item(
                collection_id=99999,
                user_id=sample_user.userid,
                condition='Good'
            )
            
            assert item is None
            assert error is not None
            assert 'not found' in error.lower()

    def test_update_collection_item_wrong_user(self, app, sample_user_2, sample_collection_item):
        """Test updating item belonging to another user"""
        with app.app_context():
            item, error = CollectionService.update_collection_item(
                collection_id=sample_collection_item.collectionid,
                user_id=sample_user_2.userid,  # Different user
                condition='Good'
            )
            
            assert item is None
            assert error is not None

    def test_update_collection_item_invalid_condition(self, app, sample_user, sample_collection_item):
        """Test updating with invalid condition"""
        with app.app_context():
            item, error = CollectionService.update_collection_item(
                collection_id=sample_collection_item.collectionid,
                user_id=sample_user.userid,
                condition='Invalid'
            )
            
            assert item is None
            assert error is not None


class TestCollectionServiceRemoveItem:
    """Tests for removing from collection"""

    def test_remove_from_collection_success(self, app, sample_user, sample_collection_item):
        """Test successfully removing from collection"""
        with app.app_context():
            collection_id = sample_collection_item.collectionid
            
            success, error = CollectionService.remove_from_collection(
                collection_id=collection_id,
                user_id=sample_user.userid
            )
            
            assert success is True
            assert error is None
            
            # Verify it's actually removed
            item = UserCollection.query.filter_by(collectionid=collection_id).first()
            assert item is None

    def test_remove_from_collection_not_found(self, app, sample_user):
        """Test removing non-existent item"""
        with app.app_context():
            success, error = CollectionService.remove_from_collection(
                collection_id=99999,
                user_id=sample_user.userid
            )
            
            assert success is False
            assert error is not None

    def test_remove_from_collection_wrong_user(self, app, sample_user_2, sample_collection_item):
        """Test removing item belonging to another user"""
        with app.app_context():
            success, error = CollectionService.remove_from_collection(
                collection_id=sample_collection_item.collectionid,
                user_id=sample_user_2.userid
            )
            
            assert success is False
            assert error is not None


class TestWishlistService:
    """Tests for wishlist operations"""

    def test_add_to_wishlist_success(self, app, sample_user, sample_car_model):
        """Test successfully adding to wishlist"""
        with app.app_context():
            item, error = CollectionService.add_to_wishlist(
                user_id=sample_user.userid,
                model_id=sample_car_model.modelid,
                priority=5,
                maxpricewilling=25.00,
                notes='Looking for mint'
            )
            
            assert item is not None
            assert error is None
            assert item.priority == 5

    def test_add_to_wishlist_duplicate(self, app, sample_user, sample_wishlist_item, sample_car_model):
        """Test adding duplicate to wishlist"""
        with app.app_context():
            item, error = CollectionService.add_to_wishlist(
                user_id=sample_user.userid,
                model_id=sample_car_model.modelid
            )
            
            assert item is None
            assert error is not None
            assert 'already' in error.lower()

    def test_add_to_wishlist_model_not_found(self, app, sample_user):
        """Test adding non-existent model to wishlist"""
        with app.app_context():
            item, error = CollectionService.add_to_wishlist(
                user_id=sample_user.userid,
                model_id=99999
            )
            
            assert item is None
            assert error is not None

    def test_add_to_wishlist_invalid_priority(self, app, sample_user, sample_car_model):
        """Test adding with invalid priority"""
        with app.app_context():
            item, error = CollectionService.add_to_wishlist(
                user_id=sample_user.userid,
                model_id=sample_car_model.modelid,
                priority=10  # Invalid
            )
            
            assert item is None
            assert error is not None

    def test_get_user_wishlist(self, app, sample_user, sample_wishlist_item):
        """Test getting user's wishlist"""
        with app.app_context():
            result = CollectionService.get_user_wishlist(
                user_id=sample_user.userid
            )
            
            assert 'items' in result
            assert len(result['items']) >= 1

    def test_remove_from_wishlist_success(self, app, sample_user, sample_wishlist_item):
        """Test successfully removing from wishlist"""
        with app.app_context():
            wishlist_id = sample_wishlist_item.wishlistid
            
            success, error = CollectionService.remove_from_wishlist(
                wishlist_id=wishlist_id,
                user_id=sample_user.userid
            )
            
            assert success is True
            assert error is None

    def test_remove_from_wishlist_not_found(self, app, sample_user):
        """Test removing non-existent wishlist item"""
        with app.app_context():
            success, error = CollectionService.remove_from_wishlist(
                wishlist_id=99999,
                user_id=sample_user.userid
            )
            
            assert success is False
            assert error is not None


class TestCollectionStats:
    """Tests for collection statistics"""

    def test_get_collection_stats(self, app, sample_user, sample_collection_item):
        """Test getting collection statistics"""
        with app.app_context():
            stats = CollectionService.get_collection_stats(
                user_id=sample_user.userid
            )
            
            assert 'total_items' in stats
            assert 'unique_models' in stats
            assert 'items_for_sale' in stats
            assert 'items_for_trade' in stats
            assert 'wishlist_items' in stats
            assert stats['total_items'] >= 1

    def test_get_collection_stats_empty(self, app, sample_user_2):
        """Test statistics for empty collection"""
        with app.app_context():
            stats = CollectionService.get_collection_stats(
                user_id=sample_user_2.userid
            )
            
            assert stats['total_items'] == 0
            assert stats['unique_models'] == 0


class TestCollectionModel:
    """Tests for UserCollection model"""

    def test_collection_item_to_dict(self, app, sample_collection_item):
        """Test UserCollection to_dict conversion"""
        with app.app_context():
            item_dict = sample_collection_item.to_dict()
            
            assert 'collection_id' in item_dict
            assert 'user_id' in item_dict
            assert 'model_id' in item_dict
            assert 'condition' in item_dict
            assert item_dict['condition'] == 'Mint'

    def test_collection_item_to_dict_with_model(self, app, sample_collection_item):
        """Test UserCollection to_dict with car model included"""
        with app.app_context():
            item_dict = sample_collection_item.to_dict(include_model=True)
            
            assert 'car_model' in item_dict
            assert item_dict['car_model'] is not None


class TestWishlistModel:
    """Tests for Wishlist model"""

    def test_wishlist_item_to_dict(self, app, sample_wishlist_item):
        """Test Wishlist to_dict conversion"""
        with app.app_context():
            item_dict = sample_wishlist_item.to_dict()
            
            assert 'wishlist_id' in item_dict
            assert 'user_id' in item_dict
            assert 'model_id' in item_dict
            assert 'priority' in item_dict
            assert item_dict['priority'] == 5

