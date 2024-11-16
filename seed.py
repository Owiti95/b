from app import create_app
from config import db
from models import User, StoreBook, LibraryBook, CartItem, Sale, Borrowing
from datetime import datetime, timedelta

app = create_app()  # Initialize the app

# Create tables
with app.app_context():
    db.create_all()


# Run the seeding process
def seed_data():
    try:
        # Add sample books for the store
        store_books = [
            StoreBook(title='The Great Gatsby', author='F. Scott Fitzgerald', genre='Fiction', isbn='1234567890', price=15.99, stock=20),
            StoreBook(title='Sapiens', author='Yuval Noah Harari', genre='Non-Fiction', isbn='0987654321', price=20.99, stock=15),
            # Add remaining books here...
        ]

        # Add sample library books
        library_books = [
            LibraryBook(title='To Kill a Mockingbird', author='Harper Lee', genre='Fiction', isbn='1122334455', available_copies=5, total_copies=10),
            LibraryBook(title='A Brief History of Time', author='Stephen Hawking', genre='Science', isbn='5566778899', available_copies=2, total_copies=4),
            # Add remaining library books here...
        ]

        # Add users
        users = [
            User(name='Alice Johnson', email='alice@example.com', is_admin=False),
            User(name='Admin User', email='admin@example.com', is_admin=True),
            # Add remaining users here...
        ]

        # Set passwords for users
        for user in users:
            user.set_password('defaultpassword123')

        # Commit base records
        db.session.add_all(store_books + library_books + users)
        db.session.commit()

        # Add cart items
        cart_items = [
            CartItem(user_id=users[0].id, book_id=store_books[0].id, quantity=1),
            # Add additional cart items...
        ]

        # Add borrowings
        borrowings = [
            Borrowing(user_id=users[0].id, book_id=library_books[0].id, date_borrowed=datetime.utcnow(), due_date=datetime.utcnow() + timedelta(days=14), status='Approved'),
            # Add additional borrowings...
        ]

        # Commit associations
        db.session.add_all(cart_items + borrowings)
        db.session.commit()

        print("Database seeded successfully!")
    except Exception as e:
        db.session.rollback()
        print(f"Error seeding data: {e}")
    finally:
        db.session.close()

# Run the seeding function
if __name__ == "__main__":
    with app.app_context():
        seed_data()
