from flask import Flask, request, jsonify
from database.mongo import mongo
from database import auth_controller
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.config["MONGO_URI"] = os.getenv("MONGO_URI")
app.config["JWT_SECRET"] = os.getenv("JWT_SECRET")

# Initialize MongoDB
mongo.init_app(app)

# Routes
@app.route("/api/auth/register", methods=["POST"])
def register():
    return auth_controller.register()

@app.route("/api/auth/login", methods=["POST"])
def login():
    return auth_controller.login()

# Example protected route
@app.route("/api/profile", methods=["GET"])
def profile():
    token = request.headers.get("Authorization")
    if not token:
        return jsonify({"error": "Missing token"}), 401

    try:
        import jwt
        decoded = jwt.decode(token.split(" ")[1], app.config["JWT_SECRET"], algorithms=["HS256"])
        from bson import ObjectId
        user = mongo.db.users.find_one({"_id": ObjectId(decoded["user_id"])})
        return jsonify({"email": user["email"], "joined": user["createdAt"]})
    except Exception as e:
        return jsonify({"error": "Invalid or expired token"}), 401

if __name__ == '__main__':
    app.run(debug=True)