"""
Video Generation API Server

This Flask application provides an API for:
1. Uploading documents (PDF, DOCX, TXT, DOC)
2. Converting uploaded documents to educational videos
3. Serving the generated videos

The conversion pipeline includes:
- Text extraction from documents
- AI-powered content analysis
- Prompt generation for images and audio
- Image generation
- Audio voice-over generation
- Video assembly and stitching
"""

from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
import os
import importlib.util
import json
import sys
import shutil
import time  # Add this import here
import traceback  # Add this import here
from werkzeug.utils import secure_filename

# Initialize Flask app
app = Flask(__name__)
CORS(app, resources={
    r"/api/*": {
        "origins": [
            "http://localhost:3000",
            "http://127.0.0.1:3000",
            "http://localhost:5173",  # Add Vite dev server
            "http://127.0.0.1:5173"   # Add Vite dev server IP
        ],
        "methods": ["GET", "POST", "OPTIONS"],
        "allow_headers": ["Content-Type", "Authorization", "Accept"],
        "expose_headers": ["Content-Type"],
        "supports_credentials": True
    }
})

# Configuration
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'doc', 'docx'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Create uploads directory if it doesn't exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def allowed_file(filename):
    """
    Check if the uploaded file has an allowed extension
    
    Args:
        filename (str): Name of the uploaded file
        
    Returns:
        bool: True if file extension is allowed, False otherwise
    """
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/api/upload', methods=['POST'])
def upload_file():
    """
    API endpoint to handle file uploads
    
    Accepts POST requests with files and saves valid files to the uploads directory.
    
    Returns:
        JSON response with success/error message and filename if successful
    """
    # Check if the post request has the file part
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    
    file = request.files['file']
    
    # If user does not select file, browser might submit an empty file
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        
        return jsonify({
            'message': 'File successfully uploaded',
            'filename': filename
        })
    
    return jsonify({'error': 'File type not allowed'}), 400

@app.route('/api/video/<filename>', methods=['GET'])
def get_video(filename):
    """
    Generate and return a video from an uploaded file
    
    This endpoint triggers the complete video generation pipeline for the specified file.
    
    Args:
        filename (str): The name of the file to convert to video
        
    Returns:
        Response: The video file or error message
    """
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    
    # Check if the file exists
    if not os.path.exists(filepath):
        return jsonify({'error': 'File not found'}), 404
    
    # Process the file to generate a video
    result = file_to_video(filepath)
    
    if result["status"] == "success" and os.path.exists(result["output_video"]):
        # Return the video file
        return send_file(result["output_video"], mimetype='video/mp4')
    else:
        # Return error details
        return jsonify({
            'error': 'Failed to generate video',
            'details': result
        }), 500

def file_to_video(file_path):
    """
    Process an uploaded file through the complete video generation pipeline.
    
    This function orchestrates the following steps:
    1. Extract text content from the uploaded file
    2. Process the extracted text with Gemini AI and generate prompts
    3. Parse the prompts into separate audio and image instructions
    4. Generate images from the image prompts
    5. Generate audio from the audio prompts
    6. Create a video by combining the generated images and audio
    
    Args:
        file_path (str): Path to the uploaded file
        
    Returns:
        dict: Status information including success/failure and output video path
    """
    from extract import process_uploaded_file
    
    # Create a results dictionary to track progress
    results = {
        "status": "processing",
        "steps": {},
        "output_video": None,
        "error": None
    }
    
    try:
        # Get just the filename from the path
        filename = os.path.basename(file_path)
        print(f"🔄 Starting video generation pipeline for: {filename}")
        
        # Step 1: Extract text and process with Gemini AI
        print("📄 Step 1: Extracting document content...")
        extraction_result = process_uploaded_file(filename)
        results["steps"]["extraction"] = extraction_result
        
        if "error" in extraction_result:
            results["status"] = "failed"
            results["error"] = extraction_result["error"]
            return results
            
        print("✅ Document extraction complete")
        
        # Step 2: Parse the AI-generated prompts into audio and image instructions
        print("🔍 Step 2: Parsing summary into prompts...")
        try:
            # Import the parser module
            parser_spec = importlib.util.spec_from_file_location(
                "parser", 
                os.path.join(os.path.dirname(__file__), "parser.py")
            )
            parser_module = importlib.util.module_from_spec(parser_spec)
            parser_spec.loader.exec_module(parser_module)
            
            # Ensure prompts directory exists
            prompts_dir = os.path.join(os.path.dirname(__file__), 'prompts')
            os.makedirs(prompts_dir, exist_ok=True)
            
            # Parse the Gemini output with absolute paths
            parser_module.parse_gemini_output()
            
            # Verify the files were created using absolute paths
            audio_path = os.path.join(prompts_dir, 'audio_prompts.txt')
            image_path = os.path.join(prompts_dir, 'image_prompts.txt')
            
            if not os.path.exists(audio_path) or not os.path.exists(image_path):
                print(f"Debug - Audio path exists: {os.path.exists(audio_path)}")
                print(f"Debug - Image path exists: {os.path.exists(image_path)}")
                raise Exception(f"Failed to generate prompt files in {prompts_dir}")
                
            results["steps"]["parsing"] = {
                "audio_prompts": audio_path,
                "image_prompts": image_path,
                "status": "success"
            }
            print("✅ Prompts parsed successfully")
            print(f"   Audio prompts: {audio_path}")
            print(f"   Image prompts: {image_path}")
            
        except Exception as e:
            results["status"] = "failed"
            results["error"] = f"Failed to parse prompts: {str(e)}"
            print(f"❌ Parser error: {str(e)}")
            return results
        
        # Step 3: Generate images from prompts
        print("🎨 Step 3: Generating images...")
        
        # Clean images directory before generating new ones
        images_dir = 'images'
        if os.path.exists(images_dir):
            shutil.rmtree(images_dir)
        os.makedirs(images_dir, exist_ok=True)
        
        # Import the image generation module
        img_spec = importlib.util.spec_from_file_location("gen_img", "gen-img.py")
        img_module = importlib.util.module_from_spec(img_spec)
        img_spec.loader.exec_module(img_module)
        
        # Generate images
        img_module.main()
        
        # Check if images were created
        image_files = [f for f in os.listdir(images_dir) if f.lower().endswith(('.png', '.jpg', '.jpeg'))]
        if not image_files:
            results["status"] = "failed"
            results["error"] = "Failed to generate images"
            return results
            
        results["steps"]["images"] = {
            "count": len(image_files),
            "directory": images_dir
        }
        print(f"✅ Generated {len(image_files)} images")
        
        # Step 4: Generate audio from prompts
        print("🔊 Step 4: Generating audio...")
        
        # Clean audio directory before generating new ones
        audio_dir = 'audios'
        if os.path.exists(audio_dir):
            shutil.rmtree(audio_dir)
        os.makedirs(audio_dir, exist_ok=True)
        
        # Import the audio generation module
        aud_spec = importlib.util.spec_from_file_location("gen_aud", "gen-aud.py")
        aud_module = importlib.util.module_from_spec(aud_spec)
        aud_spec.loader.exec_module(aud_module)
        
        # Generate audio
        aud_module.generate_all_audio_files()
        
        # Check if audio files were created
        audio_files = [f for f in os.listdir(audio_dir) if f.lower().endswith(('.mp3', '.wav'))]
        if not audio_files:
            results["status"] = "failed"
            results["error"] = "Failed to generate audio files"
            return results
            
        results["steps"]["audio"] = {
            "count": len(audio_files),
            "directory": audio_dir
        }
        print(f"✅ Generated {len(audio_files)} audio files")
        
        # Step 5: Create video by combining images and audio
        print("🎬 Step 5: Creating final video...")
        
        # Clean temp_videos and output directories
        temp_dir = 'temp_videos'
        output_dir = 'output'
        for directory in [temp_dir, output_dir]:
            if os.path.exists(directory):
                shutil.rmtree(directory)
            os.makedirs(directory, exist_ok=True)
        
        # Import the movie creation module
        movie_spec = importlib.util.spec_from_file_location("movie", "movie.py")
        movie_module = importlib.util.module_from_spec(movie_spec)
        movie_spec.loader.exec_module(movie_module)
        
        # Create the video
        result_code = movie_module.process_videos()
        
        # Check if final video was created
        final_video_path = os.path.join(output_dir, "final_video.mp4")
        if result_code != 0 or not os.path.exists(final_video_path):
            results["status"] = "failed"
            results["error"] = f"Failed to create final video (exit code: {result_code})"
            return results
        
        # Success
        results["status"] = "success"
        results["output_video"] = final_video_path
        print(f"✅ Final video created at: {final_video_path}")

        # Copy final video to frontend public directory
        frontend_videos_dir = '../frontend/public/prev-videos'
        os.makedirs(frontend_videos_dir, exist_ok=True)
        
        # Generate unique name based on timestamp
        new_video_name = f"video_{int(time.time())}.mp4"
        new_video_path = os.path.join(frontend_videos_dir, new_video_name)
        
        # Copy the video file
        shutil.copy2(final_video_path, new_video_path)
        print(f"✅ Video copied to frontend at: {new_video_path}")
        
        return results
        
    except Exception as e:
        error_details = traceback.format_exc()
        results["status"] = "failed"
        results["error"] = f"Error in video generation pipeline: {str(e)}"
        results["error_details"] = error_details
        print(f"❌ Error: {str(e)}")
        return results

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8080)