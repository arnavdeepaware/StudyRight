"""
Cleanup Script for Video Generation Files

This script deletes all files in the following directories to clean up
temporary and generated files from previous runs:
- audios: Audio clips generated for the video
- images: Generated images for the video
- output: Final output videos
- prompts: Generated AI prompts
- temp_videos: Temporary video segments
- uploads: Uploaded source files
"""

import os
import shutil
from pathlib import Path

def cleanup_directories():
    """Remove all files from specified directories"""
    # List of directories to clean
    directories = [
        'audios',
        'images',
        'output',
        'prompts',
        'temp_videos',
        'uploads'
    ]
    
    base_dir = Path(__file__).parent
    
    for directory in directories:
        dir_path = base_dir / directory
        
        print(f"Cleaning directory: {directory}")
        
        # Create directory if it doesn't exist
        if not dir_path.exists():
            print(f"  Creating directory: {directory}")
            os.makedirs(dir_path, exist_ok=True)
            continue
        
        try:
            # Remove all contents but keep the directory
            for item in dir_path.iterdir():
                if item.is_dir():
                    shutil.rmtree(item)
                    print(f"  Removed subdirectory: {item.name}")
                else:
                    item.unlink()
                    print(f"  Removed file: {item.name}")
        except Exception as e:
            print(f"  Error cleaning {directory}: {e}")
    
    print("Cleanup complete!")

if __name__ == "__main__":
    cleanup_directories()