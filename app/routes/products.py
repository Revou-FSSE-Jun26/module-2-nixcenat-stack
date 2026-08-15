from flask import Blueprint, jsonify

products_bp = Blueprint('products', __name__)

HARDCODED_PRODUCTS = [
    {"id": 1, "name": "Wireless Noise-Canceling Headphones", "price": 199.99, "stock": 45},
    {"id": 2, "name": "Ergonomic Mechanical Keyboard", "price": 89.50, "stock": 120},
    {"id": 3, "name": "Ultra-Wide Gaming Monitor 34\"", "price": 449.00, "stock": 15}
]

@products_bp.route('/products', methods=['GET'])
def get_products():
    return jsonify(HARDCODED_PRODUCTS), 200

@products_bp.route('/products/<int:product_id>', methods=['GET'])
def get_product_by_id(product_id):
    product = next((p for p in HARDCODED_PRODUCTS if p["id"] == product_id), None)
    if not product:
        return jsonify({"error": "Product not found"}), 404
    return jsonify(product), 200