import os
from moviepy.editor import *

def batch_create_videos(image_dir, audio_dir, output_dir):
    # Verify directories exist
    for directory in [image_dir, audio_dir]:
        if not os.path.exists(directory):
            print(f"⚠️ Directory not found: {directory}")
            return
    
    os.makedirs(output_dir, exist_ok=True)

    # Get all files
    image_files = sorted([f for f in os.listdir(image_dir) if f.endswith(('.png', '.jpg', '.jpeg'))])
    audio_files = sorted([f for f in os.listdir(audio_dir) if f.endswith(('.mp3', '.wav'))])

    if not image_files:
        print(f"⚠️ No image files found in {image_dir}")
        return
    
    if not audio_files:
        print(f"⚠️ No audio files found in {audio_dir}")
        return

    # Monkey patch for PIL ANTIALIAS issue in newer Pillow versions
    from PIL import Image
    if not hasattr(Image, 'ANTIALIAS'):
        Image.ANTIALIAS = Image.LANCZOS

    # Create videos for each pair
    for i in range(min(len(image_files), len(audio_files))):
        try:
            image_path = os.path.join(image_dir, image_files[i])
            audio_path = os.path.join(audio_dir, audio_files[i])

            # Output filename
            base_name = f"video_{i}"
            output_path = os.path.join(output_dir, f"{base_name}.mp4")

            print(f"🔄 Creating video {i+1}/{min(len(image_files), len(audio_files))}: {image_files[i]} + {audio_files[i]}")

            # Create video
            image_clip = ImageClip(image_path)
            audio_clip = AudioFileClip(audio_path)

            duration = audio_clip.duration
            
            # Resize the image to fit the target dimensions while maintaining aspect ratio
            video = image_clip.set_duration(duration).resize(height=1080)
            
            # Center crop if needed
            if video.w > 607:
                video = video.crop(width=607, height=1080, x_center=video.w/2)
            
            video = video.set_audio(audio_clip)

            # Add progress callback to show encoding progress
            video.write_videofile(output_path, fps=24, codec='libx264', audio_codec='aac')

            print(f"✅ Created {output_path}")
        
        except Exception as e:
            print(f"❌ Error creating video from {image_files[i]} and {audio_files[i]}: {str(e)}")

def stitch_videos(video_dir, output_path="final_video.mp4"):
    # Load all mp4 files from the video directory
    video_files = sorted([f for f in os.listdir(video_dir) if f.endswith(".mp4")])
    
    clips = []
    for filename in video_files:
        path = os.path.join(video_dir, filename)
        print(f"Adding {filename}")
        clips.append(VideoFileClip(path))

    # Combine all video clips
    final_clip = concatenate_videoclips(clips, method="compose")

    # Export final video
    final_clip.write_videofile(output_path, fps=24)

    print(f"\n✅ Final stitched video saved to: {output_path}")




if __name__ == "__main__":
    #batch_create_videos("images", "audios", "videos")
    stitch_videos("videos", "stitched/final_output.mp4")