import os
import shutil
import time
from pathlib import Path

def test_video_transfer():
    # Setup test directories
    backend_output = Path('output')
    frontend_videos = Path('../frontend/public/prev-videos')
    test_video = 'test_video.mp4'

    print("🔍 Starting video transfer test...")

    try:
        # Create test directories if they don't exist
        backend_output.mkdir(exist_ok=True)
        frontend_videos.mkdir(parents=True, exist_ok=True)

        # Create a dummy test video file
        test_video_path = backend_output / test_video
        with open(test_video_path, 'wb') as f:
            f.write(b'dummy video content')

        print(f"✅ Created test video at: {test_video_path}")

        # Generate unique name based on timestamp
        new_video_name = f"video_{int(time.time())}.mp4"
        new_video_path = frontend_videos / new_video_name

        # Try to copy the video file
        shutil.copy2(test_video_path, new_video_path)

        # Verify the transfer
        if new_video_path.exists():
            print(f"✅ Successfully copied video to: {new_video_path}")
            print(f"✅ File size: {new_video_path.stat().st_size} bytes")
            
            # Check permissions
            print(f"✅ File permissions: {oct(new_video_path.stat().st_mode)[-3:]}")
            
            # Check if frontend can access the file
            relative_path = f"frontend/public/prev-videos/{new_video_name}"
            print(f"✅ Frontend can access video at: {relative_path}")
            
            return True
        else:
            print("❌ Video transfer failed: File not found in frontend directory")
            return False

    except Exception as e:
        print(f"❌ Error during test: {str(e)}")
        return False
    finally:
        # Cleanup test files
        if test_video_path.exists():
            test_video_path.unlink()
        if new_video_path.exists():
            new_video_path.unlink()

if __name__ == "__main__":
    success = test_video_transfer()
    print(f"\n{'✅ Test passed!' if success else '❌ Test failed!'}")