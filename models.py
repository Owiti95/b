# # from sqlalchemy.ext.associationproxy import association_proxy
# # from sqlalchemy.orm import validates, relationship
# # from config import db
# # from sqlalchemy import MetaData, Table, ForeignKey
# # from sqlalchemy_serializer import SerializerMixin
# # from flask_bcrypt import Bcrypt
# # import re
# # from datetime import datetime, timedelta

# # bcrypt = Bcrypt()
# # metadata = MetaData()

# # # Association Tables
# # cart_items_association = Table('cart_items_association', db.Model.metadata,
# #     db.Column('user_id', db.Integer, db.ForeignKey('users.id'), primary_key=True),
# #     db.Column('book_id', db.Integer, db.ForeignKey('store_books.id'), primary_key=True),
# #     db.Column('quantity', db.Integer, nullable=False)
# # )

# # borrowings_association = Table('borrowings_association', db.Model.metadata,
# #     db.Column('user_id', db.Integer, db.ForeignKey('users.id'), primary_key=True),
# #     db.Column('book_id', db.Integer, db.ForeignKey('library_books.id'), primary_key=True),
# #     db.Column('date_borrowed', db.Date, default=datetime.utcnow),
# #     db.Column('due_date', db.Date, default=lambda: datetime.utcnow() + timedelta(days=70)),
# #     db.Column('date_returned', db.Date),
# #     db.Column('status', db.String, default='Pending')
# # )

# # # Models
# # class User(db.Model, SerializerMixin):
# #     __tablename__ = 'users'
# #     serialize_rules = ('-password_hash', '-borrowings.user', '-sales.user', '-cart_items.user')

# #     id = db.Column(db.Integer, primary_key=True)
# #     name = db.Column(db.String, nullable=False)
# #     email = db.Column(db.String, unique=True, nullable=False)
# #     password_hash = db.Column(db.String, nullable=False)
# #     is_admin = db.Column(db.Boolean, default=False)
# #     profile_image = db.Column(db.String, nullable=True)  # Cloudinary URL for profile picture

# #     # Relationships
# #     borrowings = relationship('Borrowing', back_populates='user', cascade='all, delete-orphan', lazy='joined')
# #     sales = relationship('Sale', back_populates='user', cascade='all, delete-orphan', lazy='joined')
# #     cart_items = relationship('CartItem', back_populates='user', cascade='all, delete-orphan', lazy='joined')

# #     @validates('email')
# #     def validate_email(self, key, email):
# #         valid_email = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
# #         if not re.match(valid_email, email):
# #             raise ValueError("Invalid email")
# #         return email

# #     def set_password(self, password):
# #         self.password_hash = bcrypt.generate_password_hash(password).decode('utf-8')

# #     def check_password(self, password):
# #         return bcrypt.check_password_hash(self.password_hash, password)

# #     def __repr__(self):
# #         return f'<User {self.name}, Email: {self.email}>'

# # class StoreBook(db.Model, SerializerMixin):
# #     __tablename__ = 'store_books'
# #     serialize_rules = ('-cart_items.book', '-sales.book')

# #     id = db.Column(db.Integer, primary_key=True)
# #     title = db.Column(db.String, nullable=False)
# #     author = db.Column(db.String, nullable=False)
# #     genre = db.Column(db.String, nullable=False)
# #     isbn = db.Column(db.String, unique=True, nullable=False)
# #     price = db.Column(db.Float, nullable=False)
# #     stock = db.Column(db.Integer, default=0)
# #     image_url = db.Column(db.String, nullable=True)  # Cloudinary URL for book cover

# #     # Relationships
# #     cart_items = relationship('CartItem', back_populates='book', cascade='all, delete-orphan', lazy='joined')
# #     sales = relationship('Sale', back_populates='book', cascade='all, delete-orphan', lazy='joined')

# #     def __repr__(self):
# #         return f'<StoreBook {self.title} by {self.author}>'

# # class LibraryBook(db.Model, SerializerMixin):
# #     __tablename__ = 'library_books'
# #     serialize_rules = ('-borrowings.book',)

# #     id = db.Column(db.Integer, primary_key=True)
# #     title = db.Column(db.String, nullable=False)
# #     author = db.Column(db.String, nullable=False)
# #     genre = db.Column(db.String, nullable=False)
# #     isbn = db.Column(db.String, unique=True, nullable=False)
# #     available_copies = db.Column(db.Integer, default=0)
# #     total_copies = db.Column(db.Integer, default=0)
# #     image_url = db.Column(db.String, nullable=True)  # Cloudinary URL for book cover

# #     # Relationships
# #     borrowings = relationship('Borrowing', back_populates='book', cascade='all, delete-orphan', lazy='joined')

# #     def __repr__(self):
# #         return f'<LibraryBook {self.title} by {self.author}>'

# # class CartItem(db.Model, SerializerMixin):
# #     __tablename__ = 'cart_items'
# #     serialize_rules = ('-user.cart_items', '-book.cart_items')

# #     id = db.Column(db.Integer, primary_key=True)
# #     user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
# #     book_id = db.Column(db.Integer, db.ForeignKey('store_books.id'), nullable=False)
# #     quantity = db.Column(db.Integer, nullable=False)

# #     # Relationships
# #     user = relationship('User', back_populates='cart_items')
# #     book = relationship('StoreBook', back_populates='cart_items')

# #     def __repr__(self):
# #         return f'<CartItem User ID {self.user_id} Book ID {self.book_id} Quantity {self.quantity}>'

# # class Sale(db.Model, SerializerMixin):
# #     __tablename__ = 'sales'
# #     serialize_rules = ('-user.sales', '-book.sales')

# #     id = db.Column(db.Integer, primary_key=True)
# #     user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
# #     book_id = db.Column(db.Integer, db.ForeignKey('store_books.id'), nullable=False)
# #     date_of_sale = db.Column(db.Date, nullable=False, default=datetime.utcnow)
# #     quantity = db.Column(db.Integer, nullable=False)
# #     total_price = db.Column(db.Float, nullable=False)
# #     status = db.Column(db.String, default='Pending')

# #     # Relationships
# #     user = relationship('User', back_populates='sales')
# #     book = relationship('StoreBook', back_populates='sales')

# #     def __repr__(self):
# #         return f'<Sale Book ID {self.book_id} to User ID {self.user_id}>'

# # class Borrowing(db.Model, SerializerMixin):
# #     __tablename__ = 'borrowings'
# #     serialize_rules = ('-user.borrowings', '-book.borrowings')

# #     id = db.Column(db.Integer, primary_key=True)
# #     user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
# #     book_id = db.Column(db.Integer, db.ForeignKey('library_books.id'), nullable=False)
# #     date_borrowed = db.Column(db.Date, nullable=False, default=datetime.utcnow)
# #     due_date = db.Column(db.Date, nullable=False, default=lambda: datetime.utcnow() + timedelta(days=70))
# #     date_returned = db.Column(db.Date)
# #     status = db.Column(db.String, default='Pending')

# #     # Relationships
# #     user = relationship('User', back_populates='borrowings')
# #     book = relationship('LibraryBook', back_populates='borrowings')

# #     def __repr__(self):
# #         return f'<Borrowing Book ID {self.book_id} by User ID {self.user_id}>'






















# # from sqlalchemy.ext.associationproxy import association_proxy
# # from sqlalchemy.orm import validates, relationship
# # from config import db
# # from sqlalchemy import MetaData, Table, ForeignKey
# # from sqlalchemy_serializer import SerializerMixin
# # from flask_bcrypt import Bcrypt
# # import re
# # from datetime import datetime, timedelta

# # bcrypt = Bcrypt()
# # metadata = MetaData()

# # # Association Tables
# # cart_items_association = Table('cart_items_association', db.Model.metadata,
# #     db.Column('user_id', db.Integer, db.ForeignKey('users.id'), primary_key=True),
# #     db.Column('book_id', db.Integer, db.ForeignKey('store_books.id'), primary_key=True),
# #     db.Column('quantity', db.Integer, nullable=False)
# # )

# # borrowings_association = Table('borrowings_association', db.Model.metadata,
# #     db.Column('user_id', db.Integer, db.ForeignKey('users.id'), primary_key=True),
# #     db.Column('book_id', db.Integer, db.ForeignKey('library_books.id'), primary_key=True),
# #     db.Column('date_borrowed', db.Date, default=datetime.utcnow),
# #     db.Column('due_date', db.Date, default=lambda: datetime.utcnow() + timedelta(days=70)),
# #     db.Column('date_returned', db.Date),
# #     db.Column('status', db.String, default='Pending')
# # )

# # # Models
# # class User(db.Model, SerializerMixin):
# #     __tablename__ = 'users'
# #     serialize_rules = ('-password_hash', '-borrowings.user', '-sales.user', '-cart_items.user')

# #     id = db.Column(db.Integer, primary_key=True)
# #     name = db.Column(db.String, nullable=False)
# #     email = db.Column(db.String, unique=True, nullable=False)
# #     password_hash = db.Column(db.String, nullable=False)
# #     is_admin = db.Column(db.Boolean, default=False)

# #     # Relationships
# #     borrowings = relationship('Borrowing', back_populates='user', cascade='all, delete-orphan', lazy='joined')
# #     sales = relationship('Sale', back_populates='user', cascade='all, delete-orphan', lazy='joined')
# #     cart_items = relationship('CartItem', back_populates='user', cascade='all, delete-orphan', lazy='joined')

# #     @validates('email')
# #     def validate_email(self, key, email):
# #         valid_email = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
# #         if not re.match(valid_email, email):
# #             raise ValueError("Invalid email")
# #         return email

# #     def set_password(self, password):
# #         self.password_hash = bcrypt.generate_password_hash(password).decode('utf-8')

# #     def check_password(self, password):
# #         return bcrypt.check_password_hash(self.password_hash, password)

# #     def __repr__(self):
# #         return f'<User {self.name}, Email: {self.email}>'

# # class StoreBook(db.Model, SerializerMixin):
# #     __tablename__ = 'store_books'
# #     serialize_rules = ('-cart_items.book', '-sales.book')

# #     id = db.Column(db.Integer, primary_key=True)
# #     title = db.Column(db.String, nullable=False)
# #     author = db.Column(db.String, nullable=False)
# #     genre = db.Column(db.String, nullable=False)
# #     isbn = db.Column(db.String, unique=True, nullable=False)
# #     price = db.Column(db.Float, nullable=False)
# #     stock = db.Column(db.Integer, default=0)
# #     image_url = db.Column(db.String, nullable=True)

# #     # Relationships
# #     cart_items = relationship('CartItem', back_populates='book', cascade='all, delete-orphan', lazy='joined')
# #     sales = relationship('Sale', back_populates='book', cascade='all, delete-orphan', lazy='joined')

# #     def __repr__(self):
# #         return f'<StoreBook {self.title} by {self.author}>'

# # class LibraryBook(db.Model, SerializerMixin):
# #     __tablename__ = 'library_books'
# #     serialize_rules = ('-borrowings.book',)

# #     id = db.Column(db.Integer, primary_key=True)
# #     title = db.Column(db.String, nullable=False)
# #     author = db.Column(db.String, nullable=False)
# #     genre = db.Column(db.String, nullable=False)
# #     isbn = db.Column(db.String, unique=True, nullable=False)
# #     available_copies = db.Column(db.Integer, default=0)
# #     total_copies = db.Column(db.Integer, default=0)
# #     image_url = db.Column(db.String, nullable=True)

# #     # Relationships
# #     borrowings = relationship('Borrowing', back_populates='book', cascade='all, delete-orphan', lazy='joined')

# #     def __repr__(self):
# #         return f'<LibraryBook {self.title} by {self.author}>'

# # class CartItem(db.Model, SerializerMixin):
# #     __tablename__ = 'cart_items'
# #     serialize_rules = ('-user.cart_items', '-book.cart_items')

# #     id = db.Column(db.Integer, primary_key=True)
# #     user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
# #     book_id = db.Column(db.Integer, db.ForeignKey('store_books.id'), nullable=False)
# #     quantity = db.Column(db.Integer, nullable=False)

# #     # Relationships
# #     user = relationship('User', back_populates='cart_items')
# #     book = relationship('StoreBook', back_populates='cart_items')

# #     def __repr__(self):
# #         return f'<CartItem User ID {self.user_id} Book ID {self.book_id} Quantity {self.quantity}>'

# # class Sale(db.Model, SerializerMixin):
# #     __tablename__ = 'sales'
# #     serialize_rules = ('-user.sales', '-book.sales')

# #     id = db.Column(db.Integer, primary_key=True)
# #     user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
# #     book_id = db.Column(db.Integer, db.ForeignKey('store_books.id'), nullable=False)
# #     date_of_sale = db.Column(db.Date, nullable=False, default=datetime.utcnow)
# #     quantity = db.Column(db.Integer, nullable=False)
# #     total_price = db.Column(db.Float, nullable=False)
# #     status = db.Column(db.String, default='Pending')

# #     # Relationships
# #     user = relationship('User', back_populates='sales')
# #     book = relationship('StoreBook', back_populates='sales')

# #     def __repr__(self):
# #         return f'<Sale Book ID {self.book_id} to User ID {self.user_id}>'

# # class Borrowing(db.Model, SerializerMixin):
# #     __tablename__ = 'borrowings'
# #     serialize_rules = ('-user.borrowings', '-book.borrowings')

# #     id = db.Column(db.Integer, primary_key=True)
# #     user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
# #     book_id = db.Column(db.Integer, db.ForeignKey('library_books.id'), nullable=False)
# #     date_borrowed = db.Column(db.Date, nullable=False, default=datetime.utcnow)
# #     due_date = db.Column(db.Date, nullable=False, default=lambda: datetime.utcnow() + timedelta(days=70))
# #     date_returned = db.Column(db.Date)
# #     status = db.Column(db.String, default='Pending')

# #     # Relationships
# #     user = relationship('User', back_populates='borrowings')
# #     book = relationship('LibraryBook', back_populates='borrowings')

# #     def __repr__(self):
# #         return f'<Borrowing Book ID {self.book_id} by User ID {self.user_id}>'


# # from sqlalchemy.ext.associationproxy import association_proxy
# # from sqlalchemy.orm import validates, relationship
# # from config import db
# # from sqlalchemy import MetaData, Table, ForeignKey
# # from sqlalchemy_serializer import SerializerMixin
# # from flask_bcrypt import Bcrypt
# # import re
# # from datetime import datetime, timedelta

# # bcrypt = Bcrypt()
# # metadata = MetaData()

# # # Association Tables
# # cart_items_association = Table('cart_items_association', db.Model.metadata,
# #     db.Column('user_id', db.Integer, db.ForeignKey('users.id'), primary_key=True),
# #     db.Column('book_id', db.Integer, db.ForeignKey('store_books.id'), primary_key=True),
# #     db.Column('quantity', db.Integer, nullable=False)
# # )

# # borrowings_association = Table('borrowings_association', db.Model.metadata,
# #     db.Column('user_id', db.Integer, db.ForeignKey('users.id'), primary_key=True),
# #     db.Column('book_id', db.Integer, db.ForeignKey('library_books.id'), primary_key=True),
# #     db.Column('date_borrowed', db.Date, default=datetime.utcnow),
# #     db.Column('due_date', db.Date, default=lambda: datetime.utcnow() + timedelta(days=70)),
# #     db.Column('date_returned', db.Date),
# #     db.Column('status', db.String, default='Pending')
# # )

# # # Models
# # class User(db.Model, SerializerMixin):
# #     __tablename__ = 'users'
# #     serialize_rules = ('-password_hash', '-borrowings.user', '-sales.user', '-cart_items.user')

# #     id = db.Column(db.Integer, primary_key=True)
# #     name = db.Column(db.String, nullable=False)
# #     email = db.Column(db.String, unique=True, nullable=False)
# #     password_hash = db.Column(db.String, nullable=False)
# #     is_admin = db.Column(db.Boolean, default=False)
# #     profile_image = db.Column(db.String, nullable=True)

# #     borrowings = relationship('Borrowing', back_populates='user', cascade='all, delete-orphan', lazy='selectin')
# #     sales = relationship('Sale', back_populates='user', cascade='all, delete-orphan', lazy='selectin')
# #     cart_items = relationship('CartItem', back_populates='user', cascade='all, delete-orphan', lazy='selectin')

# #     @validates('email')
# #     def validate_email(self, key, email):
# #         valid_email = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
# #         if not re.match(valid_email, email):
# #             raise ValueError("Invalid email")
# #         return email

# #     def set_password(self, password):
# #         self.password_hash = bcrypt.generate_password_hash(password).decode('utf-8')

# #     def check_password(self, password):
# #         return bcrypt.check_password_hash(self.password_hash, password)

# #     def __repr__(self):
# #         return f'<User {self.name}, Email: {self.email}>'


# # class StoreBook(db.Model, SerializerMixin):
# #     __tablename__ = 'store_books'
# #     serialize_rules = ('-cart_items.book', '-sales.book')

# #     id = db.Column(db.Integer, primary_key=True)
# #     title = db.Column(db.String, nullable=False)
# #     author = db.Column(db.String, nullable=False)
# #     genre = db.Column(db.String, nullable=False)
# #     isbn = db.Column(db.String, unique=True, nullable=False)
# #     price = db.Column(db.Float, nullable=False)
# #     stock = db.Column(db.Integer, default=0)
# #     image_url = db.Column(db.String, nullable=True)

# #     cart_items = relationship('CartItem', back_populates='book', cascade='all, delete-orphan', lazy='selectin')
# #     sales = relationship('Sale', back_populates='book', cascade='all, delete-orphan', lazy='selectin')

# #     def __repr__(self):
# #         return f'<StoreBook {self.title} by {self.author}>'


# # class LibraryBook(db.Model, SerializerMixin):
# #     __tablename__ = 'library_books'
# #     serialize_rules = ('-borrowings.book',)

# #     id = db.Column(db.Integer, primary_key=True)
# #     title = db.Column(db.String, nullable=False)
# #     author = db.Column(db.String, nullable=False)
# #     genre = db.Column(db.String, nullable=False)
# #     isbn = db.Column(db.String, unique=True, nullable=False)
# #     available_copies = db.Column(db.Integer, default=0)
# #     total_copies = db.Column(db.Integer, default=0)
# #     image_url = db.Column(db.String, nullable=True)

# #     borrowings = relationship('Borrowing', back_populates='book', cascade='all, delete-orphan', lazy='selectin')

# #     def __repr__(self):
# #         return f'<LibraryBook {self.title} by {self.author}>'


# # class CartItem(db.Model, SerializerMixin):
# #     __tablename__ = 'cart_items'
# #     serialize_rules = ('-user.cart_items', '-book.cart_items')

# #     id = db.Column(db.Integer, primary_key=True)
# #     user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
# #     book_id = db.Column(db.Integer, db.ForeignKey('store_books.id'), nullable=False)
# #     quantity = db.Column(db.Integer, nullable=False)

# #     user = relationship('User', back_populates='cart_items')
# #     book = relationship('StoreBook', back_populates='cart_items')

# #     def __repr__(self):
# #         return f'<CartItem User ID {self.user_id} Book ID {self.book_id} Quantity {self.quantity}>'


# # class Sale(db.Model, SerializerMixin):
# #     __tablename__ = 'sales'
# #     serialize_rules = ('-user.sales', '-book.sales')

# #     id = db.Column(db.Integer, primary_key=True)
# #     user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
# #     book_id = db.Column(db.Integer, db.ForeignKey('store_books.id'), nullable=False)
# #     date_of_sale = db.Column(db.Date, nullable=False, default=datetime.utcnow)
# #     quantity = db.Column(db.Integer, nullable=False)
# #     total_price = db.Column(db.Float, nullable=False)
# #     status = db.Column(db.String, default='Pending')

# #     user = relationship('User', back_populates='sales')
# #     book = relationship('StoreBook', back_populates='sales')

# #     def __repr__(self):
# #         return f'<Sale Book ID {self.book_id} to User ID {self.user_id}>'


# # class Borrowing(db.Model, SerializerMixin):
# #     __tablename__ = 'borrowings'
# #     serialize_rules = ('-user.borrowings', '-book.borrowings')

# #     id = db.Column(db.Integer, primary_key=True)
# #     user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
# #     book_id = db.Column(db.Integer, db.ForeignKey('library_books.id'), nullable=False)
# #     date_borrowed = db.Column(db.Date, nullable=False, default=datetime.utcnow)
# #     due_date = db.Column(db.Date, nullable=False, default=lambda: datetime.utcnow() + timedelta(days=70))
# #     date_returned = db.Column(db.Date)
# #     status = db.Column(db.String, default='Pending')

# #     user = relationship('User', back_populates='borrowings')
# #     book = relationship('LibraryBook', back_populates='borrowings')

# #     def __repr__(self):
# #         return f'<Borrowing Book ID {self.book_id} by User ID {self.user_id}>'


# from sqlalchemy.ext.associationproxy import association_proxy
# from sqlalchemy.orm import validates, relationship
# from config import db
# from sqlalchemy import MetaData, Table, ForeignKey
# from sqlalchemy_serializer import SerializerMixin
# from flask_bcrypt import Bcrypt
# import re
# from datetime import datetime, timedelta

# bcrypt = Bcrypt()
# metadata = MetaData()

# # Association Tables
# cart_items_association = Table(
#     'cart_items_association', db.Model.metadata,
#     db.Column('user_id', db.Integer, db.ForeignKey('users.id'), primary_key=True),
#     db.Column('book_id', db.Integer, db.ForeignKey('store_books.id'), primary_key=True),
#     db.Column('quantity', db.Integer, nullable=False)
# )

# borrowings_association = Table(
#     'borrowings_association', db.Model.metadata,
#     db.Column('user_id', db.Integer, db.ForeignKey('users.id'), primary_key=True),
#     db.Column('book_id', db.Integer, db.ForeignKey('library_books.id'), primary_key=True),
#     db.Column('date_borrowed', db.Date, default=datetime.utcnow),
#     db.Column('due_date', db.Date, default=lambda: datetime.utcnow() + timedelta(days=70)),
#     db.Column('date_returned', db.Date),
#     db.Column('status', db.String, default='Pending')
# )

# # Models
# class User(db.Model, SerializerMixin):
#     __tablename__ = 'users'
#     serialize_rules = ('-password_hash', '-borrowings.user', '-sales.user', '-cart_items.user')

#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String, nullable=False)
#     email = db.Column(db.String, unique=True, nullable=False)
#     password_hash = db.Column(db.String, nullable=False)
#     is_admin = db.Column(db.Boolean, default=False)
#     profile_image = db.Column(db.String, nullable=True)

#     borrowings = relationship('Borrowing', back_populates='user', cascade='all, delete-orphan', lazy='select')
#     sales = relationship('Sale', back_populates='user', cascade='all, delete-orphan', lazy='select')
#     cart_items = relationship('CartItem', back_populates='user', cascade='all, delete-orphan', lazy='select')

#     @validates('email')
#     def validate_email(self, key, email):
#         valid_email = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
#         if not re.match(valid_email, email):
#             raise ValueError("Invalid email")
#         return email

#     def set_password(self, password):
#         self.password_hash = bcrypt.generate_password_hash(password).decode('utf-8')

#     def check_password(self, password):
#         return bcrypt.check_password_hash(self.password_hash, password)

#     def __repr__(self):
#         return f'<User {self.name}, Email: {self.email}>'


# class StoreBook(db.Model, SerializerMixin):
#     __tablename__ = 'store_books'
#     serialize_rules = ('-cart_items.book', '-sales.book')

#     id = db.Column(db.Integer, primary_key=True)
#     title = db.Column(db.String, nullable=False)
#     author = db.Column(db.String, nullable=False)
#     genre = db.Column(db.String, nullable=False)
#     isbn = db.Column(db.String, unique=True, nullable=False)
#     price = db.Column(db.Float, nullable=False)
#     stock = db.Column(db.Integer, default=0)
#     image_url = db.Column(db.String, nullable=True)

#     cart_items = relationship('CartItem', back_populates='book', cascade='all, delete-orphan', lazy='select')
#     sales = relationship('Sale', back_populates='book', cascade='all, delete-orphan', lazy='select')

#     def __repr__(self):
#         return f'<StoreBook {self.title} by {self.author}>'


# class LibraryBook(db.Model, SerializerMixin):
#     __tablename__ = 'library_books'
#     serialize_rules = ('-borrowings.book',)

#     id = db.Column(db.Integer, primary_key=True)
#     title = db.Column(db.String, nullable=False)
#     author = db.Column(db.String, nullable=False)
#     genre = db.Column(db.String, nullable=False)
#     isbn = db.Column(db.String, unique=True, nullable=False)
#     available_copies = db.Column(db.Integer, default=0)
#     total_copies = db.Column(db.Integer, default=0)
#     image_url = db.Column(db.String, nullable=True)

#     borrowings = relationship('Borrowing', back_populates='book', cascade='all, delete-orphan', lazy='select')

#     def __repr__(self):
#         return f'<LibraryBook {self.title} by {self.author}>'


# class CartItem(db.Model, SerializerMixin):
#     __tablename__ = 'cart_items'
#     serialize_rules = ('-user.cart_items', '-book.cart_items')

#     id = db.Column(db.Integer, primary_key=True)
#     user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
#     book_id = db.Column(db.Integer, db.ForeignKey('store_books.id'), nullable=False)
#     quantity = db.Column(db.Integer, nullable=False)

#     user = relationship('User', back_populates='cart_items')
#     book = relationship('StoreBook', back_populates='cart_items')

#     def __repr__(self):
#         return f'<CartItem User ID {self.user_id} Book ID {self.book_id} Quantity {self.quantity}>'


# class Sale(db.Model, SerializerMixin):
#     __tablename__ = 'sales'
#     serialize_rules = ('-user.sales', '-book.sales')

#     id = db.Column(db.Integer, primary_key=True)
#     user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
#     book_id = db.Column(db.Integer, db.ForeignKey('store_books.id'), nullable=False)
#     date_of_sale = db.Column(db.Date, nullable=False, default=datetime.utcnow)
#     quantity = db.Column(db.Integer, nullable=False)
#     total_price = db.Column(db.Float, nullable=False)
#     status = db.Column(db.String, default='Pending')

#     user = relationship('User', back_populates='sales')
#     book = relationship('StoreBook', back_populates='sales')

#     def __repr__(self):
#         return f'<Sale Book ID {self.book_id} to User ID {self.user_id}>'


# class Borrowing(db.Model, SerializerMixin):
#     __tablename__ = 'borrowings'
#     serialize_rules = ('-user.borrowings', '-book.borrowings')

#     id = db.Column(db.Integer, primary_key=True)
#     user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
#     book_id = db.Column(db.Integer, db.ForeignKey('library_books.id'), nullable=False)
#     date_borrowed = db.Column(db.Date, nullable=False, default=datetime.utcnow)
#     due_date = db.Column(db.Date, nullable=False, default=lambda: datetime.utcnow() + timedelta(days=70))
#     date_returned = db.Column(db.Date)
#     status = db.Column(db.String, default='Pending')

#     user = relationship('User', back_populates='borrowings')
#     book = relationship('LibraryBook', back_populates='borrowings')

#     def __repr__(self):
#         return f'<Borrowing Book ID {self.book_id} by User ID {self.user_id}>'


# class Transaction(db.Model):
#     __tablename__ = 'transactions'

#     id = db.Column(db.String(100), primary_key=True)
#     status = db.Column(db.String(20), nullable=False, default="Pending")
#     amount = db.Column(db.Float, nullable=False)
#     phone_number = db.Column(db.String(15), nullable=False)

#     def __repr__(self):
#         return f'<Transaction ID {self.id} Status {self.status} Amount {self.amount}>'


from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy.orm import validates, relationship
from config import db
from sqlalchemy import MetaData, Table, ForeignKey
from sqlalchemy_serializer import SerializerMixin
from flask_bcrypt import Bcrypt
import re
from datetime import datetime, timedelta

bcrypt = Bcrypt()
metadata = MetaData()

# Association Tables
cart_items_association = Table(
    'cart_items_association', db.Model.metadata,
    db.Column('user_id', db.Integer, db.ForeignKey('users.id'), primary_key=True),
    db.Column('book_id', db.Integer, db.ForeignKey('store_books.id'), primary_key=True),
    db.Column('quantity', db.Integer, nullable=False)
)

borrowings_association = Table(
    'borrowings_association', db.Model.metadata,
    db.Column('user_id', db.Integer, db.ForeignKey('users.id'), primary_key=True),
    db.Column('book_id', db.Integer, db.ForeignKey('library_books.id'), primary_key=True),
    db.Column('date_borrowed', db.Date, default=datetime.utcnow),
    db.Column('due_date', db.Date, default=lambda: datetime.utcnow() + timedelta(days=70)),
    db.Column('date_returned', db.Date),
    db.Column('status', db.String, default='Pending')
)

# Models
class User(db.Model, SerializerMixin):
    __tablename__ = 'users'
    serialize_rules = (
        '-password_hash', '-borrowings.user', '-sales.user', '-cart_items.user',
        '-borrowings.book.borrowings', '-sales.book.sales', '-cart_items.book.cart_items'
    )

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    email = db.Column(db.String, unique=True, nullable=False)
    password_hash = db.Column(db.String, nullable=False)
    is_admin = db.Column(db.Boolean, default=False)
    profile_image = db.Column(db.String, nullable=True)

    borrowings = relationship('Borrowing', back_populates='user', cascade='all, delete-orphan', lazy='select')
    sales = relationship('Sale', back_populates='user', cascade='all, delete-orphan', lazy='select')
    cart_items = relationship('CartItem', back_populates='user', cascade='all, delete-orphan', lazy='select')

    @validates('email')
    def validate_email(self, key, email):
        valid_email = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
        if not re.match(valid_email, email):
            raise ValueError("Invalid email")
        return email

    def set_password(self, password):
        self.password_hash = bcrypt.generate_password_hash(password).decode('utf-8')

    def check_password(self, password):
        return bcrypt.check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f'<User {self.name}, Email: {self.email}>'


class StoreBook(db.Model, SerializerMixin):
    __tablename__ = 'store_books'
    serialize_rules = ('-cart_items.book', '-sales.book', '-cart_items.user.cart_items', '-sales.user.sales')

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    author = db.Column(db.String, nullable=False)
    genre = db.Column(db.String, nullable=False)
    isbn = db.Column(db.String, unique=True, nullable=False)
    price = db.Column(db.Float, nullable=False)
    stock = db.Column(db.Integer, default=0)
    image_url = db.Column(db.String, nullable=True)

    cart_items = relationship('CartItem', back_populates='book', cascade='all, delete-orphan', lazy='select')
    sales = relationship('Sale', back_populates='book', cascade='all, delete-orphan', lazy='select')

    def __repr__(self):
        return f'<StoreBook {self.title} by {self.author}>'


class LibraryBook(db.Model, SerializerMixin):
    __tablename__ = 'library_books'
    serialize_rules = ('-borrowings.book', '-borrowings.user.borrowings')

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    author = db.Column(db.String, nullable=False)
    genre = db.Column(db.String, nullable=False)
    isbn = db.Column(db.String, unique=True, nullable=False)
    available_copies = db.Column(db.Integer, default=0)
    total_copies = db.Column(db.Integer, default=0)
    image_url = db.Column(db.String, nullable=True)

    borrowings = relationship('Borrowing', back_populates='book', cascade='all, delete-orphan', lazy='select')

    def __repr__(self):
        return f'<LibraryBook {self.title} by {self.author}>'


class CartItem(db.Model, SerializerMixin):
    __tablename__ = 'cart_items'
    serialize_rules = ('-user.cart_items', '-book.cart_items', '-user.borrowings', '-book.sales')

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    book_id = db.Column(db.Integer, db.ForeignKey('store_books.id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)

    user = relationship('User', back_populates='cart_items')
    book = relationship('StoreBook', back_populates='cart_items')

    def __repr__(self):
        return f'<CartItem User ID {self.user_id} Book ID {self.book_id} Quantity {self.quantity}>'


class Sale(db.Model, SerializerMixin):
    __tablename__ = 'sales'
    serialize_rules = ('-user.sales', '-book.sales', '-user.cart_items', '-book.cart_items')

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    book_id = db.Column(db.Integer, db.ForeignKey('store_books.id'), nullable=False)
    date_of_sale = db.Column(db.Date, nullable=False, default=datetime.utcnow)
    quantity = db.Column(db.Integer, nullable=False)
    total_price = db.Column(db.Float, nullable=False)
    status = db.Column(db.String, default='Pending')

    user = relationship('User', back_populates='sales')
    book = relationship('StoreBook', back_populates='sales')

    def __repr__(self):
        return f'<Sale Book ID {self.book_id} to User ID {self.user_id}>'


class Borrowing(db.Model, SerializerMixin):
    __tablename__ = 'borrowings'
    serialize_rules = ('-user.borrowings', '-book.borrowings', '-user.cart_items', '-book.sales')

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    book_id = db.Column(db.Integer, db.ForeignKey('library_books.id'), nullable=False)
    date_borrowed = db.Column(db.Date, nullable=False, default=datetime.utcnow)
    due_date = db.Column(db.Date, nullable=False, default=lambda: datetime.utcnow() + timedelta(days=70))
    date_returned = db.Column(db.Date)
    status = db.Column(db.String, default='Pending')

    user = relationship('User', back_populates='borrowings')
    book = relationship('LibraryBook', back_populates='borrowings')

    def __repr__(self):
        return f'<Borrowing Book ID {self.book_id} by User ID {self.user_id}>'


# class Transaction(db.Model, SerializerMixin):
#     __tablename__ = 'transactions'
#     serialize_rules = ('-user.transactions',)

#     id = db.Column(db.String(100), primary_key=True)
#     sale_id = db.Column(db.Integer, db.ForeignKey('sales.id'), nullable=False)
#     status = db.Column(db.String(20), nullable=False, default="Pending")
#     amount = db.Column(db.Float, nullable=False)
#     phone_number = db.Column(db.String(15), nullable=False)


#     def __repr__(self):
#         return f'<Transaction ID {self.id} Status {self.status} Amount {self.amount}>'
