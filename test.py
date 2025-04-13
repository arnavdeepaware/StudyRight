import boto3

# Initialize S3 client
s3 = boto3.client('s3')

# Local path to your video file
file_path = 'backend/output/final_video.mp4'

# Name of your S3 bucket
bucket_name = 'bitcamp-studyright'

# Desired name in S3
s3_key = 'videos/video.mp4'

# Upload the file
s3.upload_file(file_path, bucket_name, s3_key, ExtraArgs={'ACL': 'public-read'})


print(f"Uploaded {file_path} to s3://{bucket_name}/{s3_key}")

# url = s3.generate_presigned_url(
#     ClientMethod='get_object',
#     Params={'Bucket': bucket_name, 'Key': s3_key},
#     ExpiresIn = 50000  # URL expires in 1 hour
# )

# print("Access the file with this link:", url)


# https://bitcamp-studyright.s3.us-east-1.amazonaws.com//videos/video.mp4
