"""
Input validation functions
Validates user input against business rules
"""

import re
from typing import Optional
from app.utils.constants import (
    MIN_PASSWORD_LENGTH,
    MAX_PASSWORD_LENGTH,
    MIN_YEAR,
    MIN_RATING,
    MAX_RATING,
    CONDITION_LEVELS,
    RARITY_LEVELS,
    LISTING_TYPES,
    TRANSACTION_TYPES,
    ERROR_MESSAGES
)


def validate_email(email: str) -> tuple[bool, Optional[str]]:
    """
    Validate email format

    Args:
        email: Email address to validate

    Returns:
        Tuple of (is_valid, error_message)
    """
    if not email:
        return False, "Email is required"

    # RFC 5322 simplified regex
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'

    if not re.match(pattern, email):
        return False, ERROR_MESSAGES['INVALID_EMAIL']

    return True, None


def validate_password(password: str) -> tuple[bool, Optional[str]]:
    """
    Validate password strength

    Args:
        password: Password to validate

    Returns:
        Tuple of (is_valid, error_message)
    """
    if not password:
        return False, "Password is required"

    if len(password) < MIN_PASSWORD_LENGTH:
        return False, ERROR_MESSAGES['INVALID_PASSWORD']

    if len(password) > MAX_PASSWORD_LENGTH:
        return False, f"Password must not exceed {MAX_PASSWORD_LENGTH} characters"

    # Check for at least one number
    if not re.search(r'\d', password):
        return False, "Password must contain at least one number"

    # Check for at least one letter
    if not re.search(r'[a-zA-Z]', password):
        return False, "Password must contain at least one letter"

    return True, None


def validate_price(price: float) -> tuple[bool, Optional[str]]:
    """
    Validate price value

    Args:
        price: Price to validate

    Returns:
        Tuple of (is_valid, error_message)
    """
    if price is None:
        return True, None  # Price can be None for trades

    try:
        price_float = float(price)
        if price_float <= 0:
            return False, ERROR_MESSAGES['INVALID_PRICE']
        return True, None
    except (ValueError, TypeError):
        return False, "Price must be a valid number"


def validate_rating(rating: int) -> tuple[bool, Optional[str]]:
    """
    Validate rating value (1-5)

    Args:
        rating: Rating to validate

    Returns:
        Tuple of (is_valid, error_message)
    """
    try:
        rating_int = int(rating)
        if not (MIN_RATING <= rating_int <= MAX_RATING):
            return False, ERROR_MESSAGES['INVALID_RATING']
        return True, None
    except (ValueError, TypeError):
        return False, "Rating must be a valid integer"


def validate_year(year: int) -> tuple[bool, Optional[str]]:
    """
    Validate release year (must be >= 1968)

    Args:
        year: Year to validate

    Returns:
        Tuple of (is_valid, error_message)
    """
    try:
        year_int = int(year)
        if year_int < MIN_YEAR:
            return False, ERROR_MESSAGES['INVALID_YEAR']
        if year_int > 2030:  # Reasonable future limit
            return False, "Year cannot be more than 5 years in the future"
        return True, None
    except (ValueError, TypeError):
        return False, "Year must be a valid integer"


def validate_condition(condition: str) -> tuple[bool, Optional[str]]:
    """
    Validate condition level

    Args:
        condition: Condition to validate

    Returns:
        Tuple of (is_valid, error_message)
    """
    valid_conditions = list(CONDITION_LEVELS.values())

    if condition not in valid_conditions:
        return False, f"{ERROR_MESSAGES['INVALID_CONDITION']}. Must be one of: {', '.join(valid_conditions)}"

    return True, None


def validate_rarity(rarity: str) -> tuple[bool, Optional[str]]:
    """
    Validate rarity level

    Args:
        rarity: Rarity to validate

    Returns:
        Tuple of (is_valid, error_message)
    """
    valid_rarities = list(RARITY_LEVELS.values())

    if rarity not in valid_rarities:
        return False, f"{ERROR_MESSAGES['INVALID_RARITY']}. Must be one of: {', '.join(valid_rarities)}"

    return True, None


def validate_listing_type(listing_type: str) -> tuple[bool, Optional[str]]:
    """
    Validate listing type

    Args:
        listing_type: Listing type to validate

    Returns:
        Tuple of (is_valid, error_message)
    """
    valid_types = list(LISTING_TYPES.values())

    if listing_type not in valid_types:
        return False, f"Invalid listing type. Must be one of: {', '.join(valid_types)}"

    return True, None


def validate_transaction_type(transaction_type: str) -> tuple[bool, Optional[str]]:
    """
    Validate transaction type

    Args:
        transaction_type: Transaction type to validate

    Returns:
        Tuple of (is_valid, error_message)
    """
    valid_types = list(TRANSACTION_TYPES.values())

    if transaction_type not in valid_types:
        return False, f"Invalid transaction type. Must be one of: {', '.join(valid_types)}"

    return True, None


def validate_username(username: str) -> tuple[bool, Optional[str]]:
    """
    Validate username format

    Args:
        username: Username to validate

    Returns:
        Tuple of (is_valid, error_message)
    """
    if not username:
        return False, "Username is required"

    if len(username) < 3:
        return False, "Username must be at least 3 characters"

    if len(username) > 50:
        return False, "Username must not exceed 50 characters"

    # Alphanumeric, underscore, hyphen only
    if not re.match(r'^[a-zA-Z0-9_-]+$', username):
        return False, "Username can only contain letters, numbers, underscores, and hyphens"

    return True, None


def validate_quantity(quantity: int) -> tuple[bool, Optional[str]]:
    """
    Validate quantity value

    Args:
        quantity: Quantity to validate

    Returns:
        Tuple of (is_valid, error_message)
    """
    try:
        qty = int(quantity)
        if qty <= 0:
            return False, "Quantity must be greater than 0"
        if qty > 1000:
            return False, "Quantity seems unreasonably high"
        return True, None
    except (ValueError, TypeError):
        return False, "Quantity must be a valid integer"


def validate_priority(priority: int) -> tuple[bool, Optional[str]]:
    """
    Validate priority value (1-5)

    Args:
        priority: Priority to validate

    Returns:
        Tuple of (is_valid, error_message)
    """
    try:
        pri = int(priority)
        if not (1 <= pri <= 5):
            return False, "Priority must be between 1 and 5"
        return True, None
    except (ValueError, TypeError):
        return False, "Priority must be a valid integer"