# Import the AWS SDK for Python and environment variable tools
import boto3
import os
from dotenv import load_dotenv

# Load environment variables from a .env file
load_dotenv()

# ✅ Initialize the S3 client using credentials stored in your .env file
s3 = boto3.client('s3',
    aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),           # Your AWS access key
    aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'),   # Your AWS secret key
    region_name=os.getenv('AWS_REGION')                          # Your AWS region (e.g., us-east-1)
)

# 📦 This function uploads a video file from your local backend to an S3 bucket
def upload_video(file_path, s3_filename):
    bucket = os.getenv('S3_BUCKET_NAME')  # The name of the S3 bucket (from .env)
    
    # Upload the file to S3 with public-read permission so it can be viewed via browser
    s3.upload_file(
        file_path,     # Local path to the file (e.g., 'backend/output/final_video.mp4')
        bucket,        # Name of the bucket to upload to
        s3_filename,   # Name the file will have on S3 (e.g., 'final_video.mp4')
        ExtraArgs={'ACL': 'public-read'}  # Make the file publicly accessible
    )
    
    # Build and return the public URL to the uploaded video
    url = f"https://{bucket}.s3.amazonaws.com/{s3_filename}"
    return url