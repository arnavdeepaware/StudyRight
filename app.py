from flask import Flask, request, jsonify, send_file
from database.mongo import mongo
import database.models.auth_controller as auth_controller
from dotenv import load_dotenv
from datetime import datetime
from werkzeug.utils import secure_filename
import boto3
import jwt
from bson import ObjectId
import os
import importlib.util
import shutil

# Load .env
load_dotenv()

app = Flask(__name__)

# Configs
app.config["MONGO_URI"] = os.getenv("MONGO_URI")
app.config["JWT_SECRET"] = os.getenv("JWT_SECRET")
app.config["UPLOAD_FOLDER"] = "uploads"
os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)

# Initialize services
mongo.init_app(app)
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

# ------------------ LECTURE FILE UPLOAD ------------------

@app.route('/api/upload', methods=['POST'])
def upload_lecture_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file uploaded'}), 400

    file = request.files['file']
    filename = secure_filename(file.filename)
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(filepath)

    return jsonify({'message': 'File uploaded', 'filename': filename})

# ------------------ VIDEO GENERATION ------------------

@app.route('/api/video/<filename>', methods=['GET'])
def generate_video_from_file(filename):
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    if not os.path.exists(filepath):
        return jsonify({'error': 'File not found'}), 404

    result = file_to_video(filepath)
    if result['status'] == 'success':
        return send_file(result['output_video'], mimetype='video/mp4')
    else:
        return jsonify({'error': result.get('error', 'Video generation failed')}), 500

# ------------------ S3 UPLOAD FROM OUTPUT ------------------

@app.route('/api/upload-from-output', methods=['POST'])
def upload_from_output():
    filename = "final_video.mp4"
    filepath = os.path.join("backend", "output", filename)

    if not os.path.exists(filepath):
        return jsonify({"error": f"File '{filename}' not found in backend/output/"}), 404

    try:
        s3.upload_file(filepath, BUCKET_NAME, filename)
        video_url = f"https://{BUCKET_NAME}.s3.amazonaws.com/{filename}"

        mongo.db.videos.insert_one({
            "filename": filename,
            "video_url": video_url,
            "status": "ready",
            "uploadedAt": datetime.utcnow()
        })

        return jsonify({
            "message": "Video uploaded to S3",
            "url": video_url
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# ------------------ GET USER VIDEOS ------------------

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

# ------------------ VIDEO PROCESSING PIPELINE ------------------

def file_to_video(file_path):
    from extract import process_uploaded_file

    results = {
        "status": "processing",
        "steps": {},
        "output_video": None,
        "error": None
    }

    try:
        filename = os.path.basename(file_path)

        # Step 1: Extract
        extraction_result = process_uploaded_file(filename)
        results["steps"]["extraction"] = extraction_result
        if "error" in extraction_result:
            results["status"] = "failed"
            results["error"] = extraction_result["error"]
            return results

        # Step 2: Parse prompts
        parse_spec = importlib.util.spec_from_file_location("parse_summary", "parse-summary.py")
        parse_module = importlib.util.module_from_spec(parse_spec)
        parse_spec.loader.exec_module(parse_module)
        json_path = os.path.join('prompts', 'all_prompts.json')
        audio_path, image_path = parse_module.process_summary_file(json_path, 'prompts')

        # Step 3: Generate images
        img_spec = importlib.util.spec_from_file_location("gen_img", "gen-img.py")
        img_module = importlib.util.module_from_spec(img_spec)
        img_spec.loader.exec_module(img_module)
        shutil.rmtree("images", ignore_errors=True)
        os.makedirs("images", exist_ok=True)
        img_module.main()

        # Step 4: Generate audio
        aud_spec = importlib.util.spec_from_file_location("gen_aud", "gen-aud.py")
        aud_module = importlib.util.module_from_spec(aud_spec)
        aud_spec.loader.exec_module(aud_module)
        shutil.rmtree("audios", ignore_errors=True)
        os.makedirs("audios", exist_ok=True)
        aud_module.generate_all_audio_files()

        # Step 5: Generate final video
        movie_spec = importlib.util.spec_from_file_location("movie", "movie.py")
        movie_module = importlib.util.module_from_spec(movie_spec)
        movie_spec.loader.exec_module(movie_module)
        shutil.rmtree("output", ignore_errors=True)
        os.makedirs("output", exist_ok=True)
        result_code = movie_module.process_videos()
        final_video_path = os.path.join("output", "final_video.mp4")

        if result_code != 0 or not os.path.exists(final_video_path):
            results["status"] = "failed"
            results["error"] = "Video generation failed"
            return results

        results["status"] = "success"
        results["output_video"] = final_video_path
        return results

    except Exception as e:
        import traceback
        results["status"] = "failed"
        results["error"] = str(e)
        results["error_details"] = traceback.format_exc()
        return results

# ------------------ RUN APP ------------------

if __name__ == '__main__':
    app.run(debug=True, port=5000)