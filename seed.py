from app import create_app
from config import db
from models import User, StoreBook, LibraryBook, CartItem, Sale, Borrowing
from datetime import datetime, timedelta

app = create_app()  # Initialize the app

# Create tables
with app.app_context():
    db.create_all()

# Seeding function
def seed_data():
    # Add sample books for the store
    book_1 = StoreBook(title='The Great Gatsby', author='F. Scott Fitzgerald', genre='Fiction', isbn='1234567890', price=15.99, stock=20)
    book_2 = StoreBook(title='Sapiens', author='Yuval Noah Harari', genre='Non-Fiction', isbn='0987654321', price=20.99, stock=15)
    book_3 = StoreBook(title='1984', author='George Orwell', genre='Fiction', isbn='1231231230', price=10.99, stock=30)
    book_4 = StoreBook(title='Becoming', author='Michelle Obama', genre='Biography', isbn='1123581321', price=25.99, stock=25)
    book_5 = StoreBook(title='The Alchemist', author='Paulo Coelho', genre='Fiction', isbn='9876543210', price=12.99, stock=40)
    book_6 = StoreBook(title='The Catcher in the Rye', author='J.D. Salinger', genre='Fiction', isbn='1112223334', price=9.99, stock=50)
    book_7 = StoreBook(title='Educated', author='Tara Westover', genre='Memoir', isbn='3334445556', price=18.99, stock=10)
    book_8 = StoreBook(title='The Silent Patient', author='Alex Michaelides', genre='Thriller', isbn='5556667778', price=22.99, stock=30)

    # Add sample books for the library
    library_book_1 = LibraryBook(title='To Kill a Mockingbird', author='Harper Lee', genre='Fiction', isbn='1122334455', available_copies=5, total_copies=10)
    library_book_2 = LibraryBook(title='A Brief History of Time', author='Stephen Hawking', genre='Science', isbn='5566778899', available_copies=2, total_copies=4)
    library_book_3 = LibraryBook(title='Pride and Prejudice', author='Jane Austen', genre='Fiction', isbn='3344556677', available_copies=1, total_copies=3)
    library_book_4 = LibraryBook(title='Moby Dick', author='Herman Melville', genre='Adventure', isbn='4455667788', available_copies=3, total_copies=5)
    library_book_5 = LibraryBook(title='The Art of War', author='Sun Tzu', genre='Philosophy', isbn='2233445566', available_copies=4, total_copies=6)
    library_book_6 = LibraryBook(title='The Odyssey', author='Homer', genre='Epic', isbn='9876543210', available_copies=5, total_copies=8)
    library_book_7 = LibraryBook(title='The Hobbit', author='J.R.R. Tolkien', genre='Fantasy', isbn='1111111111', available_copies=3, total_copies=5)

    # Add users with hashed passwords
    user1 = User(name='Alice Johnson', email='alice@example.com')
    user1.set_password('alicepassword123')
    user2 = User(name='Bob Smith', email='bob@example.com')
    user2.set_password('bobpassword123')
    user3 = User(name='Charlie Davis', email='charlie@example.com')
    user3.set_password('charliepassword123')
    user4 = User(name='David Clark', email='david@example.com')
    user4.set_password('davidpassword123')
    user5 = User(name='Eva Thompson', email='eva@example.com')
    user5.set_password('evapassword123')

    # Add an admin user
    admin_user = User(name='Admin User', email='admin@example.com', is_admin=True)
    admin_user.set_password('adminpassword123')

    # Add the data to the database
    db.session.add_all([book_1, book_2, book_3, book_4, book_5, book_6, book_7, book_8, library_book_1, library_book_2, library_book_3, library_book_4, library_book_5, library_book_6, library_book_7, user1, user2, user3, user4, user5, admin_user])
    db.session.commit()

    # Add cart items
    cart_item_1 = CartItem(user_id=user1.id, book_id=book_1.id, quantity=1)
    cart_item_2 = CartItem(user_id=user1.id, book_id=book_2.id, quantity=2)
    cart_item_3 = CartItem(user_id=user2.id, book_id=book_3.id, quantity=3)
    cart_item_4 = CartItem(user_id=user3.id, book_id=book_4.id, quantity=1)
    cart_item_5 = CartItem(user_id=user3.id, book_id=book_5.id, quantity=2)
    cart_item_6 = CartItem(user_id=user4.id, book_id=book_6.id, quantity=1)
    cart_item_7 = CartItem(user_id=user5.id, book_id=book_7.id, quantity=2)

    # Add sales
    sale_1 = Sale(user_id=user1.id, book_id=book_1.id, quantity=1, total_price=book_1.price * 1, status='Completed')
    sale_2 = Sale(user_id=user1.id, book_id=book_2.id, quantity=2, total_price=book_2.price * 2, status='Completed')
    sale_3 = Sale(user_id=user2.id, book_id=book_3.id, quantity=3, total_price=book_3.price * 3, status='Pending')
    sale_4 = Sale(user_id=user3.id, book_id=book_4.id, quantity=1, total_price=book_4.price * 1, status='Completed')
    sale_5 = Sale(user_id=user3.id, book_id=book_5.id, quantity=2, total_price=book_5.price * 2, status='Pending')
    sale_6 = Sale(user_id=user4.id, book_id=book_6.id, quantity=1, total_price=book_6.price * 1, status='Completed')
    sale_7 = Sale(user_id=user5.id, book_id=book_7.id, quantity=2, total_price=book_7.price * 2, status='Completed')

    # Add borrowings
    borrowing_1 = Borrowing(user_id=user1.id, book_id=library_book_1.id, date_borrowed=datetime.utcnow(), due_date=datetime.utcnow() + timedelta(days=14), status='Approved')
    borrowing_2 = Borrowing(user_id=user1.id, book_id=library_book_2.id, date_borrowed=datetime.utcnow(), due_date=datetime.utcnow() + timedelta(days=14), status='Pending')
    borrowing_3 = Borrowing(user_id=user2.id, book_id=library_book_3.id, date_borrowed=datetime.utcnow(), due_date=datetime.utcnow() + timedelta(days=21), status='Approved')
    borrowing_4 = Borrowing(user_id=user2.id, book_id=library_book_4.id, date_borrowed=datetime.utcnow(), due_date=datetime.utcnow() + timedelta(days=10), status='Approved')
    borrowing_5 = Borrowing(user_id=user3.id, book_id=library_book_5.id, date_borrowed=datetime.utcnow(), due_date=datetime.utcnow() + timedelta(days=7), status='Pending')
    borrowing_6 = Borrowing(user_id=user4.id, book_id=library_book_6.id, date_borrowed=datetime.utcnow(), due_date=datetime.utcnow() + timedelta(days=14), status='Approved')
    borrowing_7 = Borrowing(user_id=user5.id, book_id=library_book_7.id, date_borrowed=datetime.utcnow(), due_date=datetime.utcnow() + timedelta(days=7), status='Pending')

    # Add the items to the session and commit
    db.session.add_all([cart_item_1, cart_item_2, cart_item_3, cart_item_4, cart_item_5, cart_item_6, cart_item_7, sale_1, sale_2, sale_3, sale_4, sale_5, sale_6, sale_7, borrowing_1, borrowing_2, borrowing_3, borrowing_4, borrowing_5, borrowing_6, borrowing_7])
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

#     # Add a regular user with hashed password
#     user = User(name='John Doe', email='john@example.com')
#     user.set_password('password123')

#     # Add an admin user
#     admin_user = User(name='Admin User', email='admin@example.com', is_admin=True)
#     admin_user.set_password('adminpassword123')

#     # Add the data to the database
#     db.session.add(book_1)
#     db.session.add(book_2)
#     db.session.add(library_book_1)
#     db.session.add(library_book_2)
#     db.session.add(user)
#     db.session.add(admin_user)
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
# # from models import User, StoreBook, LibraryBook, CartItem, Sale, Borrowing
# # from datetime import datetime

# # app = create_app()  # Initialize the app

# # # Create tables
# # with app.app_context():
# #     db.create_all()

# # # Seeding function
# # def seed_data():
# #     # Add sample books for the store
# #     book_1 = StoreBook(title='Sample Book 1', author='Author 1', genre='Fiction', isbn='1234567890', price=19.99, stock=10)
# #     book_2 = StoreBook(title='Sample Book 2', author='Author 2', genre='Non-Fiction', isbn='0987654321', price=24.99, stock=5)

# #     # Add sample books for the library
# #     library_book_1 = LibraryBook(title='Library Book 1', author='Author 1', genre='Fiction', isbn='1122334455', available_copies=3, total_copies=5)
# #     library_book_2 = LibraryBook(title='Library Book 2', author='Author 2', genre='Non-Fiction', isbn='5566778899', available_copies=2, total_copies=3)

# #     # Add a user with hashed password
# #     user = User(name='John Doe', email='john@example.com')
# #     user.set_password('password123')

# #     # Add the data to the database
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




















# # # from app import create_app
# # # from config import db
# # # from models import User, Category, StoreBook, LibraryBook, CartItem, Sale, Borrowing
# # # from datetime import datetime

# # # app = create_app()  # Initialize the app

# # # # Create tables
# # # with app.app_context():
# # #     db.create_all()

# # # # Seeding function
# # # def seed_data():
# # #     # Add categories
# # #     fiction_category = Category(name='Fiction')
# # #     non_fiction_category = Category(name='Non-Fiction')

# # #     # Add sample books for the store
# # #     book_1 = StoreBook(title='Sample Book 1', author='Author 1', genre='Fiction', isbn='1234567890', price=19.99, stock=10, category=fiction_category)
# # #     book_2 = StoreBook(title='Sample Book 2', author='Author 2', genre='Non-Fiction', isbn='0987654321', price=24.99, stock=5, category=non_fiction_category)

# # #     # Add sample books for the library
# # #     library_book_1 = LibraryBook(title='Library Book 1', author='Author 1', genre='Fiction', isbn='1122334455', available_copies=3, total_copies=5, category=fiction_category)
# # #     library_book_2 = LibraryBook(title='Library Book 2', author='Author 2', genre='Non-Fiction', isbn='5566778899', available_copies=2, total_copies=3, category=non_fiction_category)

# # #     # Add a user with hashed password
# # #     user = User(name='John Doe', email='john@example.com')
# # #     user.set_password('password123')

# # #     # Add the data to the database
# # #     db.session.add(fiction_category)
# # #     db.session.add(non_fiction_category)
# # #     db.session.add(book_1)
# # #     db.session.add(book_2)
# # #     db.session.add(library_book_1)
# # #     db.session.add(library_book_2)
# # #     db.session.add(user)
# # #     db.session.commit()

# # #     # Add cart items (user adds books to cart)
# # #     cart_item_1 = CartItem(user_id=user.id, book_id=book_1.id, quantity=2)
# # #     cart_item_2 = CartItem(user_id=user.id, book_id=book_2.id, quantity=1)
# # #     db.session.add(cart_item_1)
# # #     db.session.add(cart_item_2)

# # #     # Add sales (user buys books)
# # #     sale_1 = Sale(user_id=user.id, book_id=book_1.id, quantity=2, total_price=book_1.price * 2)
# # #     sale_2 = Sale(user_id=user.id, book_id=book_2.id, quantity=1, total_price=book_2.price)
# # #     db.session.add(sale_1)
# # #     db.session.add(sale_2)

# # #     # Add borrowings (user borrows books from the library)
# # #     borrowing_1 = Borrowing(user_id=user.id, book_id=library_book_1.id, status='Approved')
# # #     borrowing_2 = Borrowing(user_id=user.id, book_id=library_book_2.id, status='Pending')
# # #     db.session.add(borrowing_1)
# # #     db.session.add(borrowing_2)

# # #     db.session.commit()

# # #     print("Database seeded successfully!")

# # # # Run the seeding process
# # # if __name__ == "__main__":
# # #     with app.app_context():
# # #         seed_data()
