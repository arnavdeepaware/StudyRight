from flask import Flask, request, jsonify
from werkzeug.utils import secure_filename
from database.mongo import mongo
import database.models.auth_controller as auth_controller
from dotenv import load_dotenv
from datetime import datetime
import os
import boto3
import jwt
from bson import ObjectId

# Load environment variables from .env
load_dotenv()

# Flask app
app = Flask(__name__)

# Configs
app.config["MONGO_URI"] = os.getenv("MONGO_URI")
app.config["JWT_SECRET"] = os.getenv("JWT_SECRET")
app.config["UPLOAD_FOLDER"] = "uploads"
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'doc', 'docx'}
os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)

# Initialize MongoDB
mongo.init_app(app)

# Initialize AWS S3
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

# ------------------ VIDEO UPLOAD FROM OUTPUT ------------------

@app.route('/api/upload-from-output', methods=['POST'])
def upload_from_output():
    filename = "final_video.mp4"
    filepath = os.path.join("backend", "output", filename)

    print("🔍 Checking file:", filepath)
    if not os.path.exists(filepath):
        return jsonify({"error": f"File '{filename}' not found in backend/output/"}), 404

    try:
        s3.upload_file(filepath, BUCKET_NAME, filename, ExtraArgs={"ACL": "public-read"})
        video_url = f"https://{BUCKET_NAME}.s3.amazonaws.com/{filename}"

        mongo.db.videos.insert_one({
            "filename": filename,
            "video_url": video_url,
            "status": "ready",
            "uploadedAt": datetime.utcnow()
        })

        print("✅ Uploaded to S3:", video_url)
        return jsonify({
            "message": "Video uploaded successfully to S3",
            "url": video_url
        })

    except Exception as e:
        print("❌ Upload failed:", str(e))
        return jsonify({"error": str(e)}), 500

# ------------------ FETCH USER VIDEOS ------------------

@app.route('/api/videos/<user_id>', methods=['GET'])
def get_user_videos(user_id):
    try:
        videos = list(mongo.db.videos.find({"user_id": user_id}))
        for video in videos:
            video["_id"] = str(video["_id"])
            video["uploadedAt"] = video["uploadedAt"].isoformat()
        return jsonify({"videos": videos})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# ------------------ DOCUMENT UPLOAD ENDPOINT ------------------

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/api/upload', methods=['POST'])
def upload_file():
    print("📥 Incoming POST to /api/upload")
    print("🧾 request.files keys:", list(request.files.keys()))

    if 'file' not in request.files:
        print("❌ No file key in request.files")
        return jsonify({'error': 'No file part'}), 400

    file = request.files['file']
    print("📄 Filename received:", file.filename)

    if file.filename == '':
        print("❌ Empty filename received")
        return jsonify({'error': 'No selected file'}), 400

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)

        print(f"✅ File saved to: {filepath}")
        return jsonify({
            'message': 'File successfully uploaded',
            'filename': filename
        })

    print("❌ File type not allowed")
    return jsonify({'error': 'File type not allowed'}), 400

# ------------------ MAIN ------------------

if __name__ == '__main__':
    app.run(debug=True, port=5000)