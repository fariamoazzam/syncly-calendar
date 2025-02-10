# app/__init__.py
"""
This module initializes the Flask application and sets up the database and blueprints.
"""

from flask import Flask
from config import DevelopmentConfig  # Config before local imports
from .models import db  # Local imports
from .auth import auth_bp
from .webhooks import webhook_bp

def create_app():
    """
    Create and configure the Flask application.
    """
    app = Flask(__name__, template_folder='template')

    app.config.from_object(DevelopmentConfig)

    # Initialize the database
    db.init_app(app)

    # Register Blueprints
    app.register_blueprint(auth_bp, url_prefix='/auth')

    # Lazy load routes_bp to avoid circular imports
    from .routes import routes_bp
    app.register_blueprint(routes_bp)

    app.register_blueprint(webhook_bp)

    with app.app_context():
        db.create_all()

    return app