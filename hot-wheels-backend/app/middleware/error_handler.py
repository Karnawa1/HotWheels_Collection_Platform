"""
Error Handler Middleware
Global error handling for consistent API responses
"""

from flask import Flask, jsonify, request
from werkzeug.exceptions import HTTPException
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from flask_jwt_extended.exceptions import JWTExtendedException
from app.utils.helpers import format_error_response
from app.utils.constants import ERROR_MESSAGES
import logging


def register_error_handlers(app: Flask):
    """
    Register global error handlers for the Flask application

    Args:
        app: Flask application instance
    """

    @app.errorhandler(400)
    def bad_request(error):
        """Handle 400 Bad Request errors"""
        return format_error_response(
            message=str(error.description) if hasattr(error, 'description') else "Bad request",
            status_code=400
        )

    @app.errorhandler(401)
    def unauthorized(error):
        """Handle 401 Unauthorized errors"""
        return format_error_response(
            message=ERROR_MESSAGES['UNAUTHORIZED'],
            status_code=401
        )

    @app.errorhandler(403)
    def forbidden(error):
        """Handle 403 Forbidden errors"""
        return format_error_response(
            message=ERROR_MESSAGES['FORBIDDEN'],
            status_code=403
        )

    @app.errorhandler(404)
    def not_found(error):
        """Handle 404 Not Found errors"""
        return format_error_response(
            message=f"Resource not found: {request.path}",
            status_code=404
        )

    @app.errorhandler(405)
    def method_not_allowed(error):
        """Handle 405 Method Not Allowed errors"""
        return format_error_response(
            message=f"Method {request.method} not allowed for {request.path}",
            status_code=405
        )

    @app.errorhandler(409)
    def conflict(error):
        """Handle 409 Conflict errors"""
        return format_error_response(
            message=str(error.description) if hasattr(error, 'description') else "Resource conflict",
            status_code=409
        )

    @app.errorhandler(422)
    def unprocessable_entity(error):
        """Handle 422 Unprocessable Entity errors"""
        return format_error_response(
            message=str(error.description) if hasattr(error, 'description') else "Validation error",
            status_code=422
        )

    @app.errorhandler(429)
    def rate_limit_exceeded(error):
        """Handle 429 Too Many Requests errors"""
        return format_error_response(
            message="Rate limit exceeded. Please try again later.",
            status_code=429
        )

    @app.errorhandler(500)
    def internal_server_error(error):
        """Handle 500 Internal Server Error"""
        app.logger.error(f"Internal server error: {str(error)}", exc_info=True)
        return format_error_response(
            message="An internal server error occurred. Please try again later.",
            status_code=500
        )

    @app.errorhandler(HTTPException)
    def handle_http_exception(error):
        """Handle all other HTTP exceptions"""
        return format_error_response(
            message=error.description,
            status_code=error.code
        )

    @app.errorhandler(IntegrityError)
    def handle_integrity_error(error):
        """Handle database integrity errors (unique constraints, etc.)"""
        app.logger.error(f"Database integrity error: {str(error)}")

        error_msg = str(error.orig) if hasattr(error, 'orig') else str(error)

        # Check for specific constraint violations
        if 'unique constraint' in error_msg.lower():
            if 'email' in error_msg.lower():
                message = ERROR_MESSAGES['DUPLICATE_EMAIL']
            elif 'username' in error_msg.lower():
                message = ERROR_MESSAGES['DUPLICATE_USERNAME']
            else:
                message = "A record with this information already exists"
        else:
            message = "Database constraint violation"

        return format_error_response(message=message, status_code=409)

    @app.errorhandler(SQLAlchemyError)
    def handle_sqlalchemy_error(error):
        """Handle SQLAlchemy database errors"""
        app.logger.error(f"Database error: {str(error)}", exc_info=True)
        return format_error_response(
            message="A database error occurred. Please try again.",
            status_code=500
        )

    @app.errorhandler(JWTExtendedException)
    def handle_jwt_error(error):
        """Handle JWT-related errors"""
        app.logger.warning(f"JWT error: {str(error)}")
        return format_error_response(
            message=ERROR_MESSAGES['UNAUTHORIZED'],
            status_code=401
        )

    @app.errorhandler(ValueError)
    def handle_value_error(error):
        """Handle value errors (usually validation errors)"""
        app.logger.warning(f"Value error: {str(error)}")
        return format_error_response(
            message=str(error),
            status_code=400
        )

    @app.errorhandler(KeyError)
    def handle_key_error(error):
        """Handle missing key errors in request data"""
        app.logger.warning(f"Key error: {str(error)}")
        return format_error_response(
            message=f"Missing required field: {str(error)}",
            status_code=400
        )

    @app.errorhandler(Exception)
    def handle_unexpected_error(error):
        """Handle all other unexpected errors"""
        app.logger.error(f"Unexpected error: {str(error)}", exc_info=True)

        # Don't expose internal error details in production
        if app.config.get('DEBUG'):
            message = str(error)
        else:
            message = "An unexpected error occurred. Please try again."

        return format_error_response(message=message, status_code=500)

    app.logger.info("Error handlers registered successfully")