"""
Request Logger Middleware
Logs all incoming HTTP requests for debugging and monitoring
"""

from flask import Flask, request, g
from datetime import datetime
import time
import logging


def setup_request_logging(app: Flask):
    """
    Setup request/response logging middleware

    Args:
        app: Flask application instance
    """

    @app.before_request
    def before_request():
        """
        Log incoming request and record start time
        """
        g.start_time = time.time()

        # Log request details
        app.logger.info(
            f"REQUEST: {request.method} {request.path} "
            f"from {request.remote_addr} "
            f"User-Agent: {request.headers.get('User-Agent', 'unknown')}"
        )

        # Log request body for POST/PUT/PATCH (excluding sensitive data)
        if request.method in ['POST', 'PUT', 'PATCH']:
            if request.is_json:
                data = request.get_json()
                # Remove sensitive fields from logs
                safe_data = {k: v for k, v in data.items() if k not in ['password', 'token', 'secret']}
                app.logger.debug(f"Request body: {safe_data}")

    @app.after_request
    def after_request(response):
        """
        Log response details and execution time
        """
        # Calculate request duration
        duration = time.time() - g.get('start_time', time.time())

        # Log response
        app.logger.info(
            f"RESPONSE: {request.method} {request.path} "
            f"Status: {response.status_code} "
            f"Duration: {duration:.3f}s"
        )

        # Add custom headers
        response.headers['X-Request-ID'] = str(g.get('request_id', ''))
        response.headers['X-Response-Time'] = f"{duration:.3f}s"

        return response

    @app.before_request
    def generate_request_id():
        """
        Generate unique request ID for tracking
        """
        import uuid
        g.request_id = str(uuid.uuid4())

    @app.teardown_request
    def teardown_request(exception=None):
        """
        Cleanup after request (log errors if any)
        """
        if exception:
            app.logger.error(
                f"Request failed: {request.method} {request.path} "
                f"Error: {str(exception)}",
                exc_info=True
            )

    app.logger.info("Request logging middleware configured successfully")


def setup_security_headers(app: Flask):
    """
    Add security headers to all responses

    Args:
        app: Flask application instance
    """

    @app.after_request
    def add_security_headers(response):
        """Add security headers to response"""

        # Prevent clickjacking
        response.headers['X-Frame-Options'] = 'DENY'

        # Prevent MIME type sniffing
        response.headers['X-Content-Type-Options'] = 'nosniff'

        # Enable XSS protection
        response.headers['X-XSS-Protection'] = '1; mode=block'

        # Content Security Policy (adjust as needed)
        response.headers['Content-Security-Policy'] = "default-src 'self'"

        # Referrer Policy
        response.headers['Referrer-Policy'] = 'strict-origin-when-cross-origin'

        # CORS headers (if needed)
        if app.config.get('CORS_ENABLED'):
            response.headers['Access-Control-Allow-Origin'] = app.config.get('CORS_ORIGIN', '*')
            response.headers['Access-Control-Allow-Methods'] = 'GET, POST, PUT, PATCH, DELETE, OPTIONS'
            response.headers['Access-Control-Allow-Headers'] = 'Content-Type, Authorization'

        return response

    app.logger.info("Security headers configured successfully")