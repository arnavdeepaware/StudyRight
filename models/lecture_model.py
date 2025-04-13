from database.mongo import mongo
from datetime import datetime

def save_lecture(user_id, title, text):
    return mongo.db.lectures.insert_one({
        "user_id": user_id,
        "title": title,
        "text": text,
        "uploadedAt": datetime.utcnow()
    })