"""
Flask application factory and configuration.
"""

import os
from flask import Flask
from pathlib import Path

def create_app(config=None):
    """Create and configure the Flask application."""
    
    app = Flask(__name__)
    
    # Configuration
    app.config.update({
        'SECRET_KEY': os.environ.get('SECRET_KEY', 'dev-secret-key-change-in-production'),
        'DEBUG': os.environ.get('FLASK_DEBUG', 'False').lower() == 'true',
        'TESTING': False,
        'WTF_CSRF_ENABLED': True,
        'WTF_CSRF_TIME_LIMIT': None,
    })
    
    # Override with custom config if provided
    if config:
        app.config.update(config)
    
    # Register blueprints
    from .routes import main_bp, api_bp
    app.register_blueprint(main_bp)
    app.register_blueprint(api_bp, url_prefix='/api')
    
    # Error handlers
    from flask import render_template
    
    @app.errorhandler(404)
    def not_found_error(error):
        return render_template('errors/404.html'), 404
    
    @app.errorhandler(500)
    def internal_error(error):
        return render_template('errors/500.html'), 500
    
    return app

# Create default app instance
app = create_app()

