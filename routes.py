from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity, create_access_token
from flask_bcrypt import Bcrypt
from datetime import timedelta
from models import db, User, StoreBook, Sale, CartItem, Borrowing, LibraryBook

# Initialize bcrypt for password hashing
bcrypt = Bcrypt()

# Create blueprints for admin and user
admin_bp = Blueprint('admin_bp', __name__)
user_bp = Blueprint('user_bp', __name__)

# User Registration Route
@user_bp.route('/register', methods=['POST'])
def register():
    """Register a new user"""
    data = request.get_json()
    
    # Validate input data
    if not data.get('name') or not data.get('email') or not data.get('password'):
        return jsonify({"message": "Name, email, and password are required"}), 400
    
    # Check if the email already exists
    existing_user = User.query.filter_by(email=data['email']).first()
    if existing_user:
        return jsonify({"message": "Email already in use"}), 400
    
    # Create a new user
    new_user = User(
        name=data['name'],
        email=data['email'],
        is_admin=data.get('is_admin', False)  # Default to False if not provided
    )
    new_user.set_password(data['password'])
    
    # Add user to database
    db.session.add(new_user)
    db.session.commit()
    
    return jsonify({"message": "User registered successfully"}), 201


# User Login Route
@user_bp.route('/login', methods=['POST'])
def login():
    """Login a user"""
    data = request.get_json()
    
    # Validate input data
    if not data.get('email') or not data.get('password'):
        return jsonify({"message": "Email and password are required"}), 400
    
    user = User.query.filter_by(email=data['email']).first()
    
    # Check if user exists and password is correct
    if not user or not user.check_password(data['password']):
        return jsonify({"message": "Invalid email or password"}), 401
    
    # Generate a JWT token
    access_token = create_access_token(identity={"id": user.id, "email": user.email, "role": "admin" if user.is_admin else "user"}, expires_delta=timedelta(hours=1))
    
    return jsonify({"access_token": access_token}), 200


# Admin Routes
@admin_bp.route('/users', methods=['GET'])
@jwt_required()
def get_users():
    """Get all users (admin-only route)"""
    current_user = get_jwt_identity()
    # Check if user is an admin
    if current_user['role'] != 'admin':
        return jsonify({"message": "Permission denied"}), 403
    users = User.query.all()
    return jsonify([user.to_dict() for user in users]), 200

@admin_bp.route('/user/<int:user_id>', methods=['DELETE'])
@jwt_required()
def delete_user(user_id):
    """Delete a user (admin-only route)"""
    current_user = get_jwt_identity()
    # Check if user is an admin
    if current_user['role'] != 'admin':
        return jsonify({"message": "Permission denied"}), 403
    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()
    return jsonify({"message": "User deleted"}), 200

@admin_bp.route('/books', methods=['POST'])
@jwt_required()
def add_book():
    """Add a new book (admin-only route)"""
    current_user = get_jwt_identity()
    # Check if user is an admin
    if current_user['role'] != 'admin':
        return jsonify({"message": "Permission denied"}), 403
    data = request.get_json()
    new_book = StoreBook(
        title=data['title'],
        author=data['author'],
        genre=data['genre'],
        isbn=data['isbn'],
        price=data['price'],
        stock=data['stock']
    )
    db.session.add(new_book)
    db.session.commit()
    return jsonify({"message": "Book added"}), 201


# User Routes
@user_bp.route('/books', methods=['GET'])
@jwt_required()
def get_books():
    """Get all books available in the store (user route)"""
    books = StoreBook.query.all()
    return jsonify([book.to_dict() for book in books]), 200

@user_bp.route('/cart', methods=['GET'])
@jwt_required()
def view_cart():
    """View user's cart"""
    current_user = get_jwt_identity()
    cart_items = CartItem.query.filter_by(user_id=current_user['id']).all()
    return jsonify([item.to_dict() for item in cart_items]), 200

@user_bp.route('/cart', methods=['POST'])
@jwt_required()
def add_to_cart():
    """Add a book to the cart"""
    current_user = get_jwt_identity()
    data = request.get_json()
    book = StoreBook.query.get_or_404(data['book_id'])
    cart_item = CartItem(user_id=current_user['id'], book_id=book.id, quantity=data['quantity'])
    db.session.add(cart_item)
    db.session.commit()
    return jsonify({"message": "Book added to cart"}), 201

@user_bp.route('/sales', methods=['POST'])
@jwt_required()
def make_purchase():
    """User makes a purchase (buy books from the store)"""
    current_user = get_jwt_identity()
    data = request.get_json()
    cart_items = CartItem.query.filter_by(user_id=current_user['id']).all()
    total_price = 0

    for item in cart_items:
        book = StoreBook.query.get_or_404(item.book_id)
        if book.stock < item.quantity:
            return jsonify({"message": f"Not enough stock for {book.title}"}), 400
        total_price += book.price * item.quantity
        book.stock -= item.quantity  # Decrease stock after purchase

    # Create sale records
    for item in cart_items:
        sale = Sale(user_id=current_user['id'], book_id=item.book_id, quantity=item.quantity, total_price=item.quantity * StoreBook.query.get(item.book_id).price)
        db.session.add(sale)
    
    # Clear the user's cart after purchase
    CartItem.query.filter_by(user_id=current_user['id']).delete()

    db.session.commit()
    return jsonify({"message": "Purchase successful", "total_price": total_price}), 201

@user_bp.route('/borrowings', methods=['GET'])
@jwt_required()
def view_borrowings():
    """View borrowed books"""
    current_user = get_jwt_identity()
    borrowings = Borrowing.query.filter_by(user_id=current_user['id']).all()
    return jsonify([borrowing.to_dict() for borrowing in borrowings]), 200

@user_bp.route('/borrow', methods=['POST'])
@jwt_required()
def borrow_book():
    """User borrows a book from the library"""
    current_user = get_jwt_identity()
    data = request.get_json()
    book = LibraryBook.query.get_or_404(data['book_id'])

    if book.available_copies <= 0:
        return jsonify({"message": "No available copies to borrow"}), 400
    
    borrowing = Borrowing(user_id=current_user['id'], book_id=book.id, status='Pending')
    book.available_copies -= 1  # Decrease available copies when borrowed
    db.session.add(borrowing)
    db.session.commit()

    return jsonify({"message": "Book borrowing requested"}), 201
