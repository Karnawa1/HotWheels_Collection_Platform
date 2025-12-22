"""
Middleware package
Global request/response processing, authentication, and error handling
"""

from app.middleware.auth_middleware import jwt_required, admin_required, optional_jwt
from app.middleware.error_handler import register_error_handlers
from app.middleware.request_logger import setup_request_logging

__all__ = [
    'jwt_required',
    'admin_required', 
    'optional_jwt',
    'register_error_handlers',
    'setup_request_logging'
]