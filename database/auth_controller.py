from flask import request, jsonify
from database.user_model import find_user_by_email, create_user, check_password
import jwt
from datetime import datetime, timedelta
import os

JWT_SECRET = os.getenv("JWT_SECRET")


def register():
    data = request.get_json()
    email = data.get("email")
    password = data.get("password")

    if find_user_by_email(email):
        return jsonify({"error": "User already exists"}), 400

    create_user(email, password)
    return jsonify({"message": "User registered successfully"}), 201


def login():
    data = request.get_json()
    email = data.get("email")
    password = data.get("password")

    user = find_user_by_email(email)
    if not user or not check_password(user, password):
        return jsonify({"error": "Invalid credentials"}), 401

    token = jwt.encode({
        "user_id": str(user['_id']),
        "exp": datetime.utcnow() + timedelta(days=7)
    }, JWT_SECRET, algorithm="HS256")

    return jsonify({"token": token, "email": email})
