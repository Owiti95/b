from app import create_app
from config import db
from models import User, StoreBook, LibraryBook, CartItem, Borrowing
from datetime import datetime, timedelta
import cloudinary.uploader
import os

import cloudinary
from my_cloudinary_config import Cloudinary_config

cloudinary.config(
    cloud_name=Cloudinary_config["CLOUD_NAME"],
    api_key=Cloudinary_config["API_KEY"],
    api_secret=Cloudinary_config["API_SECRET"]
)

app = create_app()  # Initialize the app

# Create tables
with app.app_context():
    db.create_all()

# Helper function to upload image to Cloudinary
def upload_to_cloudinary(image_path):
    if not os.path.exists(image_path):
        print(f"Image file does not exist: {image_path}")
        return None
    try:
        response = cloudinary.uploader.upload(image_path)
        return response.get('secure_url')  # Return the secure URL
    except Exception as e:
        print(f"Error uploading {image_path} to Cloudinary: {e}")
        return None

# Run the seeding process
def seed_data():
    try:
        # Delete existing data before seeding
        db.session.query(User).delete()
        db.session.commit()

        # Add sample books for the store
        store_books_data = [
            {'title': 'The Great Gatsby', 'author': 'F. Scott Fitzgerald', 'genre': 'Fiction', 'isbn': '123123123', 'price': 15.99, 'stock': 20, 'image_path': './images/gatsby.jpg'},
            {'title': 'Sapiens', 'author': 'Yuval Noah Harari', 'genre': 'Non-Fiction', 'isbn': '987654321', 'price': 20.99, 'stock': 15, 'image_path': './images/sapiens.jpg'},
            
            {'title': '1984', 'author': 'George Orwell', 'genre': 'Dystopian', 'isbn': '2222222221', 'price': 12.99, 'stock': 10, 'image_path': './images/1984.jpg'},
            {'title': 'Pride and Prejudice', 'author': 'Jane Austen', 'genre': 'Romance', 'isbn': '3333333332', 'price': 10.99, 'stock': 25, 'image_path': './images/pride_and_prejudice.jpg'},
            {'title': 'Clean Code', 'author': 'Robert C. Martin', 'genre': 'Programming', 'isbn': '44444444443', 'price': 30.99, 'stock': 8, 'image_path': './images/clean_code.jpg'},
            # {'title': 'The Pragmatic Programmer', 'author': 'Andrew Hunt', 'genre': 'Programming', 'isbn': '5555555554', 'price': 25.99, 'stock': 12, 'image_path': './images/pragmatic_programmer.jpg'},
            {'title': 'Atomic Habits', 'author': 'James Clear', 'genre': 'Self-help', 'isbn': '6666666667', 'price': 18.99, 'stock': 30, 'image_path': './images/atomic_habits.jpg'},
            {'title': 'Educated', 'author': 'Tara Westover', 'genre': 'Biography', 'isbn': '7777777778', 'price': 14.99, 'stock': 10, 'image_path': './images/educated.jpg'},
            # {'title': 'The Power of Now', 'author': 'Eckhart Tolle', 'genre': 'Spirituality', 'isbn': '8888888889', 'price': 17.99, 'stock': 20, 'image_path': './images/power_of_now.jpg'},
            {'title': 'Rich Dad Poor Dad', 'author': 'Robert Kiyosaki', 'genre': 'Finance', 'isbn': '9999999990', 'price': 19.99, 'stock': 18, 'image_path': './images/rich_dad_poor_dad.jpg'},
            {'title': 'Dune', 'author': 'Frank Herbert', 'genre': 'Science Fiction', 'isbn': '1010101011', 'price': 22.99, 'stock': 15, 'image_path': './images/dune.jpg'},
            {'title': 'The Alchemist', 'author': 'Paulo Coelho', 'genre': 'Fiction', 'isbn': '1111111112', 'price': 16.99, 'stock': 25, 'image_path': './images/alchemist.jpg'},
            {'title': 'Thinking, Fast and Slow', 'author': 'Daniel Kahneman', 'genre': 'Psychology', 'isbn': '1212121213', 'price': 23.99, 'stock': 10, 'image_path': './images/thinking_fast_slow.jpg'},
            {'title': 'The Lean Startup', 'author': 'Eric Ries', 'genre': 'Business', 'isbn': '1313131314', 'price': 21.99, 'stock': 20, 'image_path': './images/lean_startup.jpg'},
            {'title': 'The Four Agreements', 'author': 'Don Miguel Ruiz', 'genre': 'Spirituality', 'isbn': '1414141415', 'price': 15.99, 'stock': 18, 'image_path': './images/four_agreements.jpg'},
            # {'title': 'A Game of Thrones', 'author': 'George R.R. Martin', 'genre': 'Fantasy', 'isbn': '1515151516', 'price': 24.99, 'stock': 12, 'image_path': './images/game_of_thrones.jpg'},
            {'title': 'Becoming', 'author': 'Michelle Obama', 'genre': 'Biography', 'isbn': '1616161617', 'price': 19.99, 'stock': 10, 'image_path': './images/becoming.jpg'},
            {'title': 'The Subtle Art of Not Giving a F*ck', 'author': 'Mark Manson', 'genre': 'Self-help', 'isbn': '1717171718', 'price': 18.99, 'stock': 25, 'image_path': './images/subtle_art.jpg'},
            {'title': 'Zero to One', 'author': 'Peter Thiel', 'genre': 'Business', 'isbn': '1818181819', 'price': 22.99, 'stock': 15, 'image_path': './images/zero_to_one.jpg'},
            {'title': 'The Road', 'author': 'Cormac McCarthy', 'genre': 'Post-apocalyptic', 'isbn': '1919191910', 'price': 14.99, 'stock': 8, 'image_path': './images/the_road.jpg'},
        ]

        store_books = []
        for book_data in store_books_data:
            image_url = upload_to_cloudinary(book_data.pop('image_path'))
            if image_url:
                store_books.append(StoreBook(image_url=image_url, **book_data))

        # Add sample library books
        library_books_data = [
            # {'title': 'To Kill a Mockingbird', 'author': 'Harper Lee', 'genre': 'Fiction', 'isbn': '1122334455', 'available_copies': 5, 'total_copies': 10, 'image_path': './images/mockingbird.jpg'},
            {'title': 'A Brief History of Time', 'author': 'Stephen Hawking', 'genre': 'Science', 'isbn': '5566778123', 'available_copies': 2, 'total_copies': 4, 'image_path': './images/brief_history.jpg'},
            
            # {'title': 'The Art of War', 'author': 'Sun Tzu', 'genre': 'Philosophy', 'isbn': '6666666666', 'available_copies': 3, 'total_copies': 5, 'image_path': './images/art_of_war.jpg'},
            {'title': 'The Catcher in the Rye', 'author': 'J.D. Salinger', 'genre': 'Fiction', 'isbn': '7777777777', 'available_copies': 4, 'total_copies': 6, 'image_path': './images/catcher_in_the_rye.jpg'},
            {'title': 'The Selfish Gene', 'author': 'Richard Dawkins', 'genre': 'Biology', 'isbn': '8888888888', 'available_copies': 1, 'total_copies': 3, 'image_path': './images/selfish_gene.jpg'},
            {'title': 'Crime and Punishment', 'author': 'Fyodor Dostoevsky', 'genre': 'Classic', 'isbn': '2020202020', 'available_copies': 6, 'total_copies': 10, 'image_path': './images/crime_and_punishment.jpg'},
            {'title': 'The Hobbit', 'author': 'J.R.R. Tolkien', 'genre': 'Fantasy', 'isbn': '2121212121', 'available_copies': 5, 'total_copies': 8, 'image_path': './images/hobbit.jpg'},
            {'title': 'Moby-Dick', 'author': 'Herman Melville', 'genre': 'Classic', 'isbn': '2323232323', 'available_copies': 4, 'total_copies': 7, 'image_path': './images/moby_dick.jpg'},
            {'title': 'Brave New World', 'author': 'Aldous Huxley', 'genre': 'Dystopian', 'isbn': '2424242424', 'available_copies': 3, 'total_copies': 6, 'image_path': './images/brave_new_world.jpg'},
            {'title': 'Les Misérables', 'author': 'Victor Hugo', 'genre': 'Historical Fiction', 'isbn': '2525252525', 'available_copies': 2, 'total_copies': 5, 'image_path': './images/les_miserables.jpg'},
            {'title': 'Jane Eyre', 'author': 'Charlotte Brontë', 'genre': 'Romance', 'isbn': '2626262626', 'available_copies': 3, 'total_copies': 7, 'image_path': './images/jane_eyre.jpg'},
            {'title': 'The Grapes of Wrath', 'author': 'John Steinbeck', 'genre': 'Historical Fiction', 'isbn': '2727272727', 'available_copies': 2, 'total_copies': 6, 'image_path': './images/grapes_of_wrath.jpg'},
            {'title': 'Dracula', 'author': 'Bram Stoker', 'genre': 'Horror', 'isbn': '2828282828', 'available_copies': 4, 'total_copies': 8, 'image_path': './images/dracula.jpg'},
            {'title': 'Wuthering Heights', 'author': 'Emily Brontë', 'genre': 'Romance', 'isbn': '2929292929', 'available_copies': 3, 'total_copies': 7, 'image_path': './images/wuthering_heights.jpg'},
            {'title': 'Frankenstein', 'author': 'Mary Shelley', 'genre': 'Horror', 'isbn': '3030303030', 'available_copies': 4, 'total_copies': 6, 'image_path': './images/frankenstein.jpg'},
            {'title': 'The Odyssey', 'author': 'Homer', 'genre': 'Epic', 'isbn': '3131313131', 'available_copies': 2, 'total_copies': 5, 'image_path': './images/odyssey.jpg'},
            {'title': 'War and Peace', 'author': 'Leo Tolstoy', 'genre': 'Historical Fiction', 'isbn': '3232323232', 'available_copies': 3, 'total_copies': 7, 'image_path': './images/war_and_peace.jpg'},
            {'title': 'The Brothers Karamazov', 'author': 'Fyodor Dostoevsky', 'genre': 'Classic', 'isbn': '3333333333', 'available_copies': 4, 'total_copies': 8, 'image_path': './images/brothers_karamazov.jpg'},
            {'title': 'Meditations', 'author': 'Marcus Aurelius', 'genre': 'Philosophy', 'isbn': '3434343434', 'available_copies': 6, 'total_copies': 10, 'image_path': './images/meditations.jpg'},
            {'title': 'The Picture of Dorian Gray', 'author': 'Oscar Wilde', 'genre': 'Classic', 'isbn': '3535353535', 'available_copies': 3, 'total_copies': 5, 'image_path': './images/dorian_gray.jpg'},
        ]

        library_books = []
        for book_data in library_books_data:
            image_url = upload_to_cloudinary(book_data.pop('image_path'))
            if image_url:
                library_books.append(LibraryBook(image_url=image_url, **book_data))

        # Add users with unique emails
        users = [
            User(name='Alice Johnson', email='alice@example.com', is_admin=False),
            User(name='Admin User', email='admin@example.com', is_admin=True),
            User(name='Bob Smith', email='bob@example.com', is_admin=False),  # Unique email
            # Add remaining users here...
        ]

        # Set passwords for users
        for user in users:
            user.set_password('defaultpassword123')

        # Commit base records
        db.session.add_all(store_books + library_books + users)
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
