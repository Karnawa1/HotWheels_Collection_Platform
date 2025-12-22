"""
Test Configuration and Fixtures
Provides test database, client, and mock data for unit tests
"""

import pytest
import os
from datetime import datetime, date
from decimal import Decimal

# Set testing environment before importing app
os.environ['FLASK_ENV'] = 'testing'
os.environ['SECRET_KEY'] = 'test-secret-key-for-testing'
os.environ['JWT_SECRET_KEY'] = 'test-jwt-secret-key-for-testing'
os.environ['DATABASE_URL'] = 'sqlite:///:memory:'  # Use in-memory SQLite for tests

from app import create_app, db
from app.models.user import User, UserCollection, Wishlist
from app.models.car_model import CarModel
from app.models.casting import Casting
from app.models.series import Series
from app.models.manufacturer import Manufacturer
from app.models.listing import Listing
from app.models.transaction import Transaction, Review


@pytest.fixture(scope='function')
def app():
    """Create and configure a test application instance"""
    application = create_app('testing')
    application.config.update({
        'TESTING': True,
        'SQLALCHEMY_DATABASE_URI': 'sqlite:///:memory:',
        'WTF_CSRF_ENABLED': False,
        'JWT_SECRET_KEY': 'test-jwt-secret',
        'SECRET_KEY': 'test-secret',
    })
    
    # Create application context
    with application.app_context():
        # Create all tables
        db.create_all()
        yield application
        # Clean up
        db.session.remove()
        db.drop_all()


@pytest.fixture(scope='function')
def client(app):
    """Create a test client for the application"""
    return app.test_client()


@pytest.fixture(scope='function')
def runner(app):
    """Create a test CLI runner"""
    return app.test_cli_runner()


@pytest.fixture(scope='function')
def db_session(app):
    """Create a database session for tests"""
    with app.app_context():
        yield db.session


# ==================== User Fixtures ====================

@pytest.fixture
def sample_user(app):
    """Create a sample user for testing"""
    with app.app_context():
        user = User(
            username='testuser',
            email='test@example.com',
            fullname='Test User',
            country='USA',
            city='Los Angeles',
            role='collector',
            isactive=True,
            isverified=False
        )
        user.set_password('TestPass123')
        db.session.add(user)
        db.session.commit()
        
        # Refresh to get the ID
        db.session.refresh(user)
        yield user


@pytest.fixture
def sample_user_2(app):
    """Create a second sample user for testing"""
    with app.app_context():
        user = User(
            username='testuser2',
            email='test2@example.com',
            fullname='Test User 2',
            country='Canada',
            city='Toronto',
            role='trader',
            isactive=True,
            isverified=True
        )
        user.set_password('TestPass456')
        db.session.add(user)
        db.session.commit()
        
        db.session.refresh(user)
        yield user


@pytest.fixture
def inactive_user(app):
    """Create an inactive user for testing"""
    with app.app_context():
        user = User(
            username='inactiveuser',
            email='inactive@example.com',
            isactive=False
        )
        user.set_password('TestPass789')
        db.session.add(user)
        db.session.commit()
        
        db.session.refresh(user)
        yield user


# ==================== Catalog Fixtures ====================

@pytest.fixture
def sample_manufacturer(app):
    """Create a sample manufacturer"""
    with app.app_context():
        manufacturer = Manufacturer(
            name='Mattel',
            country='USA',
            foundedyear=1945
        )
        db.session.add(manufacturer)
        db.session.commit()
        
        db.session.refresh(manufacturer)
        yield manufacturer


@pytest.fixture
def sample_casting(app, sample_manufacturer):
    """Create a sample casting"""
    with app.app_context():
        casting = Casting(
            castingname="'67 Camaro",
            firstreleaseyear=1968,
            manufacturerid=sample_manufacturer.manufacturerid,
            scale='1:64',
            designer='Harry Bradley',
            basedonrealcar=True,
            realcarmodel='1967 Chevrolet Camaro'
        )
        db.session.add(casting)
        db.session.commit()
        
        db.session.refresh(casting)
        yield casting


@pytest.fixture
def sample_series(app, sample_manufacturer):
    """Create a sample series"""
    with app.app_context():
        series = Series(
            seriesname='Mainline 2024',
            releaseyear=2024,
            manufacturerid=sample_manufacturer.manufacturerid,
            description='Standard mainline series',
            islimitededition=False
        )
        db.session.add(series)
        db.session.commit()
        
        db.session.refresh(series)
        yield series


@pytest.fixture
def sample_car_model(app, sample_casting, sample_series):
    """Create a sample car model"""
    with app.app_context():
        car_model = CarModel(
            castingid=sample_casting.castingid,
            seriesid=sample_series.seriesid,
            releaseyear=2024,
            color='Spectraflame Red',
            tampodesign='Racing stripes',
            wheeltype='5-Spoke',
            basecolor='Chrome',
            windowcolor='Tinted',
            interiorcolor='Black',
            productioncode='L2593',
            sku='HW-2024-TEST001',
            raritylevel='Common',
            estimatedproductionquantity=50000,
            msrp=Decimal('1.29')
        )
        db.session.add(car_model)
        db.session.commit()
        
        db.session.refresh(car_model)
        yield car_model


@pytest.fixture
def rare_car_model(app, sample_casting, sample_series):
    """Create a rare car model"""
    with app.app_context():
        car_model = CarModel(
            castingid=sample_casting.castingid,
            seriesid=sample_series.seriesid,
            releaseyear=2024,
            color='Spectraflame Blue',
            tampodesign='TH Logo',
            wheeltype='Real Riders',
            basecolor='Chrome',
            raritylevel='Super Treasure Hunt',
            estimatedproductionquantity=5000,
            msrp=Decimal('1.29'),
            sku='HW-2024-STH001'
        )
        db.session.add(car_model)
        db.session.commit()
        
        db.session.refresh(car_model)
        yield car_model


# ==================== Collection Fixtures ====================

@pytest.fixture
def sample_collection_item(app, sample_user, sample_car_model):
    """Create a sample collection item"""
    with app.app_context():
        collection_item = UserCollection(
            userid=sample_user.userid,
            modelid=sample_car_model.modelid,
            acquisitiondate=date.today(),
            acquisitionprice=Decimal('4.99'),
            condition='Mint',
            isinpackage=True,
            packagecondition='Mint',
            quantity=1,
            storagelocation='Display Case A',
            notes='Found at local Walmart',
            isfortrade=False,
            isforsale=False
        )
        db.session.add(collection_item)
        db.session.commit()
        
        db.session.refresh(collection_item)
        yield collection_item


@pytest.fixture
def sample_wishlist_item(app, sample_user, sample_car_model):
    """Create a sample wishlist item"""
    with app.app_context():
        wishlist_item = Wishlist(
            userid=sample_user.userid,
            modelid=sample_car_model.modelid,
            priority=5,
            maxpricewilling=Decimal('25.00'),
            notes='Looking for mint condition'
        )
        db.session.add(wishlist_item)
        db.session.commit()
        
        db.session.refresh(wishlist_item)
        yield wishlist_item


# ==================== Marketplace Fixtures ====================

@pytest.fixture
def sample_listing(app, sample_user, sample_car_model):
    """Create a sample listing"""
    with app.app_context():
        listing = Listing(
            sellerid=sample_user.userid,
            modelid=sample_car_model.modelid,
            listingtype='sale',
            price=Decimal('15.99'),
            condition='Mint',
            description='Pristine condition, never opened',
            status='active',
            viewscount=0
        )
        db.session.add(listing)
        db.session.commit()
        
        db.session.refresh(listing)
        yield listing


@pytest.fixture
def sample_trade_listing(app, sample_user_2, sample_car_model):
    """Create a sample trade listing"""
    with app.app_context():
        listing = Listing(
            sellerid=sample_user_2.userid,
            modelid=sample_car_model.modelid,
            listingtype='trade',
            price=None,
            condition='Near Mint',
            description='Looking to trade for Chase variants',
            status='active',
            viewscount=5
        )
        db.session.add(listing)
        db.session.commit()
        
        db.session.refresh(listing)
        yield listing


@pytest.fixture
def sample_transaction(app, sample_listing, sample_user_2):
    """Create a sample transaction"""
    with app.app_context():
        transaction = Transaction(
            listingid=sample_listing.listingid,
            buyerid=sample_user_2.userid,
            sellerid=sample_listing.sellerid,
            transactiontype='purchase',
            amount=sample_listing.price,
            paymentmethod='PayPal',
            paymentstatus='completed',
            shippingstatus='delivered'
        )
        db.session.add(transaction)
        db.session.commit()
        
        db.session.refresh(transaction)
        yield transaction


# ==================== Auth Fixtures ====================

@pytest.fixture
def auth_headers(app, sample_user):
    """Create authorization headers for authenticated requests"""
    from flask_jwt_extended import create_access_token
    
    with app.app_context():
        access_token = create_access_token(identity=str(sample_user.userid))
        return {'Authorization': f'Bearer {access_token}'}


@pytest.fixture
def auth_headers_user2(app, sample_user_2):
    """Create authorization headers for second user"""
    from flask_jwt_extended import create_access_token
    
    with app.app_context():
        access_token = create_access_token(identity=str(sample_user_2.userid))
        return {'Authorization': f'Bearer {access_token}'}


# ==================== Helper Fixtures ====================

@pytest.fixture
def mock_request_context(app):
    """Create a mock request context"""
    with app.test_request_context():
        yield


# ==================== Data Generation Helpers ====================

def create_multiple_car_models(app, casting, series, count=10):
    """Helper to create multiple car models for pagination tests"""
    with app.app_context():
        models = []
        colors = ['Red', 'Blue', 'Green', 'Yellow', 'Black', 'White', 'Orange', 'Purple', 'Silver', 'Gold']
        rarities = ['Common', 'Common', 'Common', 'Uncommon', 'Uncommon', 'Rare', 'Rare', 'Rare', 'Chase', 'Super Treasure Hunt']
        
        for i in range(count):
            model = CarModel(
                castingid=casting.castingid,
                seriesid=series.seriesid,
                releaseyear=2024 - (i % 5),
                color=colors[i % len(colors)],
                raritylevel=rarities[i % len(rarities)],
                sku=f'HW-TEST-{i:04d}'
            )
            db.session.add(model)
            models.append(model)
        
        db.session.commit()
        return models

