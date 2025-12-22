"""
Flask Application Factory
Creates and configures the Flask application with automatic migrations
"""
import os
import logging
from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask_cors import CORS

# Initialize extensions
db = SQLAlchemy()
jwt = JWTManager()

def create_app(config_name='development'):
    """Create and configure Flask application"""

    app = Flask(__name__)

    # Load configuration
    from app.config import config
    app.config.from_object(config[config_name])

    # Setup logging
    setup_logging(app)

    # Initialize extensions
    db.init_app(app)
    jwt.init_app(app)
    CORS(app, resources={r"/api/*": {"origins": "*"}})

    # Register CLI commands
    from app.cli_commands import register_commands
    register_commands(app)

    # Run database migrations on startup (only if AUTO_MIGRATE is True)
    if app.config.get('AUTO_MIGRATE', True):
        run_startup_migrations(app)

    # Register blueprints
    register_blueprints(app)

    # Register middleware
    register_middleware(app)

    # Register error handlers
    register_error_handlers(app)

    # Health check endpoint
    @app.route('/health', methods=['GET'])
    def health_check():
        return jsonify({
            'status': 'healthy',
            'service': 'Hot Wheels API',
            'version': app.config.get('APP_VERSION', '1.0.0')
        }), 200

    app.logger.info(f"✅ Flask app '{app.config['APP_NAME']}' created successfully")

    return app

def setup_logging(app):
    """Configure application logging"""
    log_level = app.config.get('LOG_LEVEL', 'INFO')

    logging.basicConfig(
        level=getattr(logging, log_level),
        format='%(asctime)s [%(levelname)s] %(name)s: %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )

    # Set Flask logger level
    app.logger.setLevel(getattr(logging, log_level))

def run_startup_migrations(app):
    """Run database migrations on application startup"""
    app.logger.info("🔄 Checking for pending database migrations...")

    try:
        from app.utils.db_manager import DatabaseManager

        database_url = app.config.get('SQLALCHEMY_DATABASE_URI')
        if not database_url:
            app.logger.error("❌ Database URL not configured")
            return

        manager = DatabaseManager(database_url)
        success = manager.run_migrations()

        if success:
            app.logger.info("✅ Database migrations completed")
        else:
            app.logger.error("❌ Database migrations failed")
            # Don't exit - allow app to start for debugging

    except Exception as e:
        app.logger.error(f"❌ Migration error: {e}")
        # Don't exit - allow app to start for debugging

def register_blueprints(app):
    """Register Flask blueprints (API routes)"""
    from app.routes.auth import auth_bp
    from app.routes.catalog import catalog_bp
    from app.routes.collections import collections_bp
    from app.routes.marketplace import marketplace_bp
    
    # API v1
    app.register_blueprint(auth_bp, url_prefix='/api/v1/auth')
    app.register_blueprint(catalog_bp, url_prefix='/api/v1/catalog')
    app.register_blueprint(collections_bp, url_prefix='/api/v1/collections')
    app.register_blueprint(marketplace_bp, url_prefix='/api/v1/marketplace')
    
    app.logger.info("✓ Blueprints registered")

def register_middleware(app):
    """Register middleware"""
    from app.middleware.request_logger import setup_request_logging, setup_security_headers
    
    # Request logging
    setup_request_logging(app)
    setup_security_headers(app)
    
    app.logger.info("✓ Middleware registered")

def register_error_handlers(app):
    """Register error handlers"""
    from app.middleware.error_handler import register_error_handlers as setup_error_handlers
    
    # Call the function that registers all error handlers
    setup_error_handlers(app)
    
    app.logger.info("✓ Error handlers registered")