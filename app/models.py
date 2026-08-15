from datetime import datetime, timezone
from app import db

order_items = db.Table(
    "order_items",
    db.Column("order_item_id", db.Integer, primary_key=True),
    db.Column("order_id", db.Integer, db.ForeignKey("orders.order_id", ondelete="CASCADE"), nullable=False),
    db.Column("product_id", db.Integer, db.ForeignKey("products.product_id", ondelete="RESTRICT"), nullable=False),
    db.Column("quantity", db.Integer, nullable=False, default=1),
    db.Column("unit_price", db.Numeric(10, 2), nullable=False)
)

class User(db.Model):
    __tablename__ = "users"
    user_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(20), nullable=False, server_default="customer")
    created_at = db.Column(db.DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    orders = db.relationship("Order", backref="user", lazy=True)

class Category(db.Model):
    __tablename__ = "categories"
    category_id = db.Column(db.Integer, primary_key=True)
    category_name = db.Column(db.String(100), unique=True, nullable=False)
    description = db.Column(db.Text)
    products = db.relationship("Product", backref="category", lazy=True)

class Product(db.Model):
    __tablename__ = "products"
    product_id = db.Column(db.Integer, primary_key=True)
    category_id = db.Column(db.Integer, db.ForeignKey("categories.category_id", ondelete="RESTRICT"), nullable=False)
    product_name = db.Column(db.String(150), nullable=False)
    description = db.Column(db.Text)
    price = db.Column(db.Numeric(10, 2), nullable=False)
    stock_quantity = db.Column(db.Integer, nullable=False, default=0)
    created_at = db.Column(db.DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

class Order(db.Model):
    __tablename__ = "orders"
    order_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.user_id", ondelete="CASCADE"), nullable=False)
    order_date = db.Column(db.DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    total_amount = db.Column(db.Numeric(10, 2), nullable=False, default=0.00)
    status = db.Column(db.String(30), nullable=False, default="pending")
    products = db.relationship("Product", secondary=order_items, backref=db.backref("orders", lazy=True))
