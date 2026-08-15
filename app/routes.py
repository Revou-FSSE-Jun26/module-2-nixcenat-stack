from flask import Blueprint, jsonify, request
from app import db
from app.models import User

main_bp = Blueprint("main", __name__)

HARDCODED_PRODUCTS = [
    {"id": 1, "name": "Wireless Mechanical Keyboard", "description": "RGB tactile switch keyboard", "price": 89.99, "stock_quantity": 45},
    {"id": 2, "name": "Ergonomic Gaming Mouse", "description": "High precision 26K DPI optical sensor", "price": 49.99, "stock_quantity": 120},
    {"id": 3, "name": "Cotton Hoodie", "description": "100% organic heavy fleece sweater", "price": 39.50, "stock_quantity": 200}
]

@main_bp.route("/products", methods=["GET"])
def get_products():
    return jsonify(HARDCODED_PRODUCTS), 200

@main_bp.route("/products/<int:product_id>", methods=["GET"])
def get_product(product_id):
    product = next((p for p in HARDCODED_PRODUCTS if p["id"] == product_id), None)
    if product is None:
        return jsonify({"error": "Product not found"}), 404
    return jsonify(product), 200

@main_bp.route("/register", methods=["POST"])
def register():
    data = request.get_json() or {}
    if not data.get("username") or not data.get("email") or not data.get("password_hash"):
        return jsonify({"error": "Missing required fields"}), 400

    existing_user = User.query.filter(
        (User.username == data["username"]) | (User.email == data["email"])
    ).first()
    if existing_user:
        return jsonify({"error": "Username or email already exists"}), 400

    new_user = User(
        username=data["username"],
        email=data["email"],
        password_hash=data["password_hash"],
        role=data.get("role", "customer")
    )
    db.session.add(new_user)
    db.session.commit()

    return jsonify({
        "message": "User registered successfully",
        "user": {
            "user_id": new_user.user_id,
            "username": new_user.username,
            "email": new_user.email,
            "role": new_user.role
        }
    }), 201

@main_bp.route("/users/<int:user_id>", methods=["GET"])
def get_user(user_id):
    user = User.query.get(user_id)
    if user is None:
        return jsonify({"error": "User not found"}), 404
    return jsonify({
        "user_id": user.user_id,
        "username": user.username,
        "email": user.email,
        "role": user.role
    }), 200
