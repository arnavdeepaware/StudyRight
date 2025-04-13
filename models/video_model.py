from database.mongo import mongo
from datetime import datetime

def save_video(user_id, lecture_id, script_id, video_url, thumbnail_url, duration):
    return mongo.db.videos.insert_one({
        "user_id": user_id,
        "lecture_id": lecture_id,
        "script_id": script_id,
        "video_url": video_url,
        "thumbnail_url": thumbnail_url,
        "duration_seconds": duration,
        "status": "ready",
        "generatedAt": datetime.utcnow()
    })