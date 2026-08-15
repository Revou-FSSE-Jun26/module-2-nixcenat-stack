from datetime import datetime
from app.database import db

# Association Table / Junction Table Many-to-Many
order_items = db.Table(
    'order_items',
    db.Column('order_item_id', db.Integer, primary_key=True),
    db.Column('order_id', db.Integer, db.ForeignKey('orders.order_id', ondelete='CASCADE'), nullable=False),
    db.Column('product_id', db.Integer, db.ForeignKey('products.product_id', ondelete='RESTRICT'), nullable=False),
    db.Column('quantity', db.Integer, nullable=False),
    db.Column('unit_price', db.Numeric(10, 2), nullable=False)
)

class User(db.Model):
    __tablename__ = 'users'

    user_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), nullable=False, unique=True)
    email = db.Column(db.String(100), nullable=False, unique=True)
    password_hash = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime(timezone=True), default=datetime.utcnow)
    
    # Kolom role yang sudah dipindahkan ke class User
    role = db.Column(db.String(20), nullable=False, server_default='customer')

    orders = db.relationship('Order', backref='user', lazy=True)

class Category(db.Model):
    __tablename__ = 'categories'

    category_id = db.Column(db.Integer, primary_key=True)
    category_name = db.Column(db.String(100), nullable=False, unique=True)
    description = db.Column(db.Text)

    products = db.relationship('Product', backref='category', lazy=True)

class Product(db.Model):
    __tablename__ = 'products'

    product_id = db.Column(db.Integer, primary_key=True)
    category_id = db.Column(db.Integer, db.ForeignKey('categories.category_id'), nullable=False)
    product_name = db.Column(db.String(150), nullable=False)
    description = db.Column(db.Text)
    price = db.Column(db.Numeric(10, 2), nullable=False)
    stock_quantity = db.Column(db.Integer, nullable=False, default=0)
    created_at = db.Column(db.DateTime(timezone=True), default=datetime.utcnow)

class Order(db.Model):
    __tablename__ = 'orders'

    order_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    order_date = db.Column(db.DateTime(timezone=True), default=datetime.utcnow)
    total_amount = db.Column(db.Numeric(10, 2), nullable=False, default=0.00)
    status = db.Column(db.String(30), nullable=False, default='pending')

    products = db.relationship('Product', secondary=order_items, backref='orders', lazy=True)
    
