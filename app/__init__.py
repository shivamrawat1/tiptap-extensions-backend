from flask import Flask
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from config import Config

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    # Initialize extensions
    CORS(app, resources={
        r"/api/*": {
            "origins": "http://localhost:3000",
            "methods": ["GET", "POST", "OPTIONS"],
            "allow_headers": ["Content-Type"]
        }
    })
    db.init_app(app)

    # Register blueprints
    from app.routes import mcq_bp
    app.register_blueprint(mcq_bp, url_prefix='/api')

    # Create database tables
    with app.app_context():
        db.create_all()

    return app 