import os
import sys
import pytest
from app import create_app, db

# Add project root to Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

@pytest.fixture
def app():
    app = create_app()
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    app.config['TESTING'] = True
    return app

@pytest.fixture
def client(app):
    return app.test_client()

@pytest.fixture
def ctx(app):
    with app.app_context() as ctx:
        db.create_all()
        yield ctx
        db.session.remove()
        db.drop_all() 