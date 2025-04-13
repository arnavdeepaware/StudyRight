from flask import Flask, request, jsonify
from werkzeug.utils import secure_filename  # Safely handles uploaded filenames
from database.mongo import mongo  # MongoDB connection
from datetime import datetime
import boto3
import os
from dotenv import load_dotenv

# Load AWS and Mongo credentials from .env file
load_dotenv()

# ✅ Set up the S3 client using credentials from the .env file
s3 = boto3.client("s3",
    aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),            # AWS access key
    aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),    # AWS secret key
    region_name=os.getenv("AWS_REGION")                          # e.g., us-east-1
)

BUCKET_NAME = os.getenv("S3_BUCKET_NAME")  # Get bucket name from .env

# ✅ Initialize Flask app
app = Flask(__name__)

# ✅ Define route to handle video upload from frontend or Postman
@app.route('/api/upload-video', methods=['POST'])
def upload_video():
    # Check if a file was included in the request
    if 'video' not in request.files:
        return jsonify({"error": "No video file provided"}), 400

    # Get the video file and sanitize the filename
    video_file = request.files['video']
    filename = secure_filename(video_file.filename)

    try:
        # ✅ Upload the file to AWS S3 (no ACL = private by default or bucket policy controlled)
        s3.upload_fileobj(video_file, BUCKET_NAME, filename)

        # ✅ Create a URL to access the uploaded video
        video_url = f"https://{BUCKET_NAME}.s3.amazonaws.com/{filename}"

        # ✅ Save video metadata to MongoDB
        video_doc = {
            "user_id": "placeholder-user-id",  # Replace this with actual user_id if using JWT
            "video_url": video_url,            # Public S3 URL to video
            "filename": filename,              # Original filename
            "duration_seconds": 0,             # Placeholder — you can calculate with moviepy
            "status": "ready",                 # You could set "processing" if you're generating video
            "uploadedAt": datetime.utcnow()    # Save current UTC time
        }
        mongo.db.videos.insert_one(video_doc)

        # ✅ Return success response and video URL
        return jsonify({
            "message": "Video uploaded successfully",
            "url": video_url
        })

    except Exception as e:
        # Catch and return any errors during upload or DB insert
        return jsonify({"error": f"Failed to upload: {str(e)}"}), 500