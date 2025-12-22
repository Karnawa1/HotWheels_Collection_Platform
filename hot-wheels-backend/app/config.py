"""
Flask Application Configuration
Environment-based configuration with automatic migration support
"""
import os
from datetime import timedelta


def get_required_env(key: str, default: str = None) -> str:
    """
    Get required environment variable.
    In production, raises error if not set. In development/testing, uses default.
    """
    value = os.getenv(key)
    if value:
        return value
    
    env = os.getenv('FLASK_ENV', 'development')
    if env == 'production' and default is None:
        raise ValueError(f"Required environment variable '{key}' is not set")
    
    return default or ''


class Config:
    """Base configuration"""

    # Application
    APP_NAME = os.getenv('APP_NAME', 'Hot Wheels Collector API')
    APP_VERSION = os.getenv('APP_VERSION', '1.0.0')
    
    # SECURITY: SECRET_KEY must be set via environment variable
    # No default value - will fail in production if not set
    SECRET_KEY = get_required_env('SECRET_KEY', 'dev-secret-key-for-testing-only')

    # Database - URL must be provided via environment
    SQLALCHEMY_DATABASE_URI = get_required_env(
        'DATABASE_URL',
        'postgresql://hotwheels_admin:dev_password@localhost:5432/hotwheels_dev'
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ECHO = False

    # Database connection pool
    SQLALCHEMY_ENGINE_OPTIONS = {
        'pool_pre_ping': True,
        'pool_recycle': 300,
        'pool_size': 10,
        'max_overflow': 20
    }

    # Redis - credentials from environment
    REDIS_URL = get_required_env('REDIS_URL', 'redis://localhost:6379/0')
    REDIS_HOST = os.getenv('REDIS_HOST', 'localhost')
    REDIS_PORT = int(os.getenv('REDIS_PORT', 6379))
    REDIS_PASSWORD = os.getenv('REDIS_PASSWORD', '')

    # JWT - SECURITY: Must be set via environment variable
    JWT_SECRET_KEY = get_required_env('JWT_SECRET_KEY', 'dev-jwt-secret-for-testing-only')
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(seconds=int(os.getenv('JWT_ACCESS_TOKEN_EXPIRES', 86400)))
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(seconds=int(os.getenv('JWT_REFRESH_TOKEN_EXPIRES', 2592000)))

    # CORS
    CORS_ORIGINS = os.getenv('CORS_ORIGIN', '*').split(',')

    # Logging
    LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
    LOG_FILE = os.getenv('LOG_FILE', 'logs/app.log')

    # Pagination
    DEFAULT_PAGE_SIZE = int(os.getenv('DEFAULT_PAGE_SIZE', 20))
    MAX_PAGE_SIZE = int(os.getenv('MAX_PAGE_SIZE', 100))

    # File uploads
    MAX_CONTENT_LENGTH = int(os.getenv('MAX_CONTENT_LENGTH', 16 * 1024 * 1024))  # 16MB
    UPLOAD_FOLDER = os.getenv('UPLOAD_FOLDER', 'uploads')

    # Migrations
    AUTO_MIGRATE = os.getenv('AUTO_MIGRATE', 'True').lower() == 'true'
    MIGRATIONS_DIR = os.getenv('MIGRATIONS_DIR', 'migrations')

class DevelopmentConfig(Config):
    """Development configuration"""
    DEBUG = True
    TESTING = False
    SQLALCHEMY_ECHO = False  # Set to True to see SQL queries

class ProductionConfig(Config):
    """Production configuration - strict environment variable requirements"""
    DEBUG = False
    TESTING = False
    SQLALCHEMY_ECHO = False

    # In production, all secrets MUST come from environment variables
    # get_required_env will raise ValueError if not set
    SECRET_KEY = get_required_env('SECRET_KEY')  # Required, no default
    JWT_SECRET_KEY = get_required_env('JWT_SECRET_KEY')  # Required, no default
    SQLALCHEMY_DATABASE_URI = get_required_env('DATABASE_URL')  # Required, no default

    @classmethod
    def init_app(cls, app):
        """Validate production configuration on startup"""
        # Verify critical settings are not development defaults
        if 'dev-' in (cls.SECRET_KEY or '') or 'test' in (cls.SECRET_KEY or '').lower():
            raise ValueError("Production SECRET_KEY appears to be a development value!")
        
        if 'dev-' in (cls.JWT_SECRET_KEY or '') or 'test' in (cls.JWT_SECRET_KEY or '').lower():
            raise ValueError("Production JWT_SECRET_KEY appears to be a development value!")
        
        app.logger.info("✅ Production configuration validated")

class TestingConfig(Config):
    """Testing configuration"""
    DEBUG = True
    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.getenv(
        'TEST_DATABASE_URL',
        'postgresql://hotwheels_admin:secure_password_123@postgres:5432/hotwheels_test_db'
    )
    AUTO_MIGRATE = False  # Don't auto-migrate in tests

# Configuration dictionary
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}