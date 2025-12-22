"""
Unit Tests for Validators Module
Tests input validation functions
"""

import pytest
from app.utils.validators import (
    validate_email,
    validate_password,
    validate_price,
    validate_rating,
    validate_year,
    validate_condition,
    validate_rarity,
    validate_listing_type,
    validate_transaction_type,
    validate_username,
    validate_quantity,
    validate_priority
)


class TestValidateEmail:
    """Tests for email validation"""

    def test_valid_email(self):
        """Test valid email addresses"""
        valid_emails = [
            'user@example.com',
            'user.name@example.com',
            'user+tag@example.com',
            'user123@subdomain.example.com',
            'test@test.co.uk',
        ]
        for email in valid_emails:
            is_valid, error = validate_email(email)
            assert is_valid is True, f"Email {email} should be valid"
            assert error is None

    def test_invalid_email_format(self):
        """Test invalid email formats"""
        invalid_emails = [
            'invalid',
            'invalid@',
            '@example.com',
            'user@.com',
            'user@example',
            'user space@example.com',
        ]
        for email in invalid_emails:
            is_valid, error = validate_email(email)
            assert is_valid is False, f"Email {email} should be invalid"
            assert error is not None

    def test_empty_email(self):
        """Test empty email"""
        is_valid, error = validate_email('')
        assert is_valid is False
        assert 'required' in error.lower()

    def test_none_email(self):
        """Test None email"""
        is_valid, error = validate_email(None)
        assert is_valid is False


class TestValidatePassword:
    """Tests for password validation"""

    def test_valid_password(self):
        """Test valid passwords"""
        valid_passwords = [
            'Password1',
            'SecurePass123',
            'MyP4ssw0rd!',
            'Test1234',
        ]
        for password in valid_passwords:
            is_valid, error = validate_password(password)
            assert is_valid is True, f"Password should be valid: {error}"
            assert error is None

    def test_password_too_short(self):
        """Test password that's too short"""
        is_valid, error = validate_password('Pass1')
        assert is_valid is False
        assert 'at least' in error.lower() or 'character' in error.lower()

    def test_password_no_number(self):
        """Test password without numbers"""
        is_valid, error = validate_password('PasswordOnly')
        assert is_valid is False
        assert 'number' in error.lower()

    def test_password_no_letter(self):
        """Test password without letters"""
        is_valid, error = validate_password('12345678')
        assert is_valid is False
        assert 'letter' in error.lower()

    def test_empty_password(self):
        """Test empty password"""
        is_valid, error = validate_password('')
        assert is_valid is False
        assert 'required' in error.lower()

    def test_password_too_long(self):
        """Test password that exceeds max length"""
        long_password = 'A' * 130 + '1'
        is_valid, error = validate_password(long_password)
        assert is_valid is False
        assert 'exceed' in error.lower()


class TestValidatePrice:
    """Tests for price validation"""

    def test_valid_price(self):
        """Test valid prices"""
        valid_prices = [0.01, 1.0, 10.99, 100.00, 9999.99]
        for price in valid_prices:
            is_valid, error = validate_price(price)
            assert is_valid is True
            assert error is None

    def test_zero_price(self):
        """Test zero price (invalid)"""
        is_valid, error = validate_price(0)
        assert is_valid is False
        assert 'greater than 0' in error.lower()

    def test_negative_price(self):
        """Test negative price"""
        is_valid, error = validate_price(-5.00)
        assert is_valid is False

    def test_none_price(self):
        """Test None price (allowed for trades)"""
        is_valid, error = validate_price(None)
        assert is_valid is True
        assert error is None

    def test_invalid_price_type(self):
        """Test invalid price type"""
        is_valid, error = validate_price('not_a_number')
        assert is_valid is False
        assert 'valid number' in error.lower()


class TestValidateRating:
    """Tests for rating validation"""

    def test_valid_ratings(self):
        """Test valid rating values (1-5)"""
        for rating in range(1, 6):
            is_valid, error = validate_rating(rating)
            assert is_valid is True
            assert error is None

    def test_rating_zero(self):
        """Test zero rating (invalid)"""
        is_valid, error = validate_rating(0)
        assert is_valid is False

    def test_rating_too_high(self):
        """Test rating above 5"""
        is_valid, error = validate_rating(6)
        assert is_valid is False

    def test_rating_negative(self):
        """Test negative rating"""
        is_valid, error = validate_rating(-1)
        assert is_valid is False

    def test_rating_invalid_type(self):
        """Test invalid rating type"""
        is_valid, error = validate_rating('five')
        assert is_valid is False


class TestValidateYear:
    """Tests for year validation"""

    def test_valid_years(self):
        """Test valid years (1968 onwards)"""
        valid_years = [1968, 1985, 2000, 2020, 2024, 2025]
        for year in valid_years:
            is_valid, error = validate_year(year)
            assert is_valid is True, f"Year {year} should be valid"
            assert error is None

    def test_year_before_1968(self):
        """Test year before Hot Wheels existed"""
        is_valid, error = validate_year(1967)
        assert is_valid is False
        assert '1968' in error

    def test_year_too_far_future(self):
        """Test year too far in the future"""
        is_valid, error = validate_year(2050)
        assert is_valid is False

    def test_invalid_year_type(self):
        """Test invalid year type"""
        is_valid, error = validate_year('twenty-twenty')
        assert is_valid is False


class TestValidateCondition:
    """Tests for condition validation"""

    def test_valid_conditions(self):
        """Test all valid condition values"""
        valid_conditions = ['Mint', 'Near Mint', 'Excellent', 'Good', 'Fair', 'Poor']
        for condition in valid_conditions:
            is_valid, error = validate_condition(condition)
            assert is_valid is True, f"Condition {condition} should be valid"
            assert error is None

    def test_invalid_condition(self):
        """Test invalid condition value"""
        is_valid, error = validate_condition('Perfect')
        assert is_valid is False
        assert 'Invalid condition' in error

    def test_condition_case_sensitive(self):
        """Test that condition validation is case-sensitive"""
        is_valid, error = validate_condition('mint')  # lowercase
        assert is_valid is False


class TestValidateRarity:
    """Tests for rarity validation"""

    def test_valid_rarities(self):
        """Test all valid rarity values"""
        valid_rarities = ['Common', 'Uncommon', 'Rare', 'Chase', 'Super Treasure Hunt']
        for rarity in valid_rarities:
            is_valid, error = validate_rarity(rarity)
            assert is_valid is True, f"Rarity {rarity} should be valid"
            assert error is None

    def test_invalid_rarity(self):
        """Test invalid rarity value"""
        is_valid, error = validate_rarity('Ultra Rare')
        assert is_valid is False


class TestValidateListingType:
    """Tests for listing type validation"""

    def test_valid_listing_types(self):
        """Test all valid listing types"""
        valid_types = ['sale', 'trade', 'auction']
        for listing_type in valid_types:
            is_valid, error = validate_listing_type(listing_type)
            assert is_valid is True
            assert error is None

    def test_invalid_listing_type(self):
        """Test invalid listing type"""
        is_valid, error = validate_listing_type('rent')
        assert is_valid is False


class TestValidateTransactionType:
    """Tests for transaction type validation"""

    def test_valid_transaction_types(self):
        """Test all valid transaction types"""
        valid_types = ['purchase', 'trade']
        for trans_type in valid_types:
            is_valid, error = validate_transaction_type(trans_type)
            assert is_valid is True
            assert error is None

    def test_invalid_transaction_type(self):
        """Test invalid transaction type"""
        is_valid, error = validate_transaction_type('gift')
        assert is_valid is False


class TestValidateUsername:
    """Tests for username validation"""

    def test_valid_usernames(self):
        """Test valid usernames"""
        valid_usernames = [
            'user',
            'user123',
            'user_name',
            'user-name',
            'User_Name_123',
        ]
        for username in valid_usernames:
            is_valid, error = validate_username(username)
            assert is_valid is True, f"Username {username} should be valid: {error}"
            assert error is None

    def test_username_too_short(self):
        """Test username that's too short"""
        is_valid, error = validate_username('ab')
        assert is_valid is False
        assert 'at least 3' in error.lower()

    def test_username_too_long(self):
        """Test username that exceeds max length"""
        long_username = 'a' * 51
        is_valid, error = validate_username(long_username)
        assert is_valid is False
        assert 'exceed' in error.lower()

    def test_username_invalid_chars(self):
        """Test username with invalid characters"""
        is_valid, error = validate_username('user@name')
        assert is_valid is False
        assert 'only contain' in error.lower()

    def test_empty_username(self):
        """Test empty username"""
        is_valid, error = validate_username('')
        assert is_valid is False
        assert 'required' in error.lower()


class TestValidateQuantity:
    """Tests for quantity validation"""

    def test_valid_quantities(self):
        """Test valid quantity values"""
        valid_quantities = [1, 5, 10, 100, 500]
        for qty in valid_quantities:
            is_valid, error = validate_quantity(qty)
            assert is_valid is True
            assert error is None

    def test_quantity_zero(self):
        """Test zero quantity (invalid)"""
        is_valid, error = validate_quantity(0)
        assert is_valid is False
        assert 'greater than 0' in error.lower()

    def test_quantity_negative(self):
        """Test negative quantity"""
        is_valid, error = validate_quantity(-1)
        assert is_valid is False

    def test_quantity_too_high(self):
        """Test unreasonably high quantity"""
        is_valid, error = validate_quantity(10000)
        assert is_valid is False
        assert 'unreasonably high' in error.lower()


class TestValidatePriority:
    """Tests for priority validation"""

    def test_valid_priorities(self):
        """Test valid priority values (1-5)"""
        for priority in range(1, 6):
            is_valid, error = validate_priority(priority)
            assert is_valid is True
            assert error is None

    def test_priority_zero(self):
        """Test zero priority (invalid)"""
        is_valid, error = validate_priority(0)
        assert is_valid is False
        assert 'between 1 and 5' in error.lower()

    def test_priority_too_high(self):
        """Test priority above 5"""
        is_valid, error = validate_priority(6)
        assert is_valid is False

    def test_priority_invalid_type(self):
        """Test invalid priority type"""
        is_valid, error = validate_priority('high')
        assert is_valid is False

