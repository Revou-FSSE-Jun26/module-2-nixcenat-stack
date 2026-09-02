from flask import Blueprint, jsonify
from app.models import Product, Category, User, Order

main = Blueprint("main", __name__)


@main.route("/api")
def api():
    return jsonify({
        "message": "RevoShop API is running",
        "status": "success"
    })


@main.route("/products")
def products():
    products = Product.query.all()

    return jsonify([
        {
            "id": product.id,
            "name": product.name,
            "description": product.description,
            "price": float(product.price),
            "stock": product.stock,
            "category_id": product.category_id
        }
        for product in products
    ])


@main.route("/categories")
def categories():
    categories = Category.query.all()

    return jsonify([
        {
            "id": category.id,
            "name": category.name
        }
        for category in categories
    ])


@main.route("/users")
def users():
    users = User.query.all()

    return jsonify([
        {
            "id": user.id,
            "name": user.name,
            "email": user.email,
            "created_at": user.created_at.isoformat()
        }
        for user in users
    ])


@main.route("/orders")
def orders():
    orders = Order.query.all()

    return jsonify([
        {
            "id": order.id,
            "user_id": order.user_id,
            "total": float(order.total),
            "status": order.status,
            "created_at": order.created_at.isoformat(),
            "items": [
                {
                    "product_id": item.product_id,
                    "quantity": item.quantity,
                    "price": float(item.price)
                }
                for item in order.order_items
            ]
        }
        for order in orders
    ])
