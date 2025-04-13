"""
Video Creation and Stitching Script
-----------------------------------
This script creates videos from image and audio pairs, then stitches them
together into a final output video.

Features:
- Pairs image files with corresponding audio files
- Creates individual video clips for each pair
- Stitches all clips together into a final output video
- Handles resizing and aspect ratio properly
- Provides detailed progress information

Usage:
    python movie.py

Directories:
    - images/: Contains images (.png, .jpg, .jpeg)
    - audios/: Contains audio files (.mp3, .wav)
    - temp_videos/: Temporary directory for individual videos
    - output/: Final output directory
"""

import os
from moviepy.editor import ImageClip, AudioFileClip, VideoFileClip, concatenate_videoclips
import sys

def batch_create_videos(image_dir="images", audio_dir="audios", output_dir="temp_videos"):
    """
    Create individual videos by pairing images with audio files.
    
    Args:
        image_dir (str): Directory containing image files
        audio_dir (str): Directory containing audio files
        output_dir (str): Directory to save individual videos
        
    Returns:
        bool: True if videos were created successfully, False otherwise
    """
    # Verify directories exist
    for directory in [image_dir, audio_dir]:
        if not os.path.exists(directory):
            print(f"⚠️ Directory not found: {directory}")
            return False
    
    # Create output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)

    # Get all files with supported extensions
    image_files = sorted([f for f in os.listdir(image_dir) 
                         if f.lower().endswith(('.png', '.jpg', '.jpeg'))])
    audio_files = sorted([f for f in os.listdir(audio_dir) 
                         if f.lower().endswith(('.mp3', '.wav'))])

    # Validate files existence
    if not image_files:
        print(f"⚠️ No image files found in {image_dir}")
        return False
    
    if not audio_files:
        print(f"⚠️ No audio files found in {audio_dir}")
        return False

    # Handle PIL ANTIALIAS compatibility issue in newer Pillow versions
    from PIL import Image
    if not hasattr(Image, 'ANTIALIAS'):
        Image.ANTIALIAS = Image.LANCZOS

    # Process tracking
    success_count = 0
    total_pairs = min(len(image_files), len(audio_files))
    
    # Create videos for each image-audio pair
    for i in range(total_pairs):
        try:
            image_path = os.path.join(image_dir, image_files[i])
            audio_path = os.path.join(audio_dir, audio_files[i])

            # Create output filename
            base_name = f"video_{i:03d}"  # Zero-padded for proper sorting
            output_path = os.path.join(output_dir, f"{base_name}.mp4")

            print(f"🔄 Creating video {i+1}/{total_pairs}: {image_files[i]} + {audio_files[i]}")

            # Create video components
            image_clip = ImageClip(image_path)
            audio_clip = AudioFileClip(audio_path)
            duration = audio_clip.duration
            
            # Resize the image to fit the target dimensions while maintaining aspect ratio
            # Height of 1080 for standard HD video
            video = image_clip.set_duration(duration).resize(height=1080)
            
            # Center crop if width exceeds target (607px)
            if video.w > 607:
                video = video.crop(width=607, height=1080, x_center=video.w/2)
            
            # Add audio to the video
            video = video.set_audio(audio_clip)

            # Write video file with high quality settings
            video.write_videofile(
                output_path, 
                fps=24, 
                codec='libx264', 
                audio_codec='aac',
                bitrate="5000k"
            )

            print(f"✅ Created {output_path}")
            success_count += 1
        
        except Exception as e:
            print(f"❌ Error creating video from {image_files[i]} and {audio_files[i]}: {str(e)}")

    # Summarize results
    print(f"\n📊 Summary: Created {success_count}/{total_pairs} videos")
    return success_count > 0

def stitch_videos(video_dir, output_path):
    """
    Stitch multiple videos together into a single video.
    
    Args:
        video_dir (str): Directory containing videos to stitch
        output_path (str): Output path for the final video
        
    Returns:
        bool: True if stitching was successful, False otherwise
    """
    try:
        # Create output directory if it doesn't exist
        output_directory = os.path.dirname(output_path)
        if output_directory:
            os.makedirs(output_directory, exist_ok=True)
        
        # Load all mp4 files from the video directory and sort them
        video_files = sorted([f for f in os.listdir(video_dir) if f.lower().endswith(".mp4")])
        
        if not video_files:
            print(f"⚠️ No video files found in {video_dir}")
            return False
        
        print(f"🔄 Stitching {len(video_files)} videos together...")
        
        # Load all video clips
        clips = []
        for filename in video_files:
            path = os.path.join(video_dir, filename)
            print(f"➕ Adding {filename}")
            clips.append(VideoFileClip(path))

        # Combine all video clips
        final_clip = concatenate_videoclips(clips, method="compose")

        # Export final video with high quality settings
        final_clip.write_videofile(
            output_path, 
            fps=24,
            codec='libx264',
            audio_codec='aac',
            bitrate="8000k"
        )

        print(f"\n✅ Final stitched video saved to: {output_path}")
        
        # Close all clips to free resources
        final_clip.close()
        for clip in clips:
            clip.close()
            
        return True
        
    except Exception as e:
        print(f"❌ Error stitching videos: {str(e)}")
        return False

def process_videos():
    """
    Main function to process videos from start to finish:
    1. Create individual videos from images and audio
    2. Stitch them together into a final output
    
    Returns:
        int: 0 for success, 1 for failure
    """
    print("🎬 Video Processing Pipeline")
    print("---------------------------")
    
    # Define directories
    image_dir = "images"
    audio_dir = "audios"
    temp_dir = "temp_videos"
    output_dir = "output"
    
    # Create output directory
    os.makedirs(output_dir, exist_ok=True)
    
    # Final output path
    output_path = os.path.join(output_dir, "final_video.mp4")
    
    # Step 1: Create individual videos
    print("\n📁 STEP 1: Creating individual videos")
    if not batch_create_videos(image_dir, audio_dir, temp_dir):
        print("❌ Failed to create individual videos. Stopping process.")
        return 1
    
    # Step 2: Stitch videos together
    print("\n📁 STEP 2: Stitching videos together")
    if not stitch_videos(temp_dir, output_path):
        print("❌ Failed to stitch videos. Stopping process.")
        return 1
    
    print(f"\n🎉 COMPLETE: Final video created at {output_path}")
    return 0

if __name__ == "__main__":
    sys.exit(process_videos())