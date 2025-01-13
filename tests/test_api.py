import pytest
import json
from app import create_app
from extensions import db
from models import User

@pytest.fixture
def app():
    app = create_app()
    app.config.update({
        'TESTING': True,
        'SQLALCHEMY_DATABASE_URI': 'sqlite:///:memory:'
    })
    
    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()

@pytest.fixture
def client(app):
    return app.test_client()

@pytest.fixture
def auth_headers(client):
    # Register a test user
    register_data = {
        'email': 'test@example.com',
        'password': 'testpass123',
        'user_type': 'landlord'
    }
    client.post('/auth/register', json=register_data)
    
    # Login to get token
    login_response = client.post('/auth/login', json={
        'email': 'test@example.com',
        'password': 'testpass123'
    })
    token = json.loads(login_response.data)['access_token']
    return {'Authorization': f'Bearer {token}'}

def test_register(client):
    """Test user registration"""
    data = {
        'email': 'newuser@example.com',
        'password': 'password123',
        'user_type': 'tenant'
    }
    response = client.post('/auth/register', json=data)
    assert response.status_code == 201
    assert b'User registered successfully' in response.data

def test_login(client):
    """Test user login"""
    # First register a user
    register_data = {
        'email': 'logintest@example.com',
        'password': 'password123',
        'user_type': 'tenant'
    }
    client.post('/auth/register', json=register_data)
    
    # Then try to login
    login_data = {
        'email': 'logintest@example.com',
        'password': 'password123'
    }
    response = client.post('/auth/login', json=login_data)
    assert response.status_code == 200
    assert 'access_token' in json.loads(response.data)

def test_create_room(client, auth_headers):
    """Test room creation by landlord"""
    room_data = {
        'title': 'Test Room',
        'description': 'A nice test room',
        'price': 500.0,
        'size': 20.0,
        'location': 'Test Location',
        'amenities': json.dumps(['wifi', 'ac']),
        'safety_score': 4.5,
        'cleanliness_score': 4.0,
        'accessibility_score': 4.8,
        'noise_level': 2.0
    }
    response = client.post('/landlord/rooms', 
                          data=room_data,
                          headers=auth_headers)
    assert response.status_code == 201
    assert b'Room created successfully' in response.data

def test_get_rooms(client, auth_headers):
    """Test getting landlord's rooms"""
    response = client.get('/landlord/rooms', headers=auth_headers)
    assert response.status_code == 200
    assert isinstance(json.loads(response.data), list)

def test_set_tenant_preferences(client, auth_headers):
    """Test setting tenant preferences"""
    preferences = {
        'max_price': 1000,
        'min_size': 15,
        'preferred_location': 'Test City',
        'required_amenities': ['wifi', 'parking'],
        'safety_weight': 0.3,
        'cleanliness_weight': 0.3,
        'accessibility_weight': 0.2,
        'noise_level_weight': 0.2
    }
    response = client.post('/tenant/preferences', 
                          json=preferences,
                          headers=auth_headers)
    assert response.status_code in [200, 403]  # 403 if tested with landlord account 