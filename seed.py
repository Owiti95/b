from app import create_app
from config import db
from models import User, StoreBook, LibraryBook, CartItem, Sale, Borrowing
from datetime import datetime

app = create_app()  # Initialize the app

# Create tables
with app.app_context():
    db.create_all()

# Seeding function
def seed_data():
    # Add sample books for the store
    book_1 = StoreBook(title='Sample Book 1', author='Author 1', genre='Fiction', isbn='1234567890', price=19.99, stock=10)
    book_2 = StoreBook(title='Sample Book 2', author='Author 2', genre='Non-Fiction', isbn='0987654321', price=24.99, stock=5)

    # Add sample books for the library
    library_book_1 = LibraryBook(title='Library Book 1', author='Author 1', genre='Fiction', isbn='1122334455', available_copies=3, total_copies=5)
    library_book_2 = LibraryBook(title='Library Book 2', author='Author 2', genre='Non-Fiction', isbn='5566778899', available_copies=2, total_copies=3)

    # Add a regular user with hashed password
    user = User(name='John Doe', email='john@example.com')
    user.set_password('password123')

    # Add an admin user
    admin_user = User(name='Admin User', email='admin@example.com', is_admin=True)
    admin_user.set_password('adminpassword123')

    # Add the data to the database
    db.session.add(book_1)
    db.session.add(book_2)
    db.session.add(library_book_1)
    db.session.add(library_book_2)
    db.session.add(user)
    db.session.add(admin_user)
    db.session.commit()

    # Add cart items (user adds books to cart)
    cart_item_1 = CartItem(user_id=user.id, book_id=book_1.id, quantity=2)
    cart_item_2 = CartItem(user_id=user.id, book_id=book_2.id, quantity=1)
    db.session.add(cart_item_1)
    db.session.add(cart_item_2)

    # Add sales (user buys books)
    sale_1 = Sale(user_id=user.id, book_id=book_1.id, quantity=2, total_price=book_1.price * 2)
    sale_2 = Sale(user_id=user.id, book_id=book_2.id, quantity=1, total_price=book_2.price)
    db.session.add(sale_1)
    db.session.add(sale_2)

    # Add borrowings (user borrows books from the library)
    borrowing_1 = Borrowing(user_id=user.id, book_id=library_book_1.id, status='Approved')
    borrowing_2 = Borrowing(user_id=user.id, book_id=library_book_2.id, status='Pending')
    db.session.add(borrowing_1)
    db.session.add(borrowing_2)

    db.session.commit()

    print("Database seeded successfully!")

# Run the seeding process
if __name__ == "__main__":
    with app.app_context():
        seed_data()




























# from app import create_app
# from config import db
# from models import User, StoreBook, LibraryBook, CartItem, Sale, Borrowing
# from datetime import datetime

# app = create_app()  # Initialize the app

# # Create tables
# with app.app_context():
#     db.create_all()

# # Seeding function
# def seed_data():
#     # Add sample books for the store
#     book_1 = StoreBook(title='Sample Book 1', author='Author 1', genre='Fiction', isbn='1234567890', price=19.99, stock=10)
#     book_2 = StoreBook(title='Sample Book 2', author='Author 2', genre='Non-Fiction', isbn='0987654321', price=24.99, stock=5)

#     # Add sample books for the library
#     library_book_1 = LibraryBook(title='Library Book 1', author='Author 1', genre='Fiction', isbn='1122334455', available_copies=3, total_copies=5)
#     library_book_2 = LibraryBook(title='Library Book 2', author='Author 2', genre='Non-Fiction', isbn='5566778899', available_copies=2, total_copies=3)

#     # Add a user with hashed password
#     user = User(name='John Doe', email='john@example.com')
#     user.set_password('password123')

#     # Add the data to the database
#     db.session.add(book_1)
#     db.session.add(book_2)
#     db.session.add(library_book_1)
#     db.session.add(library_book_2)
#     db.session.add(user)
#     db.session.commit()

#     # Add cart items (user adds books to cart)
#     cart_item_1 = CartItem(user_id=user.id, book_id=book_1.id, quantity=2)
#     cart_item_2 = CartItem(user_id=user.id, book_id=book_2.id, quantity=1)
#     db.session.add(cart_item_1)
#     db.session.add(cart_item_2)

#     # Add sales (user buys books)
#     sale_1 = Sale(user_id=user.id, book_id=book_1.id, quantity=2, total_price=book_1.price * 2)
#     sale_2 = Sale(user_id=user.id, book_id=book_2.id, quantity=1, total_price=book_2.price)
#     db.session.add(sale_1)
#     db.session.add(sale_2)

#     # Add borrowings (user borrows books from the library)
#     borrowing_1 = Borrowing(user_id=user.id, book_id=library_book_1.id, status='Approved')
#     borrowing_2 = Borrowing(user_id=user.id, book_id=library_book_2.id, status='Pending')
#     db.session.add(borrowing_1)
#     db.session.add(borrowing_2)

#     db.session.commit()

#     print("Database seeded successfully!")

# # Run the seeding process
# if __name__ == "__main__":
#     with app.app_context():
#         seed_data()




















# # from app import create_app
# # from config import db
# # from models import User, Category, StoreBook, LibraryBook, CartItem, Sale, Borrowing
# # from datetime import datetime

# # app = create_app()  # Initialize the app

# # # Create tables
# # with app.app_context():
# #     db.create_all()

# # # Seeding function
# # def seed_data():
# #     # Add categories
# #     fiction_category = Category(name='Fiction')
# #     non_fiction_category = Category(name='Non-Fiction')

# #     # Add sample books for the store
# #     book_1 = StoreBook(title='Sample Book 1', author='Author 1', genre='Fiction', isbn='1234567890', price=19.99, stock=10, category=fiction_category)
# #     book_2 = StoreBook(title='Sample Book 2', author='Author 2', genre='Non-Fiction', isbn='0987654321', price=24.99, stock=5, category=non_fiction_category)

# #     # Add sample books for the library
# #     library_book_1 = LibraryBook(title='Library Book 1', author='Author 1', genre='Fiction', isbn='1122334455', available_copies=3, total_copies=5, category=fiction_category)
# #     library_book_2 = LibraryBook(title='Library Book 2', author='Author 2', genre='Non-Fiction', isbn='5566778899', available_copies=2, total_copies=3, category=non_fiction_category)

# #     # Add a user with hashed password
# #     user = User(name='John Doe', email='john@example.com')
# #     user.set_password('password123')

# #     # Add the data to the database
# #     db.session.add(fiction_category)
# #     db.session.add(non_fiction_category)
# #     db.session.add(book_1)
# #     db.session.add(book_2)
# #     db.session.add(library_book_1)
# #     db.session.add(library_book_2)
# #     db.session.add(user)
# #     db.session.commit()

# #     # Add cart items (user adds books to cart)
# #     cart_item_1 = CartItem(user_id=user.id, book_id=book_1.id, quantity=2)
# #     cart_item_2 = CartItem(user_id=user.id, book_id=book_2.id, quantity=1)
# #     db.session.add(cart_item_1)
# #     db.session.add(cart_item_2)

# #     # Add sales (user buys books)
# #     sale_1 = Sale(user_id=user.id, book_id=book_1.id, quantity=2, total_price=book_1.price * 2)
# #     sale_2 = Sale(user_id=user.id, book_id=book_2.id, quantity=1, total_price=book_2.price)
# #     db.session.add(sale_1)
# #     db.session.add(sale_2)

# #     # Add borrowings (user borrows books from the library)
# #     borrowing_1 = Borrowing(user_id=user.id, book_id=library_book_1.id, status='Approved')
# #     borrowing_2 = Borrowing(user_id=user.id, book_id=library_book_2.id, status='Pending')
# #     db.session.add(borrowing_1)
# #     db.session.add(borrowing_2)

# #     db.session.commit()

# #     print("Database seeded successfully!")

# # # Run the seeding process
# # if __name__ == "__main__":
# #     with app.app_context():
# #         seed_data()
