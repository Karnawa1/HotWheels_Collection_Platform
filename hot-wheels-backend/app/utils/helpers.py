"""
Helper utility functions
General purpose helper functions for the application
"""

from typing import Optional, Dict, Any, List
from datetime import datetime
from flask import request, jsonify
from flask_jwt_extended import get_jwt_identity
from sqlalchemy.orm import Query
from app.utils.constants import ITEMS_PER_PAGE, MAX_ITEMS_PER_PAGE
import hashlib
import secrets


def paginate_query(query: Query, page: int = 1, per_page: int = ITEMS_PER_PAGE) -> Dict[str, Any]:
    """
    Paginate a SQLAlchemy query

    Args:
        query: SQLAlchemy query object
        page: Page number (1-indexed)
        per_page: Items per page

    Returns:
        Dictionary with paginated data and metadata
    """
    # Validate inputs
    page = max(1, page)
    per_page = min(per_page, MAX_ITEMS_PER_PAGE)

    # Execute pagination
    paginated = query.paginate(
        page=page,
        per_page=per_page,
        error_out=False
    )

    return {
        'items': [item.to_dict() if hasattr(item, 'to_dict') else item for item in paginated.items],
        'pagination': {
            'page': page,
            'per_page': per_page,
            'total_items': paginated.total,
            'total_pages': paginated.pages,
            'has_next': paginated.has_next,
            'has_prev': paginated.has_prev,
            'next_page': paginated.next_num if paginated.has_next else None,
            'prev_page': paginated.prev_num if paginated.has_prev else None
        }
    }


def calculate_offset(page: int, per_page: int) -> int:
    """
    Calculate database offset from page number

    Args:
        page: Page number (1-indexed)
        per_page: Items per page

    Returns:
        Offset value for database query
    """
    return (max(1, page) - 1) * per_page


def format_error_response(message: str, status_code: int = 400, errors: Optional[Dict] = None) -> tuple:
    """
    Format error response consistently

    Args:
        message: Error message
        status_code: HTTP status code
        errors: Additional error details

    Returns:
        Tuple of (response_dict, status_code)
    """
    response = {
        'success': False,
        'error': message,
        'timestamp': datetime.utcnow().isoformat()
    }

    if errors:
        response['details'] = errors

    return response, status_code


def format_success_response(data: Any = None, message: str = None, status_code: int = 200) -> tuple:
    """
    Format success response consistently

    Args:
        data: Response data
        message: Success message
        status_code: HTTP status code

    Returns:
        Tuple of (response_dict, status_code)
    """
    response = {
        'success': True,
        'timestamp': datetime.utcnow().isoformat()
    }

    if message:
        response['message'] = message

    if data is not None:
        response['data'] = data

    return response, status_code


def generate_sku(casting_name: str, color: str, year: int) -> str:
    """
    Generate SKU for a car model

    Args:
        casting_name: Name of the casting
        color: Color of the model
        year: Release year

    Returns:
        Generated SKU string
    """
    # Create a deterministic hash from the inputs
    input_str = f"{casting_name}_{color}_{year}".lower().replace(' ', '_')
    hash_obj = hashlib.md5(input_str.encode())
    hash_hex = hash_obj.hexdigest()[:8]

    # Format: HW-YEAR-HASH
    sku = f"HW-{year}-{hash_hex.upper()}"

    return sku


def mask_email(email: str) -> str:
    """
    Mask email address for privacy

    Args:
        email: Email address to mask

    Returns:
        Masked email address

    Example:
        john.doe@example.com -> joh***@example.com
    """
    if not email or '@' not in email:
        return '***@***'

    local, domain = email.split('@', 1)

    if len(local) <= 3:
        masked_local = local[0] + '***'
    else:
        masked_local = local[:3] + '***'

    return f"{masked_local}@{domain}"


def get_current_user_id() -> Optional[int]:
    """
    Get current authenticated user ID from JWT

    Returns:
        User ID or None if not authenticated
    """
    try:
        identity = get_jwt_identity()
        return int(identity) if identity else None
    except:
        return None


def generate_token() -> str:
    """
    Generate a random secure token

    Returns:
        Random token string
    """
    return secrets.token_urlsafe(32)


def hash_token(token: str) -> str:
    """
    Hash a token for secure storage

    Args:
        token: Token to hash

    Returns:
        Hashed token
    """
    return hashlib.sha256(token.encode()).hexdigest()


def get_request_ip() -> str:
    """
    Get client IP address from request

    Returns:
        IP address string
    """
    # Check for proxy headers
    if request.headers.get('X-Forwarded-For'):
        return request.headers.get('X-Forwarded-For').split(',')[0].strip()
    elif request.headers.get('X-Real-IP'):
        return request.headers.get('X-Real-IP')
    else:
        return request.remote_addr or 'unknown'


def get_request_user_agent() -> str:
    """
    Get user agent from request

    Returns:
        User agent string
    """
    return request.headers.get('User-Agent', 'unknown')


def sanitize_search_query(query: str) -> str:
    """
    Sanitize search query to prevent SQL injection

    Args:
        query: Search query string

    Returns:
        Sanitized query string
    """
    if not query:
        return ''

    # Remove special characters that could be used for injection
    # Keep alphanumeric, spaces, hyphens, and underscores
    import re
    sanitized = re.sub(r'[^\w\s\-]', '', query)

    # Limit length
    return sanitized[:100].strip()


def parse_filters(filters: Dict[str, Any]) -> Dict[str, Any]:
    """
    Parse and validate filter parameters

    Args:
        filters: Raw filter dictionary

    Returns:
        Validated filter dictionary
    """
    validated = {}

    # Year range
    if 'year_min' in filters:
        try:
            validated['year_min'] = int(filters['year_min'])
        except (ValueError, TypeError):
            pass

    if 'year_max' in filters:
        try:
            validated['year_max'] = int(filters['year_max'])
        except (ValueError, TypeError):
            pass

    # Price range
    if 'price_min' in filters:
        try:
            validated['price_min'] = float(filters['price_min'])
        except (ValueError, TypeError):
            pass

    if 'price_max' in filters:
        try:
            validated['price_max'] = float(filters['price_max'])
        except (ValueError, TypeError):
            pass

    # String filters (sanitized)
    for key in ['color', 'rarity', 'condition', 'series', 'casting']:
        if key in filters and filters[key]:
            validated[key] = str(filters[key])[:50]

    return validated


def build_pagination_links(base_url: str, page: int, total_pages: int) -> Dict[str, Optional[str]]:
    """
    Build pagination links for API responses

    Args:
        base_url: Base URL for the resource
        page: Current page number
        total_pages: Total number of pages

    Returns:
        Dictionary with pagination links
    """
    links = {
        'self': f"{base_url}?page={page}",
        'first': f"{base_url}?page=1",
        'last': f"{base_url}?page={total_pages}",
        'prev': f"{base_url}?page={page - 1}" if page > 1 else None,
        'next': f"{base_url}?page={page + 1}" if page < total_pages else None
    }

    return links