import pytest
from app import create_app
from models import db, User, StoreBook, LibraryBook
from flask_jwt_extended import create_access_token

@pytest.fixture(scope='module')
def app():
    app = create_app()
    app.config.from_object('config.Config')
    # Create a test client
    with app.app_context():
        db.create_all()  # Initialize the database schema
    yield app
    with app.app_context():
        db.drop_all()  # Cleanup after tests

@pytest.fixture
def client(app):
    return app.test_client()

# 1. Test the register route
def test_register(client):
    data = {
        "name": "John Doe",
        "email": "john.doe@example.com",
        "password": "password123"
    }
    response = client.post('/user/register', json=data)
    assert response.status_code == 201
    assert 'name' in response.json
    assert response.json['name'] == 'John Doe'

# 2. Test the login route
def test_login(client):
    data = {
        "email": "john.doe@example.com",
        "password": "password123"
    }
    # First, register the user
    client.post('/user/register', json=data)
    response = client.post('/user/login', json=data)
    assert response.status_code == 200
    assert 'access_token' in response.json
    assert 'user' in response.json

# 3. Test the add book route (Admin required)
@pytest.fixture
def admin_token(client):
    # Register and log in as an admin user
    admin_data = {
        "name": "Admin",
        "email": "admin@example.com",
        "password": "password123"
    }
    client.post('/user/register', json=admin_data)
    admin_login_data = {
        "email": "admin@example.com",
        "password": "password123"
    }
    response = client.post('/user/login', json=admin_login_data)
    return response.json['access_token']

def test_add_book_as_admin(client, admin_token):
    headers = {'Authorization': f'Bearer {admin_token}'}
    book_data = {
        "title": "New Book",
        "author": "John Author",
        "price": 19.99
    }
    response = client.post('/admin/add_book', json=book_data, headers=headers)
    assert response.status_code == 201
    assert 'message' in response.json
    assert response.json['message'] == 'Book added successfully'

# 4. Test the view books route (Admin required)
def test_view_books(client, admin_token):
    headers = {'Authorization': f'Bearer {admin_token}'}
    response = client.get('/admin/view_books', headers=headers)
    assert response.status_code == 200
    assert isinstance(response.json, list)  # Should return a list of books

# 5. Test the search books route
def test_search_books(client):
    # First, add a book to the store
    book_data = {
        "title": "Searchable Book",
        "author": "Search Author",
        "price": 15.99
    }
    client.post('/admin/add_book', json=book_data, headers={'Authorization': 'Bearer fake_token'})  # Add a book with any token
    # Now search for it
    response = client.get('/user/search_books?query=Searchable')
    assert response.status_code == 200
    assert len(response.json['store_books']) > 0  # Should find at least one book

# 6. Test borrow book functionality
@pytest.fixture
def user_token(client):
    # Register and log in as a user
    user_data = {
        "name": "User",
        "email": "user@example.com",
        "password": "password123"
    }
    client.post('/user/register', json=user_data)
    user_login_data = {
        "email": "user@example.com",
        "password": "password123"
    }
    response = client.post('/user/login', json=user_login_data)
    return response.json['access_token']

def test_borrow_book(client, user_token):
    headers = {'Authorization': f'Bearer {user_token}'}
    # Add a book to the library first
    book_data = {"title": "Library Book", "author": "Author", "price": 10.99}
    client.post('/admin/add_book', json=book_data, headers={'Authorization': f'Bearer {user_token}'})
    
    # Borrow the book
    book = LibraryBook.query.first()
    borrow_data = {"book_id": book.id}
    response = client.post('/user/borrow_book', json=borrow_data, headers=headers)
    assert response.status_code == 201
    assert 'user_id' in response.json
    assert response.json['user_id'] == user_token  # Should match user ID

# 7. Test add to cart functionality
def test_add_to_cart(client, user_token):
    headers = {'Authorization': f'Bearer {user_token}'}
    # Add a book to the store first
    book_data = {"title": "Book for Cart", "author": "Author", "price": 10.99}
    client.post('/admin/add_book', json=book_data, headers={'Authorization': f'Bearer {user_token}'})
    
    book = StoreBook.query.first()
    cart_data = {"book_id": book.id, "quantity": 2}
    response = client.post('/user/add_to_cart', json=cart_data, headers=headers)
    assert response.status_code == 201
    assert response.json['quantity'] == 2

