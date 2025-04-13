from database.mongo import mongo
from datetime import datetime

def save_script(user_id, lecture_id, summary):
    return mongo.db.scripts.insert_one({
        "user_id": user_id,
        "lecture_id": lecture_id,
        "summary": summary,
        "generatedAt": datetime.utcnow()
    })