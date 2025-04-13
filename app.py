from flask import Flask, request, jsonify
from database.mongo import mongo
import database.models.auth_controller as auth_controller
from dotenv import load_dotenv
from datetime import datetime
import os
import boto3
import jwt
from bson import ObjectId

load_dotenv()

app = Flask(__name__)

# Configs
app.config["MONGO_URI"] = os.getenv("MONGO_URI")
app.config["JWT_SECRET"] = os.getenv("JWT_SECRET")

# Initialize MongoDB
mongo.init_app(app)

# Initialize S3
s3 = boto3.client("s3",
    aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
    aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
    region_name=os.getenv("AWS_REGION")
)
BUCKET_NAME = os.getenv("S3_BUCKET_NAME")

# ------------------ AUTH ROUTES ------------------

@app.route("/api/auth/register", methods=["POST"])
def register():
    return auth_controller.register()

@app.route("/api/auth/login", methods=["POST"])
def login():
    return auth_controller.login()

@app.route("/api/profile", methods=["GET"])
def profile():
    token = request.headers.get("Authorization")
    if not token:
        return jsonify({"error": "Missing token"}), 401

    try:
        decoded = jwt.decode(token.split(" ")[1], app.config["JWT_SECRET"], algorithms=["HS256"])
        user = mongo.db.users.find_one({"_id": ObjectId(decoded["user_id"])})
        return jsonify({
            "email": user["email"],
            "joined": user["createdAt"]
        })
    except Exception as e:
        return jsonify({"error": "Invalid or expired token"}), 401

# ------------------ VIDEO UPLOAD ROUTE ------------------

@app.route('/api/upload-from-output', methods=['POST'])
def upload_from_output():
    filename = "final_video.mp4"  # You can make this dynamic later
    filepath = os.path.join("backend", "output", filename)  # Correct relative path

    if not os.path.exists(filepath):
        return jsonify({"error": f"File '{filename}' not found in backend/output/"}), 404

    try:
        # Upload to S3
        s3.upload_file(filepath, BUCKET_NAME, filename, ExtraArgs={"ACL": "public-read"})
        video_url = f"https://{BUCKET_NAME}.s3.amazonaws.com/{filename}"

        # Save metadata to MongoDB
        mongo.db.videos.insert_one({
            "filename": filename,
            "video_url": video_url,
            "status": "ready",
            "uploadedAt": datetime.utcnow()
        })

        return jsonify({
            "message": "Video uploaded successfully from backend/output/",
            "url": video_url
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# --------------------------------------------------------

if __name__ == '__main__':
    app.run(debug=True)


@app.route('/api/videos/<user_id>', methods=['GET'])
def get_user_videos(user_id):
    try:
        videos = list(mongo.db.videos.find({"user_id": user_id}))
        for video in videos:
            video["_id"] = str(video["_id"])  # Convert ObjectId to string
            video["uploadedAt"] = video["uploadedAt"].isoformat()  # Convert datetime

        return jsonify({"videos": videos})

    except Exception as e:
        return jsonify({"error": str(e)}), 500