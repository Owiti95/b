from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from models import db, User, StoreBook, LibraryBook, CartItem, Sale, Borrowing
from sqlalchemy import or_

user_bp = Blueprint('user_routes', __name__)

@user_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    name = data.get('name')
    email = data.get('email')
    password = data.get('password')

    if User.query.filter_by(email=email).first():
        return jsonify({'error': 'Email already registered'}), 400

    user = User(name=name, email=email)
    user.set_password(password)
    db.session.add(user)
    db.session.commit()
    return jsonify(user.to_dict()), 201

# @user_bp.route('/login', methods=['POST'])
# def login():
#     data = request.get_json()
#     email = data.get('email')
#     password = data.get('password')

#     user = User.query.filter_by(email=email).first()
#     if user and user.check_password(password):
#         access_token = create_access_token(identity=user.id)
#         return jsonify({'message': 'Login successful', 'access_token': access_token, 'user': user.to_dict()})


@user_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    user = User.query.filter_by(email=email).first()
    if user and user.check_password(password):
        # Create JWT token with the user's id and is_admin claim
        access_token = create_access_token(identity=user.id, additional_claims={'is_admin': user.is_admin})
        return jsonify({'message': 'Login successful', 'access_token': access_token, 'user': user.to_dict()})
    return jsonify({'error': 'Invalid credentials'}), 401



#     return jsonify({'error': 'Invalid credentials'}), 401

# @user_bp.route('/store_books', methods=['GET'])
# @jwt_required()
# def view_store_books():
#     books = StoreBook.query.all()
#     return jsonify([book.to_dict() for book in books])

@user_bp.route('/store_books', methods=['GET'])
def view_store_books():
    """Fetch all store books without requiring authentication."""
    books = StoreBook.query.all()
    return jsonify([book.to_dict() for book in books])


@user_bp.route('/library_books', methods=['GET'])
# @jwt_required()
def view_library_books():
    books = LibraryBook.query.all()
    return jsonify([book.to_dict() for book in books])

@user_bp.route('/search_books', methods=['GET'])
@jwt_required()
def search_books():
    query = request.args.get('query', '')
    store_books = StoreBook.query.filter(
        or_(StoreBook.title.ilike(f'%{query}%'), StoreBook.genre.ilike(f'%{query}%'))
    ).all()
    library_books = LibraryBook.query.filter(
        or_(LibraryBook.title.ilike(f'%{query}%'), LibraryBook.genre.ilike(f'%{query}%'))
    ).all()
    return jsonify({'store_books': [book.to_dict() for book in store_books], 'library_books': [book.to_dict() for book in library_books]})


@user_bp.route('/borrow_book', methods=['POST'])
@jwt_required()
def borrow_book():
    user_id = get_jwt_identity()
    data = request.get_json()
    book_id = data.get('book_id')

    book = LibraryBook.query.get(book_id)
    if book and book.available_copies > 0:
        borrowing = Borrowing(user_id=user_id, book_id=book.id)
        book.available_copies -= 1
        db.session.add(borrowing)
        db.session.commit()
        return jsonify(borrowing.to_dict()), 201
    return jsonify({'error': 'Book not available for borrowing'}), 400


@user_bp.route('/add_to_cart', methods=['POST'])
@jwt_required()
def add_to_cart():
    user_id = get_jwt_identity()
    data = request.get_json()
    book_id = data.get('book_id')
    quantity = data.get('quantity')

    book = StoreBook.query.get(book_id)
    if not book or quantity <= 0:
        return jsonify({'error': 'Invalid book or quantity'}), 400

    cart_item = CartItem.query.filter_by(user_id=user_id, book_id=book.id).first()
    if cart_item:
        cart_item.quantity += quantity
    else:
        cart_item = CartItem(user_id=user_id, book_id=book.id, quantity=quantity)
        db.session.add(cart_item)

    db.session.commit()

    result = {"message": "Item added to cart successfully"}
    return jsonify(result), 201 



@user_bp.route('/remove_from_cart', methods=['DELETE'])
@jwt_required()
def remove_from_cart():
    user_id = get_jwt_identity()
    data = request.get_json()
    book_id = data.get('book_id')

    cart_item = CartItem.query.filter_by(user_id=user_id, book_id=book_id).first()
    if not cart_item:
        return jsonify({'error': 'Cart item not found'}), 404

    db.session.delete(cart_item)
    db.session.commit()
    return jsonify({'message': 'Book removed from cart successfully'}), 200


    # db.session.commit()
    # return jsonify(cart_item.to_dict()), 201

@user_bp.route('/cart', methods=['GET'])
@jwt_required()
def view_cart():
    user_id = get_jwt_identity()
    cart_items = CartItem.query.filter_by(user_id=user_id).all()
    return jsonify([cart_item.to_dict() for cart_item in cart_items])


@user_bp.route('/checkout', methods=['POST'])
@jwt_required()
def checkout():
    user_id = get_jwt_identity()
    cart_items = CartItem.query.filter_by(user_id=user_id).all()
    if not cart_items:
        return jsonify({'error': 'Your cart is empty'}), 400

    total_price = sum(item.book.price * item.quantity for item in cart_items)
    sale = Sale(user_id=user_id, book_id=cart_items[0].book_id, quantity=cart_items[0].quantity, total_price=total_price, status='Pending')
    db.session.add(sale)
    db.session.commit()
    for item in cart_items:
        db.session.delete(item)
    db.session.commit()

    return jsonify(sale.to_dict()), 201

