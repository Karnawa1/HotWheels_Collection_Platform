"""
Hot Wheels Platform - Application Entry Point
Starts the Flask application
"""
import os
import sys
from pathlib import Path

# Add app directory to Python path
sys.path.insert(0, str(Path(__file__).parent))

from app import create_app

# Create Flask application
app = create_app(os.getenv('FLASK_ENV', 'development'))

if __name__ == '__main__':
    # Get configuration from environment
    host = os.getenv('API_HOST', '0.0.0.0')
    port = int(os.getenv('API_PORT', 5000))
    debug = os.getenv('DEBUG', 'False').lower() == 'true'

    # Run the application
    print(f"🚀 Starting Hot Wheels API on http://{host}:{port}")
    print(f"   Environment: {os.getenv('FLASK_ENV', 'development')}")
    print(f"   Debug: {debug}")

    app.run(
        host=host,
        port=port,
        debug=debug
    )