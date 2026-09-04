from flask import Blueprint, jsonify, request
from app import db
from app.models import Product, Category, User, Order, OrderItem
from werkzeug.security import generate_password_hash, check_password_hash

main = Blueprint("main", __name__)


# =========================
# API
# =========================

@main.route("/api", methods=["GET"])
def api():
    return jsonify({
        "message": "RevoShop API is running",
        "status": "success"
    }), 200


# =========================
# PRODUCTS
# =========================

@main.route("/products", methods=["GET"])
def products():
    products = Product.query.all()

    return jsonify([
        product.to_dict()
        for product in products
    ]), 200


@main.route("/products/<int:id>", methods=["GET"])
def get_product(id):
    product = Product.query.get(id)

    if not product:
        return jsonify({
            "message": "Product not found"
        }), 404

    return jsonify(product.to_dict()), 200


@main.route("/products", methods=["POST"])
def create_product():
    data = request.get_json()

    if not data:
        return jsonify({
            "message": "Request body is required"
        }), 400

    required_fields = [
        "name",
        "price",
        "stock",
        "category_id"
    ]

    for field in required_fields:
        if field not in data:
            return jsonify({
                "message": f"{field} is required"
            }), 400

    if not isinstance(data["name"], str) or not data["name"].strip():
        return jsonify({
            "message": "Name must be a non-empty string"
        }), 400

    try:
        price = float(data["price"])
    except (TypeError, ValueError):
        return jsonify({
            "message": "Price must be a valid number"
        }), 400

    if price < 0:
        return jsonify({
            "message": "Price cannot be negative"
        }), 400

    try:
        stock = int(data["stock"])
    except (TypeError, ValueError):
        return jsonify({
            "message": "Stock must be a valid integer"
        }), 400

    if stock < 0:
        return jsonify({
            "message": "Stock cannot be negative"
        }), 400

    category = Category.query.get(data["category_id"])

    if not category:
        return jsonify({
            "message": "Category not found"
        }), 404

    product = Product(
        name=data["name"].strip(),
        description=data.get("description"),
        price=price,
        stock=stock,
        category_id=category.id
    )

    db.session.add(product)
    db.session.commit()

    return jsonify(product.to_dict()), 201


@main.route("/products/<int:id>", methods=["PUT"])
def update_product(id):
    product = Product.query.get(id)

    if not product:
        return jsonify({
            "message": "Product not found"
        }), 404

    data = request.get_json()

    if not data:
        return jsonify({
            "message": "Request body is required"
        }), 400

    if "name" in data:
        if not isinstance(data["name"], str) or not data["name"].strip():
            return jsonify({
                "message": "Name must be a non-empty string"
            }), 400

        product.name = data["name"].strip()

    if "description" in data:
        product.description = data["description"]

    if "price" in data:
        try:
            price = float(data["price"])
        except (TypeError, ValueError):
            return jsonify({
                "message": "Price must be a valid number"
            }), 400

        if price < 0:
            return jsonify({
                "message": "Price cannot be negative"
            }), 400

        product.price = price

    if "stock" in data:
        try:
            stock = int(data["stock"])
        except (TypeError, ValueError):
            return jsonify({
                "message": "Stock must be a valid integer"
            }), 400

        if stock < 0:
            return jsonify({
                "message": "Stock cannot be negative"
            }), 400

        product.stock = stock

    if "category_id" in data:
        category = Category.query.get(data["category_id"])

        if not category:
            return jsonify({
                "message": "Category not found"
            }), 404

        product.category_id = category.id

    db.session.commit()

    return jsonify(product.to_dict()), 200


@main.route("/products/<int:id>", methods=["DELETE"])
def delete_product(id):
    product = Product.query.get(id)

    if not product:
        return jsonify({
            "message": "Product not found"
        }), 404

    if product.order_items:
        return jsonify({
            "message": "Product cannot be deleted because it belongs to an order"
        }), 409

    db.session.delete(product)
    db.session.commit()

    return jsonify({
        "message": "Product deleted successfully"
    }), 200


# =========================
# CATEGORIES
# =========================

@main.route("/categories", methods=["GET"])
def categories():
    categories = Category.query.all()

    return jsonify([
        {
            "id": category.id,
            "name": category.name
        }
        for category in categories
    ]), 200


@main.route("/categories/<int:id>", methods=["GET"])
def get_category(id):
    category = Category.query.get(id)

    if not category:
        return jsonify({
            "message": "Category not found"
        }), 404

    return jsonify({
        "id": category.id,
        "name": category.name,
        "products": [
            product.to_dict()
            for product in category.products
        ]
    }), 200


@main.route("/categories", methods=["POST"])
def create_category():
    data = request.get_json()

    if not data:
        return jsonify({
            "message": "Request body is required"
        }), 400

    if "name" not in data:
        return jsonify({
            "message": "name is required"
        }), 400

    if not isinstance(data["name"], str) or not data["name"].strip():
        return jsonify({
            "message": "Name must be a non-empty string"
        }), 400

    name = data["name"].strip()

    existing_category = Category.query.filter_by(
        name=name
    ).first()

    if existing_category:
        return jsonify({
            "message": "Category already exists"
        }), 409

    category = Category(name=name)

    db.session.add(category)
    db.session.commit()

    return jsonify({
        "id": category.id,
        "name": category.name
    }), 201


@main.route("/categories/<int:id>", methods=["PUT"])
def update_category(id):
    category = Category.query.get(id)

    if not category:
        return jsonify({
            "message": "Category not found"
        }), 404

    data = request.get_json()

    if not data:
        return jsonify({
            "message": "Request body is required"
        }), 400

    if "name" not in data:
        return jsonify({
            "message": "name is required"
        }), 400

    if not isinstance(data["name"], str) or not data["name"].strip():
        return jsonify({
            "message": "Name must be a non-empty string"
        }), 400

    name = data["name"].strip()

    existing_category = Category.query.filter(
        Category.name == name,
        Category.id != id
    ).first()

    if existing_category:
        return jsonify({
            "message": "Category already exists"
        }), 409

    category.name = name

    db.session.commit()

    return jsonify({
        "id": category.id,
        "name": category.name
    }), 200


@main.route("/categories/<int:id>", methods=["DELETE"])
def delete_category(id):
    category = Category.query.get(id)

    if not category:
        return jsonify({
            "message": "Category not found"
        }), 404

    if category.products:
        return jsonify({
            "message": "Category cannot be deleted because it has products"
        }), 409

    db.session.delete(category)
    db.session.commit()

    return jsonify({
        "message": "Category deleted successfully"
    }), 200


# =========================
# USERS
# =========================

@main.route("/users", methods=["GET"])
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
    ]), 200


@main.route("/users", methods=["POST"])
def create_user():
    data = request.get_json()

    if not data:
        return jsonify({
            "message": "Request body is required"
        }), 400

    required_fields = [
        "name",
        "email",
        "password"
    ]

    for field in required_fields:
        if field not in data:
            return jsonify({
                "message": f"{field} is required"
            }), 400

    if not isinstance(data["name"], str) or not data["name"].strip():
        return jsonify({
            "message": "Name must be a non-empty string"
        }), 400

    if not isinstance(data["email"], str) or not data["email"].strip():
        return jsonify({
            "message": "Email cannot be empty"
        }), 400

    if not isinstance(data["password"], str) or len(data["password"]) < 6:
        return jsonify({
            "message": "Password must be at least 6 characters"
        }), 400

    email = data["email"].strip().lower()

    existing_user = User.query.filter_by(
        email=email
    ).first()

    if existing_user:
        return jsonify({
            "message": "Email already registered"
        }), 409

    user = User(
        name=data["name"].strip(),
        email=email,
        password=generate_password_hash(data["password"])
    )

    db.session.add(user)
    db.session.commit()

    return jsonify({
        "id": user.id,
        "name": user.name,
        "email": user.email,
        "created_at": user.created_at.isoformat()
    }), 201


# =========================
# AUTH
# =========================

@main.route("/auth/login", methods=["POST"])
def login():
    data = request.get_json()

    if not data:
        return jsonify({
            "message": "Request body is required"
        }), 400

    if "email" not in data or "password" not in data:
        return jsonify({
            "message": "Email and password are required"
        }), 400

    email = data["email"].strip().lower()

    user = User.query.filter_by(
        email=email
    ).first()

    if not user:
        return jsonify({
            "message": "Invalid email or password"
        }), 401

    if not check_password_hash(
        user.password,
        data["password"]
    ):
        return jsonify({
            "message": "Invalid email or password"
        }), 401

    return jsonify({
        "message": "Login successful",
        "user": {
            "id": user.id,
            "name": user.name,
            "email": user.email
        }
    }), 200


# =========================
# ORDERS
# =========================

@main.route("/orders", methods=["POST"])
def create_order():
    data = request.get_json()

    if not data:
        return jsonify({
            "message": "Request body is required"
        }), 400

    if "user_id" not in data:
        return jsonify({
            "message": "user_id is required"
        }), 400

    if "items" not in data or not isinstance(data["items"], list):
        return jsonify({
            "message": "items must be a list"
        }), 400

    if len(data["items"]) == 0:
        return jsonify({
            "message": "Order must contain at least one item"
        }), 400

    user = User.query.get(data["user_id"])

    if not user:
        return jsonify({
            "message": "User not found"
        }), 404

    total = 0
    order_items_data = []

    for item in data["items"]:
        if "product_id" not in item or "quantity" not in item:
            return jsonify({
                "message": "Each item requires product_id and quantity"
            }), 400

        product = Product.query.get(item["product_id"])

        if not product:
            return jsonify({
                "message": f"Product {item['product_id']} not found"
            }), 404

        quantity = item["quantity"]

        if not isinstance(quantity, int) or quantity <= 0:
            return jsonify({
                "message": "Quantity must be a positive integer"
            }), 400

        if product.stock < quantity:
            return jsonify({
                "message": f"Insufficient stock for product {product.id}"
            }), 400

        item_total = float(product.price) * quantity
        total += item_total

        order_items_data.append({
            "product": product,
            "quantity": quantity,
            "price": product.price
        })

    order = Order(
        user_id=user.id,
        total=total,
        status="pending"
    )

    db.session.add(order)

    for item_data in order_items_data:
        product = item_data["product"]

        order_item = OrderItem(
            order=order,
            product=product,
            quantity=item_data["quantity"],
            price=item_data["price"]
        )

        product.stock -= item_data["quantity"]

        db.session.add(order_item)

    db.session.commit()

    return jsonify({
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
    }), 201


@main.route("/orders", methods=["GET"])
def orders():
    user_id = request.args.get("user_id", type=int)

    if user_id:
        orders = Order.query.filter_by(
            user_id=user_id
        ).all()
    else:
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
    ]), 200


@main.route("/orders/<int:id>", methods=["GET"])
def get_order(id):
    order = Order.query.get(id)

    if not order:
        return jsonify({
            "message": "Order not found"
        }), 404

    return jsonify({
        "id": order.id,
        "user_id": order.user_id,
        "total": float(order.total),
        "status": order.status,
        "created_at": order.created_at.isoformat(),
        "items": [
            {
                "product_id": item.product_id,
                "quantity": item.quantity,
                "price": float(item.price),
                "product": {
                    "id": item.product.id,
                    "name": item.product.name,
                    "description": item.product.description,
                    "price": float(item.product.price),
                    "stock": item.product.stock,
                    "category_id": item.product.category_id
                }
            }
            for item in order.order_items
        ]
    }), 200


@main.route("/orders/<int:id>", methods=["PUT"])
def update_order(id):
    order = Order.query.get(id)

    if not order:
        return jsonify({
            "message": "Order not found"
        }), 404

    data = request.get_json()

    if not data:
        return jsonify({
            "message": "Request body is required"
        }), 400

    if "status" not in data:
        return jsonify({
            "message": "status is required"
        }), 400

    allowed_statuses = [
        "pending",
        "processing",
        "completed",
        "cancelled"
    ]

    if data["status"] not in allowed_statuses:
        return jsonify({
            "message": "Invalid order status"
        }), 400

    order.status = data["status"]

    db.session.commit()

    return jsonify({
        "id": order.id,
        "user_id": order.user_id,
        "total": float(order.total),
        "status": order.status,
        "created_at": order.created_at.isoformat()
    }), 200


@main.route("/orders/<int:id>", methods=["DELETE"])
def delete_order(id):
    order = Order.query.get(id)

    if not order:
        return jsonify({
            "message": "Order not found"
        }), 404

    for item in order.order_items:
        product = item.product

        if product:
            product.stock += item.quantity

        db.session.delete(item)

    db.session.delete(order)
    db.session.commit()

    return jsonify({
        "message": "Order deleted successfully"
    }), 200
