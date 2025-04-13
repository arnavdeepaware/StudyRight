from flask import Flask, request, jsonify
from werkzeug.utils import secure_filename
from database.mongo import mongo
from datetime import datetime
import boto3
import os
from dotenv import load_dotenv

load_dotenv()

# AWS S3 Setup
s3 = boto3.client("s3",
    aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
    aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
    region_name=os.getenv("AWS_REGION")
)
BUCKET_NAME = os.getenv("S3_BUCKET_NAME")

# Flask App
app = Flask(__name__)

@app.route('/api/upload-video', methods=['POST'])
def upload_video():
    if 'video' not in request.files:
        return jsonify({"error": "No video file provided"}), 400

    video_file = request.files['video']
    filename = secure_filename(video_file.filename)

    try:
        # ✅ Upload to S3 WITHOUT ACL (fixes your error)
        s3.upload_fileobj(video_file, BUCKET_NAME, filename)
        video_url = f"https://{BUCKET_NAME}.s3.amazonaws.com/{filename}"

        # ✅ Save metadata to MongoDB
        video_doc = {
            "user_id": "placeholder-user-id",  # Replace with real user_id if needed
            "video_url": video_url,
            "filename": filename,
            "duration_seconds": 0,  # Optional: calculate with moviepy later
            "status": "ready",
            "uploadedAt": datetime.utcnow()
        }
        mongo.db.videos.insert_one(video_doc)

        return jsonify({
            "message": "Video uploaded successfully",
            "url": video_url
        })

    except Exception as e:
        return jsonify({"error": f"Failed to upload: {str(e)}"}), 500