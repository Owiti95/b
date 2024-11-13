from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import db, StoreBook, LibraryBook, Sale, Borrowing, User
from sqlalchemy.exc import SQLAlchemyError

admin_bp = Blueprint('admin', __name__)

# Authentication helper
def admin_required(func):
    @jwt_required()
    def wrapper(*args, **kwargs):
        current_user_id = get_jwt_identity()
        user = User.query.get(current_user_id)
        if not user or not user.is_admin:
            return jsonify({"error": "Admin access required"}), 403
        return func(*args, **kwargs)
    wrapper.__name__ = func.__name__
    return wrapper

@admin_bp.route('/add_book', methods=['POST'])
@admin_required
def add_book():
    data = request.get_json()
    try:
        new_book = StoreBook(**data)
        db.session.add(new_book)
        db.session.commit()
        return jsonify({"message": "Book added successfully", "book": new_book.to_dict()}), 201
    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 400

@admin_bp.route('/update_book/<int:book_id>', methods=['PUT'])
@admin_required
def update_book(book_id):
    data = request.get_json()
    book = StoreBook.query.get(book_id)
    if not book:
        return jsonify({"error": "Book not found"}), 404
    for key, value in data.items():
        setattr(book, key, value)
    db.session.commit()
    return jsonify({"message": "Book updated successfully", "book": book.to_dict()}), 200

@admin_bp.route('/delete_book/<int:book_id>', methods=['DELETE'])
@admin_required
def delete_book(book_id):
    book = StoreBook.query.get(book_id)
    if not book:
        return jsonify({"error": "Book not found"}), 404
    db.session.delete(book)
    db.session.commit()
    return jsonify({"message": "Book deleted successfully"}), 200

@admin_bp.route('/approve_order/<int:sale_id>', methods=['POST'])
@admin_required
def approve_order(sale_id):
    action = request.json.get('action')
    sale = Sale.query.get(sale_id)
    if not sale:
        return jsonify({"error": "Order not found"}), 404
    sale.status = 'Approved' if action == 'approve' else 'Rejected'
    db.session.commit()
    return jsonify({"message": f"Order {action}ed", "order": sale.to_dict()}), 200

@admin_bp.route('/approve_lending/<int:borrowing_id>', methods=['POST'])
@admin_required
def approve_lending(borrowing_id):
    action = request.json.get('action')
    borrowing = Borrowing.query.get(borrowing_id)
    if not borrowing:
        return jsonify({"error": "Lending request not found"}), 404
    borrowing.status = 'Approved' if action == 'approve' else 'Rejected'
    db.session.commit()
    return jsonify({"message": f"Lending request {action}ed", "borrowing": borrowing.to_dict()}), 200

@admin_bp.route('/view_books', methods=['GET'])
@admin_required
def view_books():
    books = StoreBook.query.all()
    return jsonify([book.to_dict() for book in books]), 200

@admin_bp.route('/view_library_books', methods=['GET'])
@admin_required
def view_library_books():
    library_books = LibraryBook.query.all()
    return jsonify([book.to_dict() for book in library_books]), 200
