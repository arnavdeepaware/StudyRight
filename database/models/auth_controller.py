from flask import request, jsonify
from database.mongo import mongo
from datetime import datetime, timedelta
import jwt
import os
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt()

JWT_SECRET = os.getenv("JWT_SECRET")
JWT_EXPIRATION_MINUTES = 60  # token expires in 1 hour

# -------------------------------
# REGISTER
# -------------------------------
def register():
    data = request.get_json()
    email = data.get("email")
    password = data.get("password")

    if not email or not password:
        return jsonify({"error": "Email and password required"}), 400

    existing_user = mongo.db.users.find_one({"email": email})
    if existing_user:
        return jsonify({"error": "User already exists"}), 400

    hashed_pw = bcrypt.generate_password_hash(password).decode("utf-8")

    result = mongo.db.users.insert_one({
        "email": email,
        "password": hashed_pw,
        "createdAt": datetime.utcnow()
    })

    return jsonify({
        "message": "User registered successfully",
        "user_id": str(result.inserted_id)
    })

# -------------------------------
# LOGIN
# -------------------------------
def login():
    data = request.get_json()
    email = data.get("email")
    password = data.get("password")

    if not email or not password:
        return jsonify({"error": "Email and password required"}), 400

    user = mongo.db.users.find_one({"email": email})
    if not user:
        return jsonify({"error": "User not found"}), 404

    if not bcrypt.check_password_hash(user["password"], password):
        return jsonify({"error": "Invalid credentials"}), 401

    token_payload = {
        "user_id": str(user["_id"]),
        "exp": datetime.utcnow() + timedelta(minutes=JWT_EXPIRATION_MINUTES)
    }

    token = jwt.encode(token_payload, JWT_SECRET, algorithm="HS256")

    return jsonify({
        "message": "Login successful",
        "token": token
    })