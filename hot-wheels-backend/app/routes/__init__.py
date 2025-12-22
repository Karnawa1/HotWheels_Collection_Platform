"""
Routes package
API blueprint registration
"""

from flask import Flask
from app.routes.auth import auth_bp
from app.routes.catalog import catalog_bp
from app.routes.collections import collections_bp
from app.routes.marketplace import marketplace_bp


def register_blueprints(app: Flask):
    """
    Register all blueprints with the Flask application

    Args:
        app: Flask application instance
    """
    # API version prefix
    api_prefix = '/api/v1'

    # Register blueprints
    app.register_blueprint(auth_bp, url_prefix=f'{api_prefix}/auth')
    app.register_blueprint(catalog_bp, url_prefix=f'{api_prefix}/catalog')
    app.register_blueprint(collections_bp, url_prefix=f'{api_prefix}/collections')
    app.register_blueprint(marketplace_bp, url_prefix=f'{api_prefix}/marketplace')

    app.logger.info("All blueprints registered successfully")

    # Register root endpoint
    @app.route('/')
    def index():
        return {
            'message': 'Hot Wheels Collector API',
            'version': 'v1',
            'endpoints': {
                'auth': f'{api_prefix}/auth',
                'catalog': f'{api_prefix}/catalog',
                'collections': f'{api_prefix}/collections',
                'marketplace': f'{api_prefix}/marketplace'
            }
        }

    @app.route('/health')
    def health_check():
        """Health check endpoint for monitoring"""
        return {'status': 'healthy', 'service': 'hot-wheels-api'}


__all__ = ['register_blueprints']