from flask import Blueprint, request, jsonify
from app.database import db
from app.models import User
import hashlib

users_bp = Blueprint('users', __name__)

def mock_hash(password: str) -> str:
    return hashlib.sha256(password.encode()).hexdigest()

@users_bp.route('/users/register', methods=['POST'])
def register_user():
    data = request.get_json() or {}

    username = data.get('username')
    email = data.get('email')
    password = data.get('password')

    if not username or not email or not password:
        return jsonify({"error": "Missing required fields: username, email, password"}), 400

    if User.query.filter_by(email=email).first():
        return jsonify({"error": "Email already registered"}), 409

    new_user = User(
        username=username,
        email=email,
        password_hash=mock_hash(password),
        role=data.get('role', 'customer')
    )

    db.session.add(new_user)
    db.session.commit()

    return jsonify({
        "id": new_user.id,
        "username": new_user.username,
        "email": new_user.email,
        "role": new_user.role,
        "created_at": new_user.created_at.isoformat()
    }), 201

@users_bp.route('/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    user = User.query.get(user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404

    return jsonify({
        "id": user.id,
        "username": user.username,
        "email": user.email,
        "role": user.role,
        "created_at": user.created_at.isoformat()
    }), 200