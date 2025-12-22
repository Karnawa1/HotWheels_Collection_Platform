"""
Application constants
Centralized definition of magic strings and configuration values
"""

# User roles
USER_ROLES = {
    'COLLECTOR': 'collector',
    'TRADER': 'trader',
    'ADMIN': 'admin',
    'MODERATOR': 'moderator'
}

# Listing types
LISTING_TYPES = {
    'SALE': 'sale',
    'TRADE': 'trade',
    'AUCTION': 'auction'
}

# Listing statuses
LISTING_STATUSES = {
    'ACTIVE': 'active',
    'SOLD': 'sold',
    'CANCELLED': 'cancelled',
    'EXPIRED': 'expired'
}

# Transaction types
TRANSACTION_TYPES = {
    'PURCHASE': 'purchase',
    'TRADE': 'trade'
}

# Payment statuses
PAYMENT_STATUSES = {
    'PENDING': 'pending',
    'COMPLETED': 'completed',
    'FAILED': 'failed',
    'REFUNDED': 'refunded'
}

# Shipping statuses
SHIPPING_STATUSES = {
    'NOT_SHIPPED': 'not_shipped',
    'SHIPPED': 'shipped',
    'IN_TRANSIT': 'in_transit',
    'DELIVERED': 'delivered'
}

# Condition levels
CONDITION_LEVELS = {
    'MINT': 'Mint',
    'NEAR_MINT': 'Near Mint',
    'EXCELLENT': 'Excellent',
    'GOOD': 'Good',
    'FAIR': 'Fair',
    'POOR': 'Poor'
}

# Rarity levels
RARITY_LEVELS = {
    'COMMON': 'Common',
    'UNCOMMON': 'Uncommon',
    'RARE': 'Rare',
    'CHASE': 'Chase',
    'SUPER_TREASURE_HUNT': 'Super Treasure Hunt'
}

# Image types
IMAGE_TYPES = {
    'PRODUCT': 'product',
    'PACKAGING': 'packaging',
    'DETAIL': 'detail',
    'USER_PHOTO': 'user_photo'
}

# Business rules
MIN_YEAR = 1968  # First Hot Wheels year
CURRENT_YEAR = 2025
MIN_RATING = 1
MAX_RATING = 5
MIN_PRIORITY = 1
MAX_PRIORITY = 5

# Pagination
ITEMS_PER_PAGE = 20
MAX_ITEMS_PER_PAGE = 100

# Password requirements
MIN_PASSWORD_LENGTH = 8
MAX_PASSWORD_LENGTH = 128

# File upload
MAX_FILE_SIZE_MB = 16
ALLOWED_IMAGE_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp'}

# API limits
DEFAULT_SEARCH_LIMIT = 50
MAX_SEARCH_LIMIT = 500

# Cache timeouts (seconds)
CACHE_SHORT = 300      # 5 minutes
CACHE_MEDIUM = 1800    # 30 minutes
CACHE_LONG = 3600      # 1 hour
CACHE_DAY = 86400      # 24 hours

# JWT
JWT_ACCESS_TOKEN_EXPIRES_HOURS = 24
JWT_REFRESH_TOKEN_EXPIRES_DAYS = 30

# Error messages
ERROR_MESSAGES = {
    'INVALID_EMAIL': 'Invalid email format',
    'INVALID_PASSWORD': f'Password must be at least {MIN_PASSWORD_LENGTH} characters',
    'INVALID_YEAR': f'Year must be {MIN_YEAR} or later',
    'INVALID_PRICE': 'Price must be greater than 0',
    'INVALID_RATING': f'Rating must be between {MIN_RATING} and {MAX_RATING}',
    'INVALID_CONDITION': f'Invalid condition level',
    'INVALID_RARITY': f'Invalid rarity level',
    'USER_NOT_FOUND': 'User not found',
    'MODEL_NOT_FOUND': 'Car model not found',
    'LISTING_NOT_FOUND': 'Listing not found',
    'UNAUTHORIZED': 'Authentication required',
    'FORBIDDEN': 'Access forbidden',
    'DUPLICATE_EMAIL': 'Email already registered',
    'DUPLICATE_USERNAME': 'Username already taken',
    'SELF_TRANSACTION': 'Cannot purchase from yourself',
    'LISTING_NOT_ACTIVE': 'Listing is not active',
    'INSUFFICIENT_QUANTITY': 'Insufficient quantity available'
}

# Success messages
SUCCESS_MESSAGES = {
    'USER_CREATED': 'User registered successfully',
    'LOGIN_SUCCESS': 'Login successful',
    'LOGOUT_SUCCESS': 'Logged out successfully',
    'LISTING_CREATED': 'Listing created successfully',
    'TRANSACTION_COMPLETED': 'Transaction completed successfully',
    'COLLECTION_ADDED': 'Added to collection successfully',
    'WISHLIST_ADDED': 'Added to wishlist successfully',
    'REVIEW_SUBMITTED': 'Review submitted successfully'
}