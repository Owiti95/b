# from flask import Blueprint, request, jsonify
# from flask_jwt_extended import jwt_required, get_jwt_identity
# from models import db, User, StoreBook, LibraryBook, Sale, Borrowing
# import cloudinary.uploader
# from functools import wraps

# admin_bp = Blueprint('admin_routes', __name__)

# # Helper decorator to check if the user is an admin
# def admin_required(fn):
#     @wraps(fn)
#     @jwt_required()
#     def wrapper(*args, **kwargs):
#         current_user_id = get_jwt_identity()
#         user = User.query.get(current_user_id)
#         if not user or not user.is_admin:
#             return jsonify({'error': 'Admin access required'}), 403
#         return fn(*args, **kwargs)
#     return wrapper

# # Admin Routes

# @admin_bp.route('/users', methods=['GET'])
# @admin_required
# def list_users():
#     users = User.query.all()
#     return jsonify([user.to_dict() for user in users])

# @admin_bp.route('/users/<int:user_id>', methods=['GET'])
# @admin_required
# def get_user(user_id):
#     user = User.query.get(user_id)
#     if not user:
#         return jsonify({'error': 'User not found'}), 404
#     return jsonify(user.to_dict())

# # form-data
# @admin_bp.route('/store_books', methods=['POST'])
# @admin_required
# def add_store_book():
#     # Fetch text data from form-data
#     title = request.form.get('title')
#     author = request.form.get('author')
#     genre = request.form.get('genre')
#     isbn = request.form.get('isbn')
#     price = request.form.get('price', type=float)
#     stock = request.form.get('stock', type=int, default=0)
    
#     # Fetch the image file
#     image = request.files.get('image')  # This will fetch the file from form-data
#     image_url = None
    
#     if image:
#         # Upload image to Cloudinary
#         upload_result = cloudinary.uploader.upload(image)
#         image_url = upload_result['secure_url']  # Get the secure URL of the uploaded image
    
#     # Create a new StoreBook instance
#     new_book = StoreBook(
#         title=title,
#         author=author,
#         genre=genre,
#         isbn=isbn,
#         price=price,
#         stock=stock,
#         image_url=image_url  # Save the uploaded image URL
#     )
    
#     # Save to the database
#     db.session.add(new_book)
#     db.session.commit()
    
#     # Return the newly created book as a JSON response
#     return jsonify(new_book.to_dict()), 201


# # form-data
# @admin_bp.route('/store_books/<int:book_id>', methods=['PUT'])
# @admin_required
# def update_store_book(book_id):
#     book = StoreBook.query.get(book_id)
#     if not book:
#         return jsonify({'error': 'Book not found'}), 404

#     # Fetch text data from form-data
#     title = request.form.get('title', book.title)
#     author = request.form.get('author', book.author)
#     genre = request.form.get('genre', book.genre)
#     isbn = request.form.get('isbn', book.isbn)
#     price = request.form.get('price', book.price, type=float)
#     stock = request.form.get('stock', book.stock, type=int)
    
#     # Fetch the image file
#     image = request.files.get('image')
#     if image:
#         # Upload image to Cloudinary
#         upload_result = cloudinary.uploader.upload(image)
#         book.image_url = upload_result['secure_url']  # Update the image URL
    
#     # Update the book's details
#     book.title = title
#     book.author = author
#     book.genre = genre
#     book.isbn = isbn
#     book.price = price
#     book.stock = stock
    
#     # Commit the changes
#     db.session.commit()
#     return jsonify(book.to_dict())

# @admin_bp.route('/store_books/<int:book_id>', methods=['DELETE'])
# @admin_required
# def delete_store_book(book_id):
#     book = StoreBook.query.get(book_id)
#     if not book:
#         return jsonify({'error': 'Book not found'}), 404
#     db.session.delete(book)
#     db.session.commit()
#     return jsonify({'message': f'Store book {book_id} deleted successfully'})


# # cloudinary
# @admin_bp.route('/library_books', methods=['POST'])
# @admin_required
# def add_library_book():
#     data = request.get_json()
#     image = request.files.get('image')  # Fetching the image file
#     image_url = None
#     if image:
#         # Upload image to Cloudinary
#         upload_result = cloudinary.uploader.upload(image)
#         image_url = upload_result['secure_url']  # Get the secure URL
    
#     new_book = LibraryBook(
#         title=data.get('title'),
#         author=data.get('author'),
#         genre=data.get('genre'),
#         isbn=data.get('isbn'),
#         total_copies=data.get('total_copies', 0),
#         available_copies=data.get('available_copies', 0),
#         image_url=image_url  # Save Cloudinary URL
#     )
#     db.session.add(new_book)
#     db.session.commit()
#     return jsonify(new_book.to_dict()), 201

# # cloudinary
# @admin_bp.route('/library_books/<int:book_id>', methods=['PUT'])
# @admin_required
# def update_library_book(book_id):
#     book = LibraryBook.query.get(book_id)
#     if not book:
#         return jsonify({'error': 'Book not found'}), 404

#     data = request.get_json()
#     image = request.files.get('image')  # Fetching the image file
#     if image:
#         # Upload image to Cloudinary
#         upload_result = cloudinary.uploader.upload(image)
#         book.image_url = upload_result['secure_url']  # Update the image URL

#     book.title = data.get('title', book.title)
#     book.author = data.get('author', book.author)
#     book.genre = data.get('genre', book.genre)
#     book.isbn = data.get('isbn', book.isbn)
#     book.total_copies = data.get('total_copies', book.total_copies)
#     book.available_copies = data.get('available_copies', book.available_copies)
#     db.session.commit()
#     return jsonify(book.to_dict())

# @admin_bp.route('/library_books/<int:book_id>', methods=['DELETE'])
# @admin_required
# def delete_library_book(book_id):
#     book = LibraryBook.query.get(book_id)
#     if not book:
#         return jsonify({'error': 'Book not found'}), 404
#     db.session.delete(book)
#     db.session.commit()
#     return jsonify({'message': f'Library book {book_id} deleted successfully'})


# @admin_bp.route('/approve_order/<int:sale_id>', methods=['POST'])
# @admin_required
# def approve_order(sale_id):
#     action = request.json.get('action')
#     sale = Sale.query.get(sale_id)
#     if not sale:
#         return jsonify({"error": "Order not found"}), 404
#     sale.status = 'Approved' if action == 'approve' else 'Rejected'
#     db.session.commit()
#     return jsonify({"message": f"Order {action}ed", "order": sale.to_dict()}), 200

# @admin_bp.route('/approve_lending/<int:borrowing_id>', methods=['POST'])
# @admin_required
# def approve_lending(borrowing_id):
#     action = request.json.get('action')
#     borrowing = Borrowing.query.get(borrowing_id)
#     if not borrowing:
#         return jsonify({"error": "Lending request not found"}), 404
#     borrowing.status = 'Approved' if action == 'approve' else 'Rejected'
#     db.session.commit()
#     return jsonify({"message": f"Lending request {action}ed", "borrowing": borrowing.to_dict()}), 200

# @admin_bp.route('/view_books', methods=['GET'])
# @admin_required
# def view_books():
#     books = StoreBook.query.all()
#     return jsonify([book.to_dict() for book in books]), 200

# @admin_bp.route('/view_library_books', methods=['GET'])
# @admin_required
# def view_library_books():
#     library_books = LibraryBook.query.all()
#     return jsonify([book.to_dict() for book in library_books]), 200


from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import db, User, StoreBook, LibraryBook, Sale, Borrowing
import cloudinary.uploader
from functools import wraps

admin_bp = Blueprint('admin_routes', __name__)

# Helper decorator to check if the user is an admin
def admin_required(fn):
    @wraps(fn)
    @jwt_required()
    def wrapper(*args, **kwargs):
        current_user_id = get_jwt_identity()
        user = User.query.get(current_user_id)
        if not user or not user.is_admin:
            return jsonify({'error': 'Admin access required'}), 403
        return fn(*args, **kwargs)
    return wrapper

# Helper function to handle image uploads
def upload_image(file):
    if not file:
        return None
    try:
        upload_result = cloudinary.uploader.upload(file)
        return upload_result['secure_url']
    except Exception as e:
        print(f"Image upload error: {e}")
        return None

# Admin Routes

@admin_bp.route('/users', methods=['GET'])
@admin_required
def list_users():
    users = User.query.all()
    return jsonify([user.to_dict() for user in users])

@admin_bp.route('/users/<int:user_id>', methods=['GET'])
@admin_required
def get_user(user_id):
    user = User.query.get(user_id)
    if not user:
        return jsonify({'error': 'User not found'}), 404
    return jsonify(user.to_dict())

@admin_bp.route('/store_books', methods=['POST'])
@admin_required
def add_store_book():
    try:
        # Extract form-data fields
        title = request.form.get('title')
        author = request.form.get('author')
        genre = request.form.get('genre')
        isbn = request.form.get('isbn')
        price = float(request.form.get('price', 0))
        stock = int(request.form.get('stock', 0))

        # Image upload
        image = request.files.get('image')
        image_url = upload_image(image)

        # Validate mandatory fields
        if not all([title, author, genre, isbn]):
            return jsonify({'error': 'Missing required fields'}), 400

        # Create and save new book
        new_book = StoreBook(
            title=title,
            author=author,
            genre=genre,
            isbn=isbn,
            price=price,
            stock=stock,
            image_url=image_url
        )
        db.session.add(new_book)
        db.session.commit()
        return jsonify(new_book.to_dict()), 201

    except Exception as e:
        print(f"Error adding book: {e}")
        return jsonify({'error': 'Failed to add store book'}), 500

@admin_bp.route('/store_books/<int:book_id>', methods=['PUT'])
@admin_required
def update_store_book(book_id):
    book = StoreBook.query.get(book_id)
    if not book:
        return jsonify({'error': 'Book not found'}), 404

    try:
        # Extract fields and update only if present
        book.title = request.form.get('title', book.title)
        book.author = request.form.get('author', book.author)
        book.genre = request.form.get('genre', book.genre)
        book.isbn = request.form.get('isbn', book.isbn)
        book.price = float(request.form.get('price', book.price))
        book.stock = int(request.form.get('stock', book.stock))

        # Handle image upload
        image = request.files.get('image')
        if image:
            book.image_url = upload_image(image)

        db.session.commit()
        return jsonify(book.to_dict())

    except Exception as e:
        print(f"Error updating book: {e}")
        return jsonify({'error': 'Failed to update store book'}), 500

@admin_bp.route('/store_books/<int:book_id>', methods=['DELETE'])
@admin_required
def delete_store_book(book_id):
    book = StoreBook.query.get(book_id)
    if not book:
        return jsonify({'error': 'Book not found'}), 404
    try:
        db.session.delete(book)
        db.session.commit()
        return jsonify({'message': f'Store book {book_id} deleted successfully'})
    except Exception as e:
        print(f"Error deleting book: {e}")
        return jsonify({'error': 'Failed to delete book'}), 500

@admin_bp.route('/approve_order/<int:sale_id>', methods=['POST'])
@admin_required
def approve_order(sale_id):
    sale = Sale.query.get(sale_id)
    if not sale:
        return jsonify({"error": "Order not found"}), 404

    action = request.json.get('action')
    if action not in ['approve', 'reject']:
        return jsonify({"error": "Invalid action"}), 400

    try:
        sale.status = 'Approved' if action == 'approve' else 'Rejected'
        db.session.commit()
        return jsonify({"message": f"Order {action}ed", "order": sale.to_dict()})
    except Exception as e:
        print(f"Error approving order: {e}")
        return jsonify({'error': 'Failed to update order'}), 500

@admin_bp.route('/approve_lending/<int:borrowing_id>', methods=['POST'])
@admin_required
def approve_lending(borrowing_id):
    borrowing = Borrowing.query.get(borrowing_id)
    if not borrowing:
        return jsonify({"error": "Lending request not found"}), 404

    action = request.json.get('action')
    if action not in ['approve', 'reject']:
        return jsonify({"error": "Invalid action"}), 400

    try:
        borrowing.status = 'Approved' if action == 'approve' else 'Rejected'
        db.session.commit()
        return jsonify({"message": f"Lending request {action}ed", "borrowing": borrowing.to_dict()})
    except Exception as e:
        print(f"Error approving lending request: {e}")
        return jsonify({'error': 'Failed to update lending request'}), 500

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
