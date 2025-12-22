"""
Unit Tests for Marketplace Service
Tests listings, transactions, and reviews
"""

import pytest
from decimal import Decimal
from app.services.marketplace_service import MarketplaceService
from app.models.listing import Listing
from app.models.transaction import Transaction


class TestMarketplaceServiceCreateListing:
    """Tests for creating listings"""

    def test_create_sale_listing_success(self, app, sample_user, sample_car_model):
        """Test successfully creating a sale listing"""
        with app.app_context():
            listing, error = MarketplaceService.create_listing(
                seller_id=sample_user.userid,
                model_id=sample_car_model.modelid,
                listing_type='sale',
                condition='Mint',
                price=15.99,
                description='Test listing'
            )
            
            assert listing is not None
            assert error is None
            assert listing.listingtype == 'sale'
            assert float(listing.price) == 15.99
            assert listing.status == 'active'

    def test_create_trade_listing_success(self, app, sample_user, sample_car_model):
        """Test successfully creating a trade listing"""
        with app.app_context():
            listing, error = MarketplaceService.create_listing(
                seller_id=sample_user.userid,
                model_id=sample_car_model.modelid,
                listing_type='trade',
                condition='Near Mint',
                description='Looking to trade'
            )
            
            assert listing is not None
            assert error is None
            assert listing.listingtype == 'trade'
            assert listing.price is None

    def test_create_sale_listing_without_price(self, app, sample_user, sample_car_model):
        """Test creating sale listing without price fails"""
        with app.app_context():
            listing, error = MarketplaceService.create_listing(
                seller_id=sample_user.userid,
                model_id=sample_car_model.modelid,
                listing_type='sale',
                condition='Mint'
                # No price
            )
            
            assert listing is None
            assert error is not None
            assert 'price' in error.lower()

    def test_create_listing_invalid_type(self, app, sample_user, sample_car_model):
        """Test creating listing with invalid type"""
        with app.app_context():
            listing, error = MarketplaceService.create_listing(
                seller_id=sample_user.userid,
                model_id=sample_car_model.modelid,
                listing_type='rent',  # Invalid
                condition='Mint',
                price=10.00
            )
            
            assert listing is None
            assert error is not None

    def test_create_listing_invalid_condition(self, app, sample_user, sample_car_model):
        """Test creating listing with invalid condition"""
        with app.app_context():
            listing, error = MarketplaceService.create_listing(
                seller_id=sample_user.userid,
                model_id=sample_car_model.modelid,
                listing_type='sale',
                condition='Perfect',  # Invalid
                price=10.00
            )
            
            assert listing is None
            assert error is not None

    def test_create_listing_user_not_found(self, app, sample_car_model):
        """Test creating listing with non-existent seller"""
        with app.app_context():
            listing, error = MarketplaceService.create_listing(
                seller_id=99999,
                model_id=sample_car_model.modelid,
                listing_type='sale',
                condition='Mint',
                price=10.00
            )
            
            assert listing is None
            assert error is not None

    def test_create_listing_model_not_found(self, app, sample_user):
        """Test creating listing with non-existent model"""
        with app.app_context():
            listing, error = MarketplaceService.create_listing(
                seller_id=sample_user.userid,
                model_id=99999,
                listing_type='sale',
                condition='Mint',
                price=10.00
            )
            
            assert listing is None
            assert error is not None

    def test_create_listing_invalid_price(self, app, sample_user, sample_car_model):
        """Test creating listing with invalid price"""
        with app.app_context():
            listing, error = MarketplaceService.create_listing(
                seller_id=sample_user.userid,
                model_id=sample_car_model.modelid,
                listing_type='sale',
                condition='Mint',
                price=-5.00  # Invalid
            )
            
            assert listing is None
            assert error is not None


class TestMarketplaceServiceGetListings:
    """Tests for getting listings"""

    def test_get_active_listings(self, app, sample_listing):
        """Test getting active listings"""
        with app.app_context():
            result = MarketplaceService.get_active_listings()
            
            assert 'items' in result
            assert 'pagination' in result
            assert len(result['items']) >= 1

    def test_get_listings_filter_by_type(self, app, sample_listing, sample_trade_listing):
        """Test filtering listings by type"""
        with app.app_context():
            result = MarketplaceService.get_active_listings(
                listing_type='sale'
            )
            
            for item in result['items']:
                assert item['listing_type'] == 'sale'

    def test_get_listings_filter_by_price_range(self, app, sample_listing):
        """Test filtering listings by price range"""
        with app.app_context():
            result = MarketplaceService.get_active_listings(
                price_min=10.00,
                price_max=20.00
            )
            
            for item in result['items']:
                if item['price'] is not None:
                    assert 10.00 <= item['price'] <= 20.00

    def test_get_listings_filter_by_seller(self, app, sample_user, sample_listing):
        """Test filtering listings by seller"""
        with app.app_context():
            result = MarketplaceService.get_active_listings(
                seller_id=sample_user.userid
            )
            
            for item in result['items']:
                assert item['seller_id'] == sample_user.userid

    def test_get_listing_by_id(self, app, sample_listing):
        """Test getting single listing by ID"""
        with app.app_context():
            listing = MarketplaceService.get_listing(sample_listing.listingid)
            
            assert listing is not None
            assert listing.listingid == sample_listing.listingid

    def test_get_listing_increments_views(self, app, sample_listing):
        """Test that getting listing increments view count"""
        with app.app_context():
            initial_views = sample_listing.viewscount
            
            listing = MarketplaceService.get_listing(
                sample_listing.listingid,
                increment_views=True
            )
            
            assert listing.viewscount == initial_views + 1

    def test_get_listing_not_found(self, app):
        """Test getting non-existent listing"""
        with app.app_context():
            listing = MarketplaceService.get_listing(99999)
            assert listing is None


class TestMarketplaceServiceUpdateListing:
    """Tests for updating listings"""

    def test_update_listing_success(self, app, sample_user, sample_listing):
        """Test successfully updating listing"""
        with app.app_context():
            listing, error = MarketplaceService.update_listing(
                listing_id=sample_listing.listingid,
                seller_id=sample_user.userid,
                price=19.99,
                description='Updated description'
            )
            
            assert listing is not None
            assert error is None
            assert float(listing.price) == 19.99
            assert listing.description == 'Updated description'

    def test_update_listing_not_found(self, app, sample_user):
        """Test updating non-existent listing"""
        with app.app_context():
            listing, error = MarketplaceService.update_listing(
                listing_id=99999,
                seller_id=sample_user.userid,
                price=19.99
            )
            
            assert listing is None
            assert error is not None

    def test_update_listing_wrong_seller(self, app, sample_user_2, sample_listing):
        """Test updating listing by non-owner"""
        with app.app_context():
            listing, error = MarketplaceService.update_listing(
                listing_id=sample_listing.listingid,
                seller_id=sample_user_2.userid,  # Different user
                price=19.99
            )
            
            assert listing is None
            assert error is not None

    def test_update_listing_invalid_price(self, app, sample_user, sample_listing):
        """Test updating listing with invalid price"""
        with app.app_context():
            listing, error = MarketplaceService.update_listing(
                listing_id=sample_listing.listingid,
                seller_id=sample_user.userid,
                price=-10.00
            )
            
            assert listing is None
            assert error is not None


class TestMarketplaceServiceCancelListing:
    """Tests for cancelling listings"""

    def test_cancel_listing_success(self, app, sample_user, sample_listing):
        """Test successfully cancelling listing"""
        with app.app_context():
            success, error = MarketplaceService.cancel_listing(
                listing_id=sample_listing.listingid,
                seller_id=sample_user.userid
            )
            
            assert success is True
            assert error is None
            
            # Verify status changed
            listing = Listing.query.filter_by(listingid=sample_listing.listingid).first()
            assert listing.status == 'cancelled'

    def test_cancel_listing_not_found(self, app, sample_user):
        """Test cancelling non-existent listing"""
        with app.app_context():
            success, error = MarketplaceService.cancel_listing(
                listing_id=99999,
                seller_id=sample_user.userid
            )
            
            assert success is False
            assert error is not None

    def test_cancel_listing_wrong_seller(self, app, sample_user_2, sample_listing):
        """Test cancelling listing by non-owner"""
        with app.app_context():
            success, error = MarketplaceService.cancel_listing(
                listing_id=sample_listing.listingid,
                seller_id=sample_user_2.userid
            )
            
            assert success is False
            assert error is not None


class TestMarketplaceServiceCreateTransaction:
    """Tests for creating transactions"""

    def test_create_transaction_success(self, app, sample_user_2, sample_listing):
        """Test successfully creating transaction"""
        with app.app_context():
            transaction, error = MarketplaceService.create_transaction(
                listing_id=sample_listing.listingid,
                buyer_id=sample_user_2.userid,
                paymentmethod='PayPal'
            )
            
            assert transaction is not None
            assert error is None
            assert transaction.buyerid == sample_user_2.userid
            assert transaction.transactiontype == 'purchase'

    def test_create_transaction_listing_not_found(self, app, sample_user_2):
        """Test creating transaction for non-existent listing"""
        with app.app_context():
            transaction, error = MarketplaceService.create_transaction(
                listing_id=99999,
                buyer_id=sample_user_2.userid
            )
            
            assert transaction is None
            assert error is not None

    def test_create_transaction_self_purchase(self, app, sample_user, sample_listing):
        """Test buyer cannot be the seller"""
        with app.app_context():
            transaction, error = MarketplaceService.create_transaction(
                listing_id=sample_listing.listingid,
                buyer_id=sample_user.userid  # Same as seller
            )
            
            assert transaction is None
            assert error is not None
            assert 'yourself' in error.lower()

    def test_create_transaction_buyer_not_found(self, app, sample_listing):
        """Test creating transaction with non-existent buyer"""
        with app.app_context():
            transaction, error = MarketplaceService.create_transaction(
                listing_id=sample_listing.listingid,
                buyer_id=99999
            )
            
            assert transaction is None
            assert error is not None


class TestMarketplaceServiceGetTransactions:
    """Tests for getting transactions"""

    def test_get_user_purchases(self, app, sample_user_2, sample_transaction):
        """Test getting user's purchases"""
        with app.app_context():
            result = MarketplaceService.get_user_transactions(
                user_id=sample_user_2.userid,
                as_buyer=True
            )
            
            assert 'items' in result
            assert 'pagination' in result

    def test_get_user_sales(self, app, sample_user, sample_transaction):
        """Test getting user's sales"""
        with app.app_context():
            result = MarketplaceService.get_user_transactions(
                user_id=sample_user.userid,
                as_buyer=False
            )
            
            assert 'items' in result
            assert 'pagination' in result


class TestMarketplaceServiceReviews:
    """Tests for review operations"""

    def test_create_review_success(self, app, sample_user_2, sample_user, sample_transaction):
        """Test successfully creating a review"""
        with app.app_context():
            review, error = MarketplaceService.create_review(
                transaction_id=sample_transaction.transactionid,
                reviewer_id=sample_user_2.userid,  # Buyer
                reviewee_id=sample_user.userid,  # Seller
                rating=5,
                comment='Great seller!'
            )
            
            assert review is not None
            assert error is None
            assert review.rating == 5

    def test_create_review_invalid_rating(self, app, sample_user_2, sample_user, sample_transaction):
        """Test creating review with invalid rating"""
        with app.app_context():
            review, error = MarketplaceService.create_review(
                transaction_id=sample_transaction.transactionid,
                reviewer_id=sample_user_2.userid,
                reviewee_id=sample_user.userid,
                rating=10  # Invalid
            )
            
            assert review is None
            assert error is not None

    def test_create_review_transaction_not_found(self, app, sample_user, sample_user_2):
        """Test creating review for non-existent transaction"""
        with app.app_context():
            review, error = MarketplaceService.create_review(
                transaction_id=99999,
                reviewer_id=sample_user.userid,
                reviewee_id=sample_user_2.userid,
                rating=5
            )
            
            assert review is None
            assert error is not None

    def test_create_review_duplicate(self, app, sample_user_2, sample_user, sample_transaction):
        """Test creating duplicate review"""
        with app.app_context():
            # Create first review
            MarketplaceService.create_review(
                transaction_id=sample_transaction.transactionid,
                reviewer_id=sample_user_2.userid,
                reviewee_id=sample_user.userid,
                rating=5
            )
            
            # Try to create duplicate
            review, error = MarketplaceService.create_review(
                transaction_id=sample_transaction.transactionid,
                reviewer_id=sample_user_2.userid,
                reviewee_id=sample_user.userid,
                rating=4
            )
            
            assert review is None
            assert error is not None
            assert 'already' in error.lower()


class TestListingModel:
    """Tests for Listing model"""

    def test_listing_to_dict(self, app, sample_listing):
        """Test Listing to_dict conversion"""
        with app.app_context():
            listing_dict = sample_listing.to_dict()
            
            assert 'listing_id' in listing_dict
            assert 'seller_id' in listing_dict
            assert 'listing_type' in listing_dict
            assert 'price' in listing_dict
            assert 'status' in listing_dict

    def test_listing_to_dict_with_relations(self, app, sample_listing):
        """Test Listing to_dict with relations"""
        with app.app_context():
            listing_dict = sample_listing.to_dict(include_relations=True)
            
            assert 'seller' in listing_dict
            assert 'car_model' in listing_dict

    def test_listing_increment_views(self, app, sample_listing):
        """Test incrementing views"""
        with app.app_context():
            initial_views = sample_listing.viewscount
            sample_listing.increment_views()
            
            assert sample_listing.viewscount == initial_views + 1

    def test_listing_mark_as_sold(self, app, sample_listing):
        """Test marking listing as sold"""
        with app.app_context():
            sample_listing.mark_as_sold()
            
            assert sample_listing.status == 'sold'
            assert sample_listing.soldat is not None


class TestTransactionModel:
    """Tests for Transaction model"""

    def test_transaction_to_dict(self, app, sample_transaction):
        """Test Transaction to_dict conversion"""
        with app.app_context():
            trans_dict = sample_transaction.to_dict()
            
            assert 'transaction_id' in trans_dict
            assert 'buyer_id' in trans_dict
            assert 'seller_id' in trans_dict
            assert 'amount' in trans_dict
            assert 'payment_status' in trans_dict

