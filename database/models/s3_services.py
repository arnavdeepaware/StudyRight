import boto3
import os
from dotenv import load_dotenv
load_dotenv()

s3 = boto3.client('s3',
    aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
    aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'),
    region_name=os.getenv('AWS_REGION')
)

def upload_video(file_path, s3_filename):
    bucket = os.getenv('S3_BUCKET_NAME')
    s3.upload_file(file_path, bucket, s3_filename, ExtraArgs={'ACL': 'public-read'})
    url = f"https://{bucket}.s3.amazonaws.com/{s3_filename}"
    return url