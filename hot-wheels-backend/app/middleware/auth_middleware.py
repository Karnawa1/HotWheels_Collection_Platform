"""
Authentication Middleware
JWT token validation and authorization decorators
"""

from functools import wraps
from typing import Optional
from flask import request, jsonify, g
from flask_jwt_extended import verify_jwt_in_request, get_jwt_identity, get_jwt
from app.services.auth_service import AuthService
from app.utils.helpers import format_error_response
from app.utils.constants import ERROR_MESSAGES, USER_ROLES


def jwt_required(fn):
    """
    Decorator to require valid JWT authentication
    Attaches current user to Flask g object

    Usage:
        @bp.route('/protected')
        @jwt_required
        def protected_route():
            user_id = g.current_user_id
            return {'message': 'authenticated'}
    """
    @wraps(fn)
    def wrapper(*args, **kwargs):
        try:
            # Verify JWT token
            verify_jwt_in_request()

            # Get user ID from token
            user_id = get_jwt_identity()

            if not user_id:
                return format_error_response(ERROR_MESSAGES['UNAUTHORIZED'], 401)

            # Load user from database
            user = AuthService.get_user_by_id(int(user_id))

            if not user:
                return format_error_response(ERROR_MESSAGES['USER_NOT_FOUND'], 401)

            # Attach to Flask g object
            g.current_user_id = user.userid
            g.current_user = user

            return fn(*args, **kwargs)

        except Exception as e:
            return format_error_response(ERROR_MESSAGES['UNAUTHORIZED'], 401)

    return wrapper


def optional_jwt(fn):
    """
    Decorator for optional JWT authentication
    Attaches user if token is present, continues if not

    Usage:
        @bp.route('/public-or-private')
        @optional_jwt
        def flexible_route():
            user_id = getattr(g, 'current_user_id', None)
            if user_id:
                return {'message': 'authenticated user'}
            return {'message': 'anonymous user'}
    """
    @wraps(fn)
    def wrapper(*args, **kwargs):
        try:
            verify_jwt_in_request(optional=True)

            user_id = get_jwt_identity()

            if user_id:
                user = AuthService.get_user_by_id(int(user_id))
                if user:
                    g.current_user_id = user.userid
                    g.current_user = user

        except:
            # No token or invalid token - continue as anonymous
            pass

        return fn(*args, **kwargs)

    return wrapper


def admin_required(fn):
    """
    Decorator to require admin role
    Must be used with @jwt_required

    Usage:
        @bp.route('/admin-only')
        @jwt_required
        @admin_required
        def admin_route():
            return {'message': 'admin access'}
    """
    @wraps(fn)
    def wrapper(*args, **kwargs):
        # Assumes jwt_required has already run
        user = getattr(g, 'current_user', None)

        if not user:
            return format_error_response(ERROR_MESSAGES['UNAUTHORIZED'], 401)

        if user.role not in [USER_ROLES['ADMIN'], USER_ROLES['MODERATOR']]:
            return format_error_response(ERROR_MESSAGES['FORBIDDEN'], 403)

        return fn(*args, **kwargs)

    return wrapper


def moderator_required(fn):
    """
    Decorator to require moderator or admin role
    Must be used with @jwt_required
    """
    @wraps(fn)
    def wrapper(*args, **kwargs):
        user = getattr(g, 'current_user', None)

        if not user:
            return format_error_response(ERROR_MESSAGES['UNAUTHORIZED'], 401)

        if user.role not in [USER_ROLES['ADMIN'], USER_ROLES['MODERATOR']]:
            return format_error_response(ERROR_MESSAGES['FORBIDDEN'], 403)

        return fn(*args, **kwargs)

    return wrapper


def rate_limit(max_requests: int = 100, window_seconds: int = 60):
    """
    Simple rate limiting decorator (placeholder for production rate limiter)
    In production, use Flask-Limiter or Redis-based rate limiting

    Args:
        max_requests: Maximum requests allowed
        window_seconds: Time window in seconds
    """
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            # TODO: Implement actual rate limiting
            # For now, just pass through
            return fn(*args, **kwargs)
        return wrapper
    return decorator