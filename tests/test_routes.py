import pytest
from flask import jsonify
from app import create_app, db
from models import User
from flask_jwt_extended import create_access_token

@pytest.fixture
def client():
    # Set up the test app
    app = create_app(testing=True)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:app.db:'
    with app.test_client() as client:
        with app.app_context():
            db.create_all()
            # Create a test user
            test_user = User(name="Test User", email="test@example.com", is_admin=False)
            test_user.set_password("password123")
            db.session.add(test_user)
            db.session.commit()
        yield client
        with app.app_context():
            db.drop_all()

@pytest.fixture
def auth_headers(client):
    # Generate a JWT token for test user and return authorization headers
    response = client.post('/user_bp/login', json={"email": "test@example.com", "password": "password123"})
    access_token = response.json['access_token']
    return {'Authorization': f'Bearer {access_token}'}

def test_register(client):
    """Test the user registration route."""
    response = client.post('/user_bp/register', json={
        "name": "New User",
        "email": "newuser@example.com",
        "password": "newpassword123"
    })
    assert response.status_code == 201
    assert response.json['message'] == "User registered successfully"

def test_login(client):
    """Test the user login route."""
    response = client.post('/user_bp/login', json={
        "email": "test@example.com",
        "password": "password123"
    })
    assert response.status_code == 200
    assert "access_token" in response.json

def test_get_users(client, auth_headers):
    """Test the get all users route (admin-only)."""
    response = client.get('/admin_bp/users', headers=auth_headers)
    assert response.status_code == 200
    assert isinstance(response.json, list)

def test_add_book(client, auth_headers):
    """Test the admin add book route."""
    response = client.post('/admin_bp/books', headers=auth_headers, json={
        "title": "New Book",
        "author": "Author Name",
        "genre": "Genre",
        "isbn": "1234567890",
        "price": 10.99,
        "stock": 5
    })
    assert response.status_code == 201
    assert response.json['message'] == "Book added"

def test_view_cart(client, auth_headers):
    """Test the view cart route."""
    response = client.get('/user_bp/cart', headers=auth_headers)
    assert response.status_code == 200
    assert isinstance(response.json, list)
